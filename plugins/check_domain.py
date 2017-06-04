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

import sys
from lib.pywhois import whois
from logger import Logger
from url_request import URLRequest

url_req = URLRequest()
log = Logger()

class CheckDomain(object):
	def domain_checker(self, domain_name, proxy_address):
		try:
			data = url_req.just_url_open(domain_name, proxy_address)
			if data is not "" and data is not "notexist" and not "ERROR" in data:
				log.console_log("OK!")
		except:
			log.console_log("NOT OK!")

	def alive_check(self, domain_name, proxy_address):
		try:
			data = url_req.just_url_open(domain_name, proxy_address)
			if data is not "" and data is not "notexist" and not "ERROR" in data:
				log.console_log("OK!")
		except:
			log.console_log("NOT OK! ")

	def whois_domain(self, domain_name):
		response = whois.whois(domain_name)
		log.console_log(response)
		return response

if __name__ == '__main__':
    CheckDomainApp = CheckDomain()
    CheckDomainApp
