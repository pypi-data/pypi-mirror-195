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

    # set the contents of the repo file
    # deb file:///opt/robin/download/repo (i.e.: elvira) + version (i.e.: 21.07.0.60388) + main
    # file:///opt/robin/repo/ specifies the location of the repository on the local filesystem
    # before this, robin-sd-download -p will run. (apt-get update)

    # check if the download directory exists
    download_dir = "/opt/robin/download"
    if os.path.isdir(download_dir):
        # get the latest folder from /opt/robin/download
        latest_pulled_version = max(os.listdir(download_dir))
    else:
        # use a default version if the directory does not exist
        latest_pulled_version = "initial"

    # Add GPG signing key.
    contents = f"deb file:///opt/robin/download/{latest_pulled_version}/ {ubuntu_version} main\n"

    if os.path.isfile(repo_file):
        logger.log(
            message=f"Repo file exists, checking contents at {repo_file}", log_level="info", to_terminal=False)
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
                    old_path=repo_file, new_path=f"{repo_file}.bak")
                sudo_file.create_sudo_file(
                    full_path=repo_file, contents=contents)
                return True
    else:
        logger.log(
            message=f"Repo file does not exist, creating it at {repo_file}", log_level="info", to_terminal=False)
        sudo_file.create_sudo_file(full_path=repo_file, contents=contents)
        return True
