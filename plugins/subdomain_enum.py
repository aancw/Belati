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

from bs4 import BeautifulSoup
from dnsdumpster.DNSDumpsterAPI import DNSDumpsterAPI
from url_request import URLRequest

url_req = URLRequest()

class SubdomainEnum(object):
	def scan_dnsdumpster(self, domain_name):
		results = DNSDumpsterAPI().search(domain_name)
		return results

	def scan_crtsh(self, domain_name, proxy_address):
		try:
			url = "https://crt.sh/?q=%25." + domain_name
			data = url_req.standart_request(url, proxy_address)
			soup = BeautifulSoup( data, 'lxml')
			subdomain_list = []
			try:
				table = soup.findAll('table')[2]
				rows = table.find_all(['tr'])
				for row in rows:
					cells = row.find_all('td', limit=5)
					if cells:
						name = cells[3].text
						# we don't need wildcard domain
						if "*." not in name:
							subdomain_list.append(name)

				return list(set(subdomain_list))
			except:
				pass
		except:
			pass
