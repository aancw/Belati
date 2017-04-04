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

import urllib2
from user_agents import UserAgents
from urlparse import urlparse
from logger import Logger
import random

# Console color
G = '\033[92m'  # green
Y = '\033[93m'  # yellow
B = '\033[94m'  # blue
R = '\033[91m'  # red
W = '\033[0m'   # white

log = Logger()
ua = UserAgents()

class URLRequest(object):
    def standart_request(self, url_request, proxy_address, user_agents=None):
        try:
            if type(proxy_address) is list:
                # Get random proxy from list
                proxy_address_fix = random.choice(proxy_address)
            else:
                proxy_address_fix = proxy_address

            if proxy_address is not "":
                log.console_log("{}[*] Using Proxy Address : {}{}".format(Y, proxy_address_fix, W))

            if user_agents is not None:
                user_agent_fix = user_agents
            else:
                user_agent_fix = ua.get_user_agent()

            parse = urlparse(proxy_address_fix)
            proxy_scheme = parse.scheme
            proxy = str(parse.hostname) + ':' + str(parse.port)
            proxy_handler = urllib2.ProxyHandler({ proxy_scheme: proxy})
            opener = urllib2.build_opener(proxy_handler)
            opener.addheaders = [('User-agent', user_agent_fix )]
            urllib2.install_opener(opener)
            req = urllib2.Request(url_request)
            data = urllib2.urlopen(req).read()
            return data
        except urllib2.HTTPError, e:
            log.console_log('Error code: {}'.format( str(e.code)))
            return e.code
        except Exception, detail:
            log.console_log('ERROR {}'.format( str(detail)))
            return 1

    def header_info(self, url_request, proxy_address):
        try:
            if type(proxy_address) is list:
                # Get random proxy from list
                proxy_address_fix = random.choice(proxy_address)
            else:
                proxy_address_fix = proxy_address

            if proxy_address is not "":
                log.console_log("{}[*] Using Proxy Address : {}{}".format(Y, proxy_address_fix, W))

            parse = urlparse(proxy_address_fix)
            proxy_scheme = parse.scheme
            proxy = str(parse.hostname) + ':' + str(parse.port)
            proxy_handler = urllib2.ProxyHandler({ proxy_scheme: proxy})
            opener = urllib2.build_opener(proxy_handler)
            opener.addheaders = [('User-agent', ua.get_user_agent() )]
            urllib2.install_opener(opener)
            req = urllib2.Request(url_request)
            data = urllib2.urlopen(req).info()
            return data
        except urllib2.HTTPError, e:
            log.console_log('Error code: {}'.format( str(e.code)))
            return e.code
        except Exception, detail:
            log.console_log('ERROR {}'.format( str(detail)))
            return 1

    def just_url_open(self, url_request, proxy_address):
        try:
            if type(proxy_address) is list:
                # Get random proxy from list
                proxy_address_fix = random.choice(proxy_address)
            else:
                proxy_address_fix = proxy_address

            if proxy_address is not "":
                log.console_log("{}[*] Using Proxy Address : {}{}".format(Y, proxy_address_fix, W))

            parse = urlparse(proxy_address_fix)
            proxy_scheme = parse.scheme
            proxy = str(parse.hostname) + ':' + str(parse.port)
            proxy_handler = urllib2.ProxyHandler({ proxy_scheme: proxy})
            opener = urllib2.build_opener(proxy_handler)
            opener.addheaders = [('User-agent', ua.get_user_agent() )]
            urllib2.install_opener(opener)
            req = urllib2.Request(url_request)
            data = urllib2.urlopen(req)
            return data
    	except urllib2.URLError, e:
			if str(e.reason) == "[Errno -2] Name or service not known":
				log.console_log("Not EXIST!")
				log.console_log("Check your internet connection or check your target domain")
				sys.exit()

    def ssl_checker(self, domain):
        use_ssl = False

        try:
            urllib2.urlopen("https://{}".format(domain), timeout=2)
            use_ssl = True
        except urllib2.HTTPError, e:
            pass
        except urllib2.URLError, e:
            pass

        if use_ssl == False:
            return "http://{}".format(domain)
        else:
            return "https://{}".format(domain)
