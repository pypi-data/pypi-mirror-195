##
## Copyright (C) Optumi Inc - All rights reserved.
##
## You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
## To receive a copy of the licensing terms please write to contact@optumi.com or visit us at https://www.optumi.com.
##

import optumi_core as optumi
from optumi_core.exceptions import OptumiException

import json, time


class Machine:
    """Class for representing a machine. It has two constructors, one to be used when creating a new
    machine and another when reconstructing from an existing Optumi instance.
    """

    status_values = ["Acquiring", "Configuring", "Busy", "Idle", "Releasing"]

    def __init__(
        self,
        uuid: str,
        size: str,
        dns_name: str,
        rate: float,
        promo: bool,
        app: str,
        state: str = None,
    ):
        """Constructor a Machine object.

        Args:
            uuid (str): The unique machine ID associated with this machine.
            size (str): The size type of this machine.
            dns_name (str): The domain name server name of this machine.
            rate (float): The hourly rate for this machine in USD.
            promo (bool): Whether this machine is being given a promotional rate or not.
            app (str): The application ID of the workload being executed on this machine.
            state (str): The current state of this machine, one of "Acquiring", "Configuring", "Busy", "Idle" or "Releasing"
        """
        self._uuid = uuid
        self._size = size
        self._dns_name = dns_name
        self._rate = "$" + str(round(rate, 2)) + "/hr"
        self._promo = promo
        self._app = app
        self._state = state
        self._last_refresh = time.time()

    @classmethod
    def reconstruct(cls, machine_map):
        return (
            machine_map["uuid"],
            machine_map["name"],
            machine_map["dnsName"],
            machine_map["rate"],
            machine_map["promo"],
            machine_map["app"],
            machine_map["state"],
        )

    def _refresh(self):
        now = time.time()
        if now - self._last_refresh > 5:
            self._last_refresh = now
            response = json.loads(optumi.core.get_machines().text)
            for machine in response["machines"]:
                if machine["uuid"] == self._uuid:
                    (
                        _,
                        _,
                        self._dns_name,
                        self._rate,
                        self._promo,
                        self._app,
                        self._state,
                    ) = Machine.reconstruct(machine)

    def release(self, override=False):
        """Release the machine

        Args:
            override (bool, optional): Whether to allow releasing a machine with an active workload or not. Defaults to False.

        Raises:
            OptumiException: If override is False and there is an active workload running on the machine.
        """
        if optumi.utils.is_dynamic():
            from .Workloads import Workloads

            current = Workloads.current()
            if current.machine._uuid == self._uuid:
                print("Releasing current machine")
                optumi.core.delete_machine(self._uuid)
                current.stop()
        else:
            workload = self.workload
            if workload != None:
                if override:
                    workload.stop()
                else:
                    raise OptumiException(
                        "Workload "
                        + str(workload)
                        + " is running on this machine. Stop the workload using workload.stop() or pass override=True into machine.release() to stop the workload before releasing."
                    )
            print("Releasing machine " + str(self) + "...")
            optumi.core.delete_machine(self._uuid)
            print("...completed")

    def is_visible(self):
        self._refresh()
        if (
            self._state == "requisition requested"
            or self._state == "requisition in progress"
            or self._state == "requisition completed"
            or self._state == "requisition completed"
            or self._state == "setup completed"
        ):
            return True
        return False

    @property
    def size(self):
        """Returns the size of the instance.

        Returns:
            int: The size of the instance.
        """
        self._refresh()
        return self._size

    @property
    def rate(self):
        """Returns the billing rate of the instance.

        Returns:
            float: The billing rate of the instance.
        """
        self._refresh()
        return self._rate

    @property
    def promo(self):
        """Returns wether a promotional rate is applied to the instance.

        Returns:
            bool: wether a promotional rate is applied to the instance.
        """
        self._refresh()
        return self._promo

    @property
    def dns_name(self):
        """Returns the domain name for the instance.

        Returns:
            string: the domain name for the instance.
        """
        self._refresh()
        return self._dns_name

    @property
    def workload(self):
        """Returns the Workload object running on the instance, if any.

        Returns:
            Workload: the Workload object running on the instance, if any.
        """
        self._refresh()
        if self._app == None:
            return None
        from .Workloads import Workloads

        ws = Workloads.list()
        for w in ws:
            if w._workload_uuid == self._app:
                return w

    @property
    def status(self):
        """Returns the status of the instance.

        Returns:
            string: The status of the instance (Acquiring, Configuring, Busy, Idle, Releasing).
        """
        if self._state in ["requisition requested", "requisition in progress"]:
            return "Acquiring"
        elif self._state in ["requisition completed"]:
            return "Configuring"
        elif self._state in ["setup completed"]:
            return "Busy" if self._app != None else "Idle"
        elif self._state in [
            "teardown requested",
            "sequestration requested",
            "sequestration in progress",
            "sequestration completed",
        ]:
            return "Releasing"
        else:
            return ""

    def __str__(self):
        return str(self._size) + " " + str(self._rate)
