#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#   Belati is tool for Collecting Public Data & Public Document from Website and other service for OSINT purpose.
#   This tools is inspired by Foca and Datasploit for OSINT
#   Copyright (C) 2017  cacaddv@gmail.com (Petruknisme a.k.a Aan Wahyu)
#   Version 0.1-dev

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

from lib.pywhois import whois
from logger import Logger
import urllib2
import sys

log = Logger()

class CheckDomain(object):
	def domain_checker(self, domain_name):
		req = urllib2.Request(domain_name)
		try:
			urllib2.urlopen(req)
			log.console_log("OK!")
		except urllib2.URLError, e:
			if str(e.reason) == "[Errno -2] Name or service not known":
				log.console_log("Not EXIST!")
				log.console_log("Check your internet connection or check your target domain")
				sys.exit()
			else:
				log.console_log("OK!")

	def alive_check(self, domain_name):
		request = urllib2.Request(domain_name, headers={'User-Agent' : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"})
		try:
			urllib2.urlopen(request)
			log.console_log("OK!")
		except urllib2.HTTPError, e:
			log.console_log("OK! - (" + str(e.getcode()) + ")")

	def whois_domain(self, domain_name):
		response = whois.whois(domain_name)
		log.console_log(response)

if __name__ == '__main__':
    CheckDomainApp = CheckDomain()
    CheckDomainApp
