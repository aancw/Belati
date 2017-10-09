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

import sys, re, time
from url_request import URLRequest

# Console color
G = '\033[92m'  # green
Y = '\033[93m'  # yellow
B = '\033[94m'  # blue
R = '\033[91m'  # red
W = '\033[0m'   # white

url_req = URLRequest()

class SVNFinder(object):
    def check_svn(self, domain, proxy_address):
        try:
            data = url_req.just_url_open(url_req.ssl_checker(domain) + "/.svn/", proxy_address)

            if data is not None and data is not "notexist":
                if data == 403:
                    return data
                if data.getcode() == 200 and data.getcode() != 302 and url_request in data.geturl():
                    return data.getcode()
        except:
            pass
