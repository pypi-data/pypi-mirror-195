##
## Copyright (C) Optumi Inc - All rights reserved.
##
## You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
## To receive a copy of the licensing terms please write to contact@optumi.com or visit us at https://www.optumi.com.
##

import optumi_core as optumi

import json

from .Machine import Machine

from optumi_core.exceptions import (
    OptumiException,
)


class Machines:
    """The Machines class is used to retrieve a list of active machines."""

    @classmethod
    def list(cls, status: str = None):
        """Returns a list of all active machines, optionally matching the status passed in.

        Args:
            status (str, optional): The status of the machine to match. Can be one of "Acquiring", "Configuring", "Busy", "Idle", "Releasing", Defaults to None.

        Raises:
            OptumiException: If an unexpected value is passed in for status.

        Returns:
            list of machines: A list of machines matching the criteria
        """
        if status != None and not status in Machine.status_values:
            raise OptumiException(
                "Unexpected machine status '"
                + status
                + "', expected one of "
                + str(Machine.status_values)
            )

        machines = []

        response = json.loads(optumi.core.get_machines().text)

        for machine in response["machines"]:
            machine = Machine(*Machine.reconstruct(machine))
            if (status is None and machine.is_visible()) or (machine.status == status):
                machines.append(machine)

        return machines
