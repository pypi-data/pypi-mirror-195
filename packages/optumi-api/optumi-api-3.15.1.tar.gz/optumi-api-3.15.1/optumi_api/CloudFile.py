##
## Copyright (C) Optumi Inc - All rights reserved.
##
## You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
## To receive a copy of the licensing terms please write to contact@optumi.com or visit us at https://www.optumi.com.
##

import optumi_core as optumi
from optumi_core.exceptions import OptumiException

import os, datetime
from uuid import uuid4


class CloudFile:
    """CloudFile class for interacting with files in Optumi cloud storage.

    Attributes:
        path (str): The path to the file on the cloud storage service.
        versions (list of CloudFileVersion): A list of CloudFileVersion objects representing different versions of a file.

    Methods:
        download(wait=True): Download the latest version of the file from cloud storage.  If 'wait' is True, it will wait until the download is complete before returning.
        remove(): Remove all versions of the file from cloud storage.
    """

    def __init__(self, path: str, versions: list):
        """Constructor for CloudFile object.

        Args:
            path (str): The path to the file on the cloud storage service.
            versions (list of CloudFileVersion): A list of CloudFileVersion objects representing different versions of a file.

        Raises:
            OptumiException: If versions is empty, or if the path is not consistent throughout the various versions in the list.
        """
        if not versions:
            raise OptumiException("Missing CloudFile versions")
        self._path = path
        # Sort files by newest to oldest modification time
        self._versions = sorted(versions, key=lambda version: version.modified)
        # Make sure all versions have the proper path
        for v in versions:
            if v.path != path:
                raise OptumiException("CloudFile has inconsistent versions")

    def download(self, wait=True):
        """Downloads the newest version of the CloudFile.

        Args:
            wait (bool, optional): A boolean indicating whether the download should wait until it is complete before returning. Defaults to True.
        """
        # Download newest version
        self._versions[0].download(wait)

    def remove(self):
        """Removes all versions of this CloudFile from the cloud."""
        # Remove all versions of the file
        print("Removing file", self)
        optumi.core.delete_files(
            [x.hash for x in self._versions],
            [x.path for x in self._versions],
            [x.created for x in self._versions],
            "",
        )

    @property
    def versions(self):
        """Returns a list of CloudFileVersion objects sorted from the newest to the oldest.

        Returns:
            list of CloudFileVersion: versions
        """
        return self._versions

    @property
    def path(self):
        """Returns the path to the file.

        Returns:
            str: path
        """
        return self._path

    def __str__(self):
        return (
            self._path
            + " ("
            + str(len(self._versions))
            + (" versions)" if len(self._versions) > 1 else " version)")
        )
