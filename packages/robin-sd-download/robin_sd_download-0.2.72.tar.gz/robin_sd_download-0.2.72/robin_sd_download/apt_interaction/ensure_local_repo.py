#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from robin_sd_download.supportive_scripts import logger
from robin_sd_download.supportive_scripts import sudo_file


def ensure_local_repo():
    """Ensures the local apt repository file exists and contains the expected contents.

    Returns:
        bool: True if the local repo file exists and contains the expected contents, or was successfully created.
    """
    repo_file = "/etc/apt/sources.list.d/robin-local.list"

    try:
        # get the current version of ubuntu
        ubuntu_version = os.popen("lsb_release -cs").read().strip()
    except (FileNotFoundError, PermissionError) as error:
        logger.log(
            message=f"Error when getting Ubuntu version: {error}", log_level="error", to_terminal=True)
        return False

    # set the contents of the repo file - check this later.
    # repo i.e.: elvira + version i.e.: 21.07.0.60388
    # file:///opt/robin/repo/ specifies the location of the repository on the local filesystem
    # so before this robin-sd-download -p will run. (when apt-get)

    # get the latest dated folder in opt/robin/download
    latest_dated_folder = os.popen(
        "ls -t /opt/robin/download | head -1").read().strip()
    print(latest_dated_folder)

    contents = "deb file:///opt/robin/download/" + \
        latest_dated_folder+"/" + ubuntu_version + " main\n"

    if os.path.isfile(repo_file):
        logger.log(message="Repo file exists, checking contents at " +
                   repo_file, log_level="info", to_terminal=False)
        # Ensure the contents of the file match the contents of the variable
        with open(repo_file, "r") as stream:
            if stream.read() == contents:
                logger.log(message="Repo file contents match",
                           log_level="info", to_terminal=False)
                return True
            else:
                logger.log(message="Repo file contents do not match, overwriting.",
                           log_level="error", to_terminal=True)
                # Copy the current file to a backup
                sudo_file.rename_sudo_file(
                    old_path=repo_file, new_path=repo_file + ".bak")
                sudo_file.create_sudo_file(
                    full_path=repo_file, contents=contents)
                return True
    else:
        logger.log(message="Repo file does not exist, creating it at " +
                   repo_file, log_level="info", to_terminal=False)
        sudo_file.create_sudo_file(full_path=repo_file, contents=contents)
        return True
