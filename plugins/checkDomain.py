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
from logger import logger
import urllib2
import sys

log = logger()

class checkDomain(object):
	def domainChecker(self, domainName):
		req = urllib2.Request(domainName)
		try:
			urllib2.urlopen(req)
			log.consoleLog("OK!")
		except urllib2.URLError, e:
			if str(e.reason) == "[Errno -2] Name or service not known":
				log.consoleLog("Not EXIST!")
				log.consoleLog("Check your internet connection or check your target domain")
				sys.exit()
			else:
				log.consoleLog("OK!")

	def aliveCheck(self, domainName):
		request = urllib2.Request(domainName, headers={'User-Agent' : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"})
		try:
			urllib2.urlopen(request)
			log.consoleLog("OK!")
		except urllib2.HTTPError, e:
			log.consoleLog("OK! - (" + str(e.getcode()) + ")")

	def whoisDomain(self, domainName):
		response = whois.whois(domainName)
		log.consoleLog(response)

if __name__ == '__main__':
    checkDomainApp = checkDomain()
    checkDomainApp
