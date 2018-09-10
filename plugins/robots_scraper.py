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

from .url_request import URLRequest

url_req = URLRequest()

class RobotsScraper(object):
    def check_robots(self, domain_name, proxy_address):
        try:
            url_request = "{}/robots.txt".format(domain_name)
            response = url_req.get(url_request, proxy_address, "", 1)
            data = response.read().decode()
            
            if data is not "" and data is not "notexist":
                # We need to check if file is valid, no redirect, no reload, or something
                if data.getcode() == 200 and data.getcode() != 302 and url_request in data.geturl() :
                    return data
        except:
            pass
