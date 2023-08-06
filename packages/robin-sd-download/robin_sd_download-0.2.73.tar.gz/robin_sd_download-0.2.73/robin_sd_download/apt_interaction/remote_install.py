#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import os
import shutil
import datetime


def remote_install():
    """Installs the software on the remote machine.

    Returns:
        bool: True if the software was successfully installed, False otherwise.
    """

    print("Installing software on remote machine")
