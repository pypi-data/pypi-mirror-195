##
## Copyright (C) Optumi Inc - All rights reserved.
##
## You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
## To receive a copy of the licensing terms please write to contact@optumi.com or visit us at https://www.optumi.com.
##

from .Executable import *


class Script(Executable):
    """A class for executing Python Scripts. Extends Executable."""

    def __init__(self, path: str):
        """Initializes the class.

        Args:
            path (str): The path to the Script file to be executed.
        """
        super().__init__(path, "python script")

    def __str__(self):
        return super().__str__()
