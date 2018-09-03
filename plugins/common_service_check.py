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

import sys, socket, errno
from .logger import Logger
from .url_request import URLRequest


# Console color
G = '\033[92m'  # green
Y = '\033[93m'  # yellow
B = '\033[94m'  # blue
R = '\033[91m'  # red
W = '\033[0m'   # white

url_req = URLRequest()
log = Logger()

class CommonServiceCheck(object):
    ## STILL NOT ACCURATE!
    def check_available_service(self, host):
        list_available_port = []
        list_common_port = [21,22,23,25,53,80,110,111,135,139,143,443,445,993,995,1723,3306,3389,5900,8080]
        for port in list_common_port:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                s.connect((host, port))
                if port == 80:
                    data = url_req.header_info("http://" + host, "")
                    log.console_log("Found HTPP Service : ({} OPEN)".format(str(port)) )
                    log.console_log("\n{}".format(data))
                elif port == 443:
                    data = url_req.header_info("https://" + host, "")
                else:
                    print(("port :" + str(port) + " OPEN! " + s.recv(4096)))
            except socket.error as e:
                if e.errno == errno.ECONNREFUSED or e.errno == 113:
                    pass
                else:
                    print(("port :" + str(port) + str(e) + "closed"))
            s.close()
