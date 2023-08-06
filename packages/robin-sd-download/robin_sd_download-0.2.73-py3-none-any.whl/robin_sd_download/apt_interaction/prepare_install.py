#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import os
import zipfile
from robin_sd_download.supportive_scripts import sudo_file
from robin_sd_download.api_interaction import get_software_info

GB = 1024 * 1024 * 1024  # number of bytes in one gigabyte
# required amount of space in gigabytes - CHANGE THIS IN PRODUCTION
REQUIRED_SPACE_GB = 30


def check_space():
    """
    Check if required amount of space is available on the disk.
    """
    statvfs = os.statvfs('/')
    available_space = statvfs.f_bavail * statvfs.f_frsize
    required_space = REQUIRED_SPACE_GB * GB
    if available_space < required_space:
        print(
            f"Not enough space on the disk. Available space: {available_space/GB:.2f} GB, Required space: {required_space/GB:.2f} GB")
        return False
    return True


def prepare_offline_apt():
    """
    Prepare offline apt by getting local IP address and checking if running as root.
    """
    # Get local IP address
    local_ip = subprocess.check_output(
        ['hostname', '-I']).decode('utf-8').strip()

    # Check if running as root
    if os.geteuid() != 0:
        print("Please run robin-sd-download package as root")
        return

    # Check if required amount of space is available in a partition with at least 1 TB of free space
    if not check_space():
        return

    # prompt user to enter the ubuntu version of target device
    ubuntu_version = input(
        "Please enter the ubuntu version for the target device (e.g. trusty, xenial, bionic, focal, jammy): ")

    # validate ubuntu_version
    if ubuntu_version not in ['trusty', 'xenial', 'bionic', 'focal', 'jammy']:
        print("Invalid ubuntu version. Please try again.")
        return

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
    # make software_type lowercase
    software_type = software_type.lower()
    software_version = software_list['version']

    # get ubuntu version of this current system
    # ubuntu_version = subprocess.check_output(
    #     ['lsb_release', '-cs']).decode('utf-8').strip()

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
