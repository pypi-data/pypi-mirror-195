##
## Copyright (C) Optumi Inc - All rights reserved.
##
## You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
## To receive a copy of the licensing terms please write to contact@optumi.com or visit us at https://www.optumi.com.
##

from .NotebookConfig import create_config
from .Packages import Packages
from .LocalStorage import LocalStorage
from .Server import Server
from .Resource import Resource
from .Workload import Workload
from .EnvironmentVariables import EnvironmentVariables

import optumi_core as optumi
from optumi_core.exceptions import (
    NotLoggedInException,
    OptumiException,
)

import os, datetime, json
from typing import Union


class Executable:
    """The Executable class is used to run executable programs on Optumi with given environment and resource requirements.

    Attributes
        path (str): The absolute path of the program to be executed.
        program_type (str): The type of program being executed (e.g. python notebook, python script, docker container).

    Methods
        launch(*args): Launch the executed program as a Workload instance with given environment/resource parameters.
    """

    program_types = ["python notebook", "python script", "docker container", "unknown"]

    def __init__(self, path: str, program_type="unknown"):
        """Constructor an Executable object taking a path to the program and the type of the program.

        Args:
            path (str): the local path to the program
            program_type (str, optional): The type of the program. One of "python notebook", "python script", "docker container" or "unknown". Defaults to "unknown".

        Raises:
            OptumiException: If the program type is not specified properly
        """
        self._path = optumi.utils.normalize_path(path)
        if not program_type in Executable.program_types:
            raise OptumiException(
                "Unexpected program type '"
                + program_type
                + "', expected one of "
                + str(program_types)
            )
        self._program_type = program_type

    def __utcnow(self):
        return datetime.datetime.utcnow().isoformat() + "Z"

    def launch(
        self,
        wait=True,
        progress="summary",
        packages=Packages(),
        files=LocalStorage(),
        env: Union[EnvironmentVariables, list] = [],
        resource=None,
        notifications=None,
        interactive=False,
    ):
        """Launches a new executable service given a specific configuration.

        Args:
            wait (bool): Whether or not to wait for the workload to finish execution before returning. Defaults to True.
            progress (str): How much progress data to return with the launched workload. Can be one of "silent", "summary", "detail". Defaults to 'summary'.
            env (Union[EnvironmentVariables, list]): Environment variables to set when running the program.
            packages (Packages, optional):  Python packages required for executing the program. Defaults to empty.
            files (LocalStorage, optional): Any input files needed for the program's execution. Defaults to empty.
            resource (Server, Resource, optional): Server or Resource requirements for running the program. Defaults to None (Meaning a T4 machine will be used).
            notifications (Notification): User notification options when running the container. Defaults to None.
            interactive (bool, optional): Wether to run the program as an interactive session. Defaults to False.

        Raises:
            OptumiException: If any of the requirements are specified incorrectly.

        Returns:
            Workload: A workload representing the program.
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

        # Plug in session/job
        nb_config["interactive"] = interactive

        # Plug in program type
        nb_config["programType"] = self._program_type

        # Plug in packages
        nb_config["upload"]["requirements"] = "\n".join(packages)

        # Plug in files
        expanded = [f.path for f in files]

        # Make sure files are uploaded
        files.upload()
        nb_config["upload"]["files"] = [
            {"path": optumi.utils.replace_home_with_tilde(path), "enabled": True}
            for path in expanded
        ]

        # Register any unsaved environment variables with the controller
        # Plug in environment variables
        if type(env) is EnvironmentVariables:
            nb_config["integrations"] = [
                {
                    "name": env.name,
                    "enabled": True,
                    "integrationType": "environment variable",
                }
            ]
        else:
            nb_config["integrations"] = [
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

        with open(self._path, "r") as f:
            program = f.read()

        setup = json.loads(
            optumi.core.setup_notebook(
                optumi.utils.replace_home_with_tilde(self._path),
                self.__utcnow(),
                {
                    "path": optumi.utils.replace_home_with_tilde(self._path),
                    "content": program,
                },
                json.dumps(nb_config),
            ).text
        )

        # print(setup)

        workload_uuid = setup["uuid"]
        run_num = setup["runNum"]

        # this is necessary for the extension
        optumi.core.push_workload_initializing_update(workload_uuid, "Initializing")
        optumi.core.push_workload_initializing_update(workload_uuid, "stop")

        hashes = [optumi.utils.hash_file(f) for f in expanded]
        stats = [os.stat(f) if os.path.isfile(f) else None for f in expanded]
        creation_times = [
            datetime.datetime.utcfromtimestamp(stat.st_ctime).isoformat() + "Z"
            if stat != None
            else None
            for stat in stats
        ]
        last_modification_times = [
            datetime.datetime.utcfromtimestamp(stat.st_mtime).isoformat() + "Z"
            if stat != None
            else None
            for stat in stats
        ]
        sizes = [str(stat.st_size) if stat else None for stat in stats]

        try:
            optumi.core.launch_notebook(
                nb_config["upload"]["requirements"],
                hashes,
                [optumi.utils.replace_home_with_tilde(path) for path in expanded],
                creation_times,
                last_modification_times,
                sizes,
                workload_uuid,
                self.__utcnow(),
            )
        except Exception as err:
            # Surppress this error so we can poll for the proper status message
            pass

        launch_status = optumi.get_launch_status(workload_uuid)

        # print(launch_status)

        module_uuid = (
            launch_status["modules"][0] if "modules" in launch_status else None
        )

        workload = Workload(
            optumi.utils.replace_home_with_tilde(self._path),
            program,
            workload_uuid,
            module_uuid,
            nb_config,
            run_num,
        )
        if wait:
            workload.wait(progress)
        return workload

    @property
    def path(self):
        """Returns the path of the program.

        Returns:
            str: the path of the program
        """
        return self._path

    def __str__(self):
        return str(self._path)
