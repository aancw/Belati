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

import sys, socket
import ssl
import urllib.request, urllib.error, urllib.parse, http.client
from .user_agents import UserAgents
from urllib.parse import urlparse
from .logger import Logger
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
    def get(self, url_request, proxy_address, user_agents=None, mode=0):
        ''' request mode
        0: standart(plus http code)
        1: just check

        '''

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
            proxy_handler = urllib.request.ProxyHandler({ proxy_scheme: proxy})
            opener = urllib.request.build_opener(proxy_handler)
            opener.addheaders = [('User-agent', user_agent_fix )]
            urllib.request.install_opener(opener)
            req = urllib.request.Request(url_request)
            if mode == 0:
                data = urllib.request.urlopen(req)
            elif mode == 1:
                data = urllib.request.urlopen(req, timeout=25)
            return data
        except urllib.error.HTTPError as e:
            return e.code
        except urllib.error.URLError as e:
            return e.reason
        except Exception as detail:
            pass
        except http.client.BadStatusLine:
            pass
            
    def ssl_checker(self, domain):
        domain_fix = "https://{}".format(domain)

        try:
            # Skip SSL Verification Check!
            # https://stackoverflow.com/questions/27835619/ssl-certificate-verify-failed-error
            gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)  # Only for gangstars
            data = urllib.request.urlopen("https://{}".format(domain), timeout=25, context=gcontext)
            if "ERROR" in data or "Errno" in data:
                domain_fix = "http://{}".format(domain)
        except urllib.error.HTTPError as e:
            pass
        except urllib.error.URLError as e:
            domain_fix = "http://{}".format(domain)
        except ssl.SSLError as e:
            domain_fix = "http://{}".format(domain)
        except http.client.BadStatusLine:
            domain_fix = "http://{}".format(domain)

        return domain_fix

    def connection_test(self):
        server_test = "github.com"
        try:
            host = socket.gethostbyname(server_test)
            s = socket.create_connection((host, 80), 2)
            return True
        except:
            pass
        return False
