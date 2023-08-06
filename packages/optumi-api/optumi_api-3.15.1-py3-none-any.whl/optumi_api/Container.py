##
## Copyright (C) Optumi Inc - All rights reserved.
##
## You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
## To receive a copy of the licensing terms please write to contact@optumi.com or visit us at https://www.optumi.com.
##


from .NotebookConfig import create_config
from .Server import Server
from .Resource import Resource
from .Workload import Workload
from .ContainerRegistry import ContainerRegistry
from .EnvironmentVariables import EnvironmentVariables

import optumi_core as optumi
from optumi_core.exceptions import OptumiException

import os, datetime, json, re
from typing import Union


class Container:
    """A class for running containers

    Attributes:
        image (str): Image name.
        registry (ContainerRegistry, optional): Registry containing the image. Defaults to None.

    Methods:
        launch(wait=True, progress="summary", env: Union[EnvironmentVariables, list] = [], args=[], resource=None, notifications=None): Launches the container
    """

    def __init__(self, image: str, registry: ContainerRegistry = None):
        """Constructor for a Container object taking a n image name and an optional registry to log in to.
        Args:
            image (str): Image name.
            registry (ContainerRegistry, optional): Registry containing the image. Defaults to None.

        Raises:
            OptumiException: If invalid container name is specified.
        """
        if not bool(re.match("^[a-zA-Z0-9][a-zA-Z0-9/_.-]+$", image)):
            raise OptumiException("Invalid container name '" + image + "'")
        self._image = image
        self._registry = registry

    def __utcnow(self):
        return datetime.datetime.utcnow().isoformat() + "Z"

    def launch(
        self,
        wait=True,
        progress="summary",
        env: Union[EnvironmentVariables, list] = [],
        args=[],
        resource=None,
        notifications=None,
    ):
        """Launches a new container given a specific configuration.

        Args:
            wait (bool): Whether or not to wait for the workload to finish execution before returning. Defaults to True.
            progress (str): How much progress data to return with the launched workload. Can be one of "silent", "summary", "detail". Defaults to 'summary'.
            env (Union[EnvironmentVariables, list]): Environment variables to set when running the container.
            args ([str]): Command-line arguments to call when running the container.
            resource (Resource): Resource requirements for running the container. Default to None.
            notifications (Notification): User notification options when running the container. Defaults to None.

        Returns:
            Workload: A workload representing the container.
        """
        if resource is None:
            resource = Server(size="Standard_NC4as_T4_v3")

        if progress != None and not progress in Workload.progress:
            raise OptumiException(
                "Unexpected progress '"
                + progress
                + "', expected one of "
                + str(Workload.progress)
            )

        # Start with blank config
        nb_config = create_config()

        # Plug in program type
        nb_config["programType"] = "docker container"

        # Register any unsaved container registries with the controller
        # Plug in container registries

        nb_config["integrations"] = []

        if self._registry:
            nb_config["integrations"] += [
                {
                    "name": self._registry.name,
                    "enabled": True,
                    "integrationType": "generic container registry",
                }
            ]

        # Register any unsaved environment variables with the controller
        # Plug in environment variables
        if type(env) is EnvironmentVariables:
            nb_config["integrations"] += [
                {
                    "name": env.name,
                    "enabled": True,
                    "integrationType": "environment variable",
                }
            ]
        else:
            nb_config["integrations"] += [
                {
                    "name": e.name,
                    "enabled": True,
                    "integrationType": "environment variable",
                }
                for e in env
            ]

        # Plug in resource requirements
        if type(resource) is Server:
            nb_config["machineAssortment"] = [resource.provider + ":" + resource.size]
        elif type(resource) is Resource:
            nb_config["machineAssortment"] = []
            if type(resource.gpu) is bool:
                nb_config["graphics"]["cores"] = [1 if resource.gpu else -1, -1, -1]
            elif type(resource.gpu) is str:
                nb_config["graphics"]["cores"] = [1, -1, -1]
                nb_config["graphics"]["boardType"] = resource.gpu

            nb_config["graphics"]["memoryPerCard"] = resource.memory_per_card

        # Plug in requirements
        if notifications != None:
            nb_config["notifications"] = {
                "jobStartedSMSEnabled": notifications.job_started,
                "jobCompletedSMSEnabled": notifications.job_completed,
                "jobFailedSMSEnabled": notifications.job_failed,
                "packageReadySMSEnabled": False,
            }

        container_name = self._image

        setup = json.loads(
            optumi.core.setup_notebook(
                container_name,
                self.__utcnow(),
                {
                    "path": container_name,
                    "content": json.dumps(
                        {
                            "containerName": container_name,
                            "args": args,
                        }
                    ),
                },
                json.dumps(nb_config),
            ).text
        )

        # print(setup)

        # TODO:JJ What do we do about error handling for these calls

        workload_uuid = setup["uuid"]
        run_num = setup["runNum"]

        # this is necessary for the extension
        optumi.core.push_workload_initializing_update(workload_uuid, "Initializing")
        optumi.core.push_workload_initializing_update(workload_uuid, "stop")

        optumi.core.launch_notebook(
            nb_config["upload"]["requirements"],
            [],
            [],
            [],
            [],
            [],
            workload_uuid,
            self.__utcnow(),
        )

        launch_status = optumi.get_launch_status(workload_uuid)

        # print(launch_status)

        module_uuid = (
            launch_status["modules"][0] if "modules" in launch_status else None
        )

        workload = Workload(
            container_name,
            container_name,
            workload_uuid,
            module_uuid,
            nb_config,
            run_num,
        )

        if wait:
            workload.wait(progress)
        return workload

    @property
    def image(self):
        """Returns the image name

        Returns:
            str: the image name
        """
        return self._image

    @property
    def registry(self):
        """Returns the container registry

        Returns:
            ContainerRegistry: the container registry
        """
        return self._registry

    def __str__(self):
        return self._registry.url + "/" + self._image if self._registry else self._image
