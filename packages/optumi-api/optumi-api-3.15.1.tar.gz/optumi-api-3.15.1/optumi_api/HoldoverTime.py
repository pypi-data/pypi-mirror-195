##
## Copyright (C) Optumi Inc - All rights reserved.
##
## You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
## To receive a copy of the licensing terms please write to contact@optumi.com or visit us at https://www.optumi.com.
##

import optumi_core as optumi


class HoldoverTime:
    """A class for calculating the holdover time in seconds.

    Attributes:
        minutes (int): Minutes to store holdover time.
        hours (int): Hours to store holdover time.

    Methods:
        init (self, minutes: int = 0, hours: int = 0): Initializes HoldoverTime instance with the given minutes and hours. If none provided, defaults to 0.
    """

    def __init__(self, minutes: int = 0, hours: int = 0):
        """Constructor a HoldoverTime object.

        Args:
            minutes (int, optional): The minutes of holdover time. Defaults to 0.
            hours (int, optional): The seconds of holdover time. Defaults to 0.
        """
        self._seconds = (60 * minutes) + (60 * 60 * hours)

    @property
    def seconds(self):
        """Returns the holdover time in seconds.

        Returns:
            int: the holdover time in seconds.
        """
        return self._seconds

    def __str__(self):
        return str(self._seconds // 60) + " min"
