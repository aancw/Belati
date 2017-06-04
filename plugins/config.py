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

import sys, os, errno
import ConfigParser
from logger import Logger

# Console color
G = '\033[92m'  # green
Y = '\033[93m'  # yellow
B = '\033[94m'  # blue
R = '\033[91m'  # red
W = '\033[0m'   # white

log = Logger()
config = ConfigParser.ConfigParser()

class Config(object):
    def __init__(self):
        self.config_file = "belati.conf"
        if os.path.isfile(self.config_file):
            pass
        else:
            log.console_log("{}[-] No Configuration file found. Setting up...{}".format(Y, W))
            self.init_config_file()

    def get_config(self, conf_section, conf_key):
        config.read(self.config_file)
        value = config.get(conf_section, conf_key)
        return value

    def set_config(self, conf_section, conf_key, conf_value):
        config.read(self.config_file)
        config.set(conf_section, conf_key, conf_value)
        with open(self.config_file, "wb") as conf_file:
            config.write(conf_file)

    def init_config_file(self):
        log.console_log("\n{} -----> Initiating Configuration <-----\n{}".format(Y, W))
        db_location = raw_input("Please enter Belati Database Location [belati.db]:") or "belati.db"

        config.add_section("Database")
        self.set_config("Database", "db_location", db_location)
