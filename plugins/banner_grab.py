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

from logger import Logger
import urllib2
import sys
from user_agents import UserAgents

log = Logger()
ua = UserAgents()

class BannerGrab(object):
    def show_banner(self, domain_name):
        try:
            req = urllib2.Request(domain_name, headers={'User-Agent' : ua.get_user_agent() })
            header = urllib2.urlopen(req).info()
            log.console_log(header)
        except urllib2.HTTPError, e:
            print('Error code: ' + str(e.code))
            return e.code
        except Exception, detail:
            print('ERROR ' +  str(detail))
            return 1

if __name__ == '__main__':
    BannerGrabApp = BannerGrab()
    BannerGrabApp
