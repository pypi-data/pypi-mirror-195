##
## Copyright (C) Optumi Inc - All rights reserved.
##
## You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
## To receive a copy of the licensing terms please write to contact@optumi.com or visit us at https://www.optumi.com.
##

import optumi_core as optumi

from .CloudFile import *
from .CloudFileVersion import *

import json, datetime, time

from pathlib import Path


# Support downloading object under a different name
class CloudStorage(list):
    """This class provides functionality for listing, downloading, and deleting files from cloud storage.

    Methods:
        download(wait=True): Download the latest version of multiple files from cloud storage. If 'wait' is True, it will wait until the download is complete before returning.
        remove(): Deletes multiple file from cloud storage.
        list(): Returns a list of all CloudFile objects stored on the cloud.
        find(self, match="", contains=""): Finds and returns CloudFile objects stored on the cloud matching the given match or containing the given contains path.
    """

    def __init__(self, files: list = []):
        """Constructor for a CloudStorage object taking a list of file objects as an argument.

        Args:
            files (list of CloudFile, optional): List of files to create a cloud storage object for. This can be useful for performing batch downloads/removal on a list of CloudFile objects. Defaults to [].
        """
        super().__init__(files)

    def download(self, wait=True):
        """Downloads the newest version of all CloudFile objects.

        Args:
            wait (bool, optional): Downloads the given version of a file from the cloud. If 'wait' is True, it will wait until the download is complete before returning. Defaults to True.
        """
        if len(self) > 0:
            key = str(uuid4())
            print("Downloading", "files..." if len(self) > 1 else "file...")
            for f in self:
                print(f)
            optumi.core.download_files(
                key,
                [x.versions[0].hash for x in self],
                [x.versions[0].path for x in self],
                [x.versions[0].size for x in self],
                False,
                None,
            )

            if wait:
                while True:
                    progress = optumi.core.get_download_progress([key])
                    time.sleep(0.2)
                    if progress[key]["progress"] < 0:
                        break

                print("...completed")

    def remove(self):
        """Removes all versions of all CloudFile objects."""
        if len(self) > 0:
            print("Removing", "files..." if len(self) > 1 else "file...")
            for f in self:
                print(f)
            hashes = []
            paths = []
            created = []

            for cloud_file in self:
                for version in cloud_file.versions:
                    hashes.append(version.hash)
                    paths.append(version.path)
                    created.append(version.created)

            optumi.core.delete_files(
                hashes,
                paths,
                created,
                "",
            )
            print("...completed")

    @classmethod
    def list(self):
        """Lists all files in the cloud.

        Returns:
            CloudStorage: All files in the cloud
        """
        res = optumi.core.list_files()
        response = json.loads(res.text)
        files = CloudStorage()
        versions = {}

        for i in range(len(response["files"])):
            path = response["files"][i]
            version = CloudFileVersion(
                path,
                response["hashes"][i],
                response["filessize"][i],
                response["filescrt"][i],
                response["filesmod"][i],
            )
            if path in versions:
                versions[path].append(version)
            else:
                versions[path] = [version]

        for path in versions:
            files.append(CloudFile(path, versions[path]))

        return files

    @classmethod
    def find(self, match="", contains=""):
        """Finds files in the cloud matching a given file name or containing a keyword.

        Args:
            match (str, optional): File name to match. Defaults to "".
            contains (str, optional): Keyword to match anywhere in the file path. Defaults to "".

        Returns:
            CloudStorage: All matching files in the cloud
        """
        if match:
            return CloudStorage(
                [
                    x
                    for x in CloudStorage.list()
                    if optumi.utils.normalize_path(match, strict=False)
                    == optumi.utils.normalize_path(x.path, strict=False)
                ]
            )
        elif contains:
            return CloudStorage(
                [
                    x
                    for x in CloudStorage.list()
                    if str(contains)
                    in optumi.utils.normalize_path(x.path, strict=False)
                ]
            )
        else:
            return CloudStorage([])

    def __str__(self):
        return str([str(x) for x in self])
