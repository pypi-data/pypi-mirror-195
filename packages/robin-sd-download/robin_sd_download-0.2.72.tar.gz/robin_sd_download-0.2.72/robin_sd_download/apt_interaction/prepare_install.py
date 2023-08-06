#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import os
import zipfile
from robin_sd_download.supportive_scripts import sudo_file
from robin_sd_download.api_interaction import get_software_info

GB = 1073741824  # number of bytes in one gigabyte
REQUIRED_SPACE_GB = 1  # required amount of disk space in gigabytes
REQUIRED_SPACE_BYTES = REQUIRED_SPACE_GB * GB
OFFLINE_SOFTWARES_PATH = '/offline_softwares'


def prepare_offline_apt():
    """
    Prepare offline apt by getting local IP address and checking if running as root.
    Also checks if the required amount of space is available in /offline_softwares folder.

    :return: None
    """
    # Get local IP address
    local_ip = subprocess.check_output(
        ['hostname', '-I']).decode('utf-8').strip()

    # Check if running as root
    if os.geteuid() != 0:
        print("Please run robin-sd-download package as root")
        return

    # Check if required amount of space is available in /offline_softwares folder
    available_space = os.statvfs(
        OFFLINE_SOFTWARES_PATH).f_bavail * os.statvfs(OFFLINE_SOFTWARES_PATH).f_frsize
    if available_space < REQUIRED_SPACE_BYTES:
        print(
            f"Not enough space in {OFFLINE_SOFTWARES_PATH} folder. Available space: {available_space}, Required space: {REQUIRED_SPACE_BYTES}")
        return

    print("Start Script")

    # Get IP address of remote system
    ip_address = input("IP Address of System: ")

    # Get password for remote system
    remote_pass = input("Robin User Password: ")

    # Set download folder
    dl_folder = '/var/www/html/download'

    # Remove zip file if it exists
    zipfile_path = '/var/www/html/download.zip'
    if os.path.isfile(zipfile_path):
        os.remove(zipfile_path)

    # Get type, version and build number from get_software() function

    # Get software list
    software_list = get_software_info.get_software_info()
    # print (software_list)
    software_type = software_list['software_type']
    software_version = software_list['version']

    # get ubuntu version of this system
    ubuntu_version = subprocess.check_output(
        ['lsb_release', '-cs']).decode('utf-8').strip()

    # Check if source folder exists: /var/www/html/download/sources.list -> if not create

    # Check if nvidia folder exists: /var/www/html/download/nvidia.list -> if not create

    # Add Robin package to sources list
    robin_list = f"deb [arch=amd64] http://{local_ip}/robin/{software_type}/{software_version} {ubuntu_version} main"
    sudo_file.write_file_with_sudo(
        os.path.join(dl_folder, 'robin.list'), robin_list)
    subprocess.run(['sudo', 'sed', '-r', f's/(\b[0-9]{{1,3}}\.){{3}}[0-9]{{1,3}}\b/{local_ip}/', os.path.join(
        dl_folder, 'sources.list'), '-i'], check=True)
    subprocess.run(['sudo', 'sed', '-r', f's/(\b[0-9]{{1,3}}\.){{3}}[0-9]{{1,3}}\b/{local_ip}/', os.path.join(
        dl_folder, 'nvidia.list'), '-i'], check=True)

    # Create zip file
    with zipfile.ZipFile(zipfile_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(dl_folder):
            for file in files:
                zipf.write(os.path.join(root, file), file)

    # Copy files to remote system
    # subprocess.run(['sudo', 'sshpass', '-p', remote_pass, 'scp', zipfile_path, f'robin@{ip_address}:/home/robin/'], check=True)
    # scriptfile = '/var/www/html/remote_install.sh'
    # subprocess.run(['sudo', 'sshpass', '-p', remote_pass, 'scp', scriptfile, f'robin@{ip_address}:/home/robin/'], check=True)

    # Run remote script
    # subprocess.run(['sudo', 'sshpass', '-p', remote_pass, 'ssh', '-t', f'robin@{ip_address}', 'sudo', 'bash', '/home/robin/remote_install.sh'], check=True)
