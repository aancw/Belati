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
from logger import Logger
from distutils.version import LooseVersion, StrictVersion
from urlparse import urlparse
from url_request import URLRequest

# Console color
G = '\033[92m'  # green
Y = '\033[93m'  # yellow
B = '\033[94m'  # blue
R = '\033[91m'  # red
W = '\033[0m'   # white

log = Logger()
url_req = URLRequest()

class Util(object):
    def check_python_version(self):
	    if sys.version[:3] == "2.7" or "2" in sys.version[:3]:
	        log.console_log("{}[*] Python version OK! {}{}".format(G, sys.version[:6], W))
	    elif "3" in sys.version[:3]:
	        log.console_log("{}[-] Nope. This system not yet compatible for Python 3!{}".format(Y, W))
	        sys.exit()
	    else:
	        log.console_log("{}[-] Duh. Your python version too old for running this :({}".format(Y, W))
	        sys.exit()

    def do_command(self, command, parameter):
    	full_command = "{} {}".format(command, parameter)
        process = subprocess.Popen(shlex.split(full_command), stdout=subprocess.PIPE)
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                log.console_log(output.strip())
        rc = process.poll()
        return rc
	
    def clean_version_string(self, text):
    	# strip v0.2.2-dev
    	strip_dev = text.strip("-dev\n")
    	return strip_dev

    def get_current_work_dir(self):
		return os.getcwd()

    def clean_list_string(self, text):
    	return str(", ".join(text))
   
    def strip_scheme(self, url):
	    parsed = urlparse(url)
	    scheme = "%s://" % parsed.scheme
	    return parsed.geturl().replace(scheme, '', 1)
