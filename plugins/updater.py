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

# All Utilities Function will be here ;)

import sys, os
import shlex, subprocess
from .logger import Logger
from .config import Config
from pkg_resources import parse_version
from urllib.parse import urlparse
from .url_request import URLRequest
from .util import Util

# Console color
G = '\033[92m'  # green
Y = '\033[93m'  # yellow
B = '\033[94m'  # blue
R = '\033[91m'  # red
W = '\033[0m'   # white

log = Logger()
url_req = URLRequest()
util = Util()
conf = Config()

class Updater(object):
    def check_update(self, version):
        # If git repo available it will result 0 and 32768 when no repo available
        if not (os.path.isdir(".git") and os.system('git rev-parse 2> /dev/null > /dev/null')) == 0:
            log.console_log("{}[-] No Git Control. Skip update check... {}".format(Y, W))
        else:
            connection_status = url_req.connection_test()
            remote_version_url = "https://raw.githubusercontent.com/aancw/Belati/master/version"
            log.console_log("{}[+] Checking Network Connection... {} {}".format(G, "OK" if connection_status else "FAILED" ,W))

            if not connection_status:
                log.console_log("{}[-] Belati can't be used in Offline Mode. Please check your network connection {}".format(R, W))
                sys.exit()
            else:
                log.console_log("{}[+] Checking Version Update for Belati... {}".format(G, W))

                try:
                    response = url_req.get(remote_version_url, "")
                    data = response.read().decode()
                    remote_version = data

                    if self.update_version(version, remote_version):
                        log.console_log("{}[+] Update is available for version {}{}".format(G, remote_version, W))
                        log.console("{}[+] CHANGELOG: https://github.com/aancw/Belati/CHANGELOG.md {}".format(G, remote_version, W))
                        log.console_log("[*] Updating from master repo")
                        self.do_update()
                        self.migrate_db()
                    else:
                        log.console_log("{}[+] Belati version is uptodate \m/{}".format(Y, W))
                except:
                    pass

    def update_version(self, local_version, remote_version):
        return parse_version(util.clean_version_string(local_version)) < parse_version(util.clean_version_string(remote_version))

    def do_update(self):
        util.do_command("git", "pull")

    def migrate_db(self):
        log.console_log("{}[+] Make database migration{}".format(Y, W))
        py_bin = conf.get_config("Environment", "py_bin")
        command = "{} web/manage.py".format(py_bin)
        util.do_command(command,"makemigrations web")
        util.do_command(command,"migrate web")
