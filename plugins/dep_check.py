#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#   Belati is tool for Collecting Public Data & Public Document from Website and other service for OSINT purpose.
#   This tools is inspired by Foca and Datasploit for OSINT
#   Copyright (C) 2017  cacaddv@gmail.com (Petruknisme a.k.a Aan Wahyu)

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 2 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

# This file is part of Belati project

import sys, os
from logger import Logger

# Console color
G = '\033[92m'  # green
Y = '\033[93m'  # yellow
B = '\033[94m'  # blue
R = '\033[91m'  # red
W = '\033[0m'   # white

log = Logger()

try:
    # Check if pip module is installed
    import pip
except ImportError:
    log.console_log("{}[-] Sorry, please install pip before using Belati : http://www.pip-installer.org/en/latest/installing.html {}".format(R, W))
    sys.exit(1)

try:
    # Check for older pip version
    from pip._vendor.packaging.version import Version
except ImportError:
    log.console_log("{}[-] Old pip version detected, please upgrade using: sudo pip install --upgrade pip {}".format(Y, W))
    sys.exit(1)

class DepCheck(object):

    def check_dependency(self):
        list_deps = []
        missing_deps = []

        with open('requirements.txt') as f:
            list_deps = f.read().splitlines()

        pip_list = sorted([(i.key) for i in pip.get_installed_distributions()])

        for req_dep in list_deps:
            if req_dep not in pip_list:
                # Why this package is not in get_installed_distributions ?
                if str(req_dep) == "argparse":
                    pass
                else:
                    missing_deps.append(req_dep)

        if missing_deps:
            missing_deps_warning ="""
            You are missing a module required for Belati. In order to continue using Belati, please install them with:

            {}`pip install -r requirements.txt`{}

            or manually install missing modules with:

            {}`pip install {}`{}

            """

            log.console_log(missing_deps_warning.format(Y, W, Y, ' '.join(missing_deps), W))
            sys.exit()
