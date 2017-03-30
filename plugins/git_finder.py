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
import urllib2
from logger import Logger
from user_agents import UserAgents
from urlparse import urlparse
import random

# Console color
G = '\033[92m'  # green
Y = '\033[93m'  # yellow
B = '\033[94m'  # blue
R = '\033[91m'  # red
W = '\033[0m'   # white

log = Logger()
ua = UserAgents()

class GitFinder(object):
    def check_git(self, domain, proxy_address):
        if type(proxy_address) is list:
            # Get random proxy from list
            proxy_address_fix = random.choice(proxy_address)
        else:
            proxy_address_fix = proxy_address

        if proxy_address is not "":
            log.console_log("{}[*] Using Proxy Address : {}{}".format(Y, proxy_address_fix, W))

        url = "http://" + domain + "/.git/HEAD"
        try:
            parse = urlparse(proxy_address_fix)
            proxy_scheme = parse.scheme
            proxy = str(parse.hostname) + ':' + str(parse.port)
            proxy_handler = urllib2.ProxyHandler({ proxy_scheme: proxy})
            opener = urllib2.build_opener(proxy_handler)
            opener.addheaders = [('User-agent', ua.get_user_agent() )]
            urllib2.install_opener(opener)
            req = urllib2.Request(url)
            data = urllib2.urlopen(req).read(200).decode()

            if not 'refs/heads' in data:
                return False
            else:
                return True

        except urllib2.HTTPError, e:
            print('Error code: {}'.format( str(e.code)))
            return e.code
        except Exception, detail:
            print('ERROR {}'.format(str(detail)))
