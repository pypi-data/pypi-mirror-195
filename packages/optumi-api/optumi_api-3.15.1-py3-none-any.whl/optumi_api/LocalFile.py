##
## Copyright (C) Optumi Inc - All rights reserved.
##
## You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
## To receive a copy of the licensing terms please write to contact@optumi.com or visit us at https://www.optumi.com.
##

import optumi_core as optumi

import os, datetime, time
from uuid import uuid4

STORAGE_TOTAL = 0
STORAGE_LIMIT = 1024 * 1024 * 1024 * 1024  # Assume the largest storage total


# Support downloading object under a different name
# Add log and summary objects that support a download function
# Shared between local storage and cloud storage
class LocalFile:
    """Class for handling local files. This class allows developers to upload a file into cloud storage.

    Attributes:
        path (str): The location of the file on the local disk.
        hash (str): The hash of the file contents.
        size (int): The size, in bytes, of the file.
        created (str): A string containing the date and time for when the file was created, in ISO 8601 format.
        modified (str): A string containing the date and time for when the file was last modified, in ISO 8601 format.

    Methods:
        upload(wait=True): Upload the file to cloud storage. If 'wait' is True, it will wait until the upload is complete before returning.

    Example:
        fs = opt.LocalFile(path)
    """

    def __init__(
        self,
        path: str,
    ):
        """Constructor a LocalFile object.

        Args:
            path (str): the path of the local file
        """
        self._path = optumi.utils.normalize_path(path)

    def upload(self, wait=True):
        """Uploads a LocalFile object to cloud storage.

        Args:
            wait (bool, optional): A boolean indicating whether the upload should wait until it is complete before returning. Defaults to True.
        """
        key = str(uuid4())
        print("Uploading file...", self)
        optumi.core.upload_files(
            key, [self._path], True, STORAGE_TOTAL, STORAGE_LIMIT, True
        )

        if wait:
            while True:
                progress = optumi.core.get_upload_progress([key])
                time.sleep(0.2)
                if progress[key]["progress"] < 0:
                    break

            print("...completed")

    @property
    def path(self):
        """Return the path to the file.

        Returns:
            str: the path to the file.
        """
        return self._path

    @property
    def hash(self):
        """Return a hash of the file contents.

        Returns:
            str: a hash of the file contents
        """
        return optumi.utils.hash_file(self._path)

    @property
    def size(self):
        """Return the size of the file in bytes.

        Returns:
            int: the size of the file in bytes.
        """
        return os.path.getsize(self._path)

    @property
    def created(self):
        """Returns a string containing the date and time for when the file was created, in ISO 8601 format

        Returns:
            str: A string containing the date and time for when the file was created, in ISO 8601 format
        """
        return (
            datetime.datetime.utcfromtimestamp(os.stat(self._path).st_ctime).isoformat()
            + "Z"
        )

    @property
    def modified(self):
        """Returns a string containing the date and time for when the file was last modified, in ISO 8601 format

        Returns:
            str:  A string containing the date and time for when the file was created, in ISO 8601 format
        """
        return (
            datetime.datetime.utcfromtimestamp(os.stat(self._path).st_mtime).isoformat()
            + "Z"
        )

    def __str__(self):
        return self.path + " " + str(self.size) + " " + self.modified
