##
## Copyright (C) Optumi Inc - All rights reserved.
##
## You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
## To receive a copy of the licensing terms please write to contact@optumi.com or visit us at https://www.optumi.com.
##

import os
from .utils import *

import optumi_core as optumi


class Log:
    """Class for downloading the log file from a workload

    Methods:
        download(path): Download the log to the specified file
    """

    def __init__(self, name: str, output: list):
        """This function initializes the Log object and creates a new log file.

        Args:
            name (str): the name that will be used to create the log file.
            output (list of str): a list of strings representing the log entries to store in the logfile.
        """
        self._name = name
        self._output = output

    def download(self, path: str = None):
        """This function downloads the log file to the given path.

        Args:
            path (str, optional): the path where the log file should be stored. If not provided, the log file will be created in the current working directory with its name specified during initialization. Defaults to None.
        """
        f_name = optumi.utils.normalize_path(
            self._name.split("/")[-1] + ".log" if path is None else path, False
        )
        with open(f_name, "w+") as f:
            f.write(
                fixBackspace(fixCarriageReturn("".join([x[0] for x in self._output])))
            )
        print("Log saved to " + f_name)
