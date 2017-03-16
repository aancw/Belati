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

# This is part of MailHarvester and EMINGOO regex
# Thanks to pantuts and maldevel

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

class HarvestEmail(object):
    def crawl_search(self, domain, proxy_address):
        try:
            if type(proxy_address) is list:
                # Get random proxy from list
                proxy_address_fix = random.choice(proxy_address)
            else:
                proxy_address_fix = proxy_address

            log.console_log(Y + "[*] Using Proxy Address : " + proxy_address_fix + W)
            url = 'https://www.google.com/search?num=200&start=0&filter=0&hl=en&q=@' + domain
            parse = urlparse(proxy_address_fix)
            proxy_scheme = parse.scheme
            proxy = str(parse.hostname) + ':' + str(parse.port)
            proxy_handler = urllib2.ProxyHandler({ proxy_scheme: proxy})
            opener = urllib2.build_opener(proxy_handler)
            opener.addheaders = [('User-agent', ua.get_user_agent() )]
            urllib2.install_opener(opener)
            req = urllib2.Request(url)
            data = urllib2.urlopen(req).read()
            dataStrip = re.sub('<[^<]+?>', '', data) # strip all html tags like <em>
            dataStrip1 =  re.findall(r'[a-zA-Z0-9._+-]+@[a-zA-Z0-9._+-]+' + domain, dataStrip)
            dataStrip2 = re.findall(r'[a-zA-Z0-9._+-]+@' + domain, dataStrip)
            dataEmail = set(dataStrip1 + dataStrip2)
            dataFix = [x for x in dataEmail if not x.startswith('x22') and not x.startswith('3D') and not x.startswith('x3d')] # ignore email because bad parsing
            return list(dataFix)
        except urllib2.URLError, e:
            return e

if __name__ == '__main__':
    HarvestEmailApp = HarvestEmail()
    HarvestEmailApp
