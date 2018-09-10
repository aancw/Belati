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

# This script based on builtwith from Richard Penman
# https://bitbucket.org/richardpenman/builtwith

import sys, re, time, json, six
from .url_request import URLRequest
from .util import Util

url_req = URLRequest()
util = Util()

class CMSDetector(object):
	def __init__(self):
		self.data = self.load_json_app()
		self.techs = {}

	def detect(self, url, proxy_address):
		html = None
		headers = None

		# check URL
		for app_name, app_spec in self.data['apps'].items():
			if 'url' in app_spec:
				if self.contains(url, app_spec['url']):
					self.add_app(self.techs, app_name, app_spec)

		try: 
			response = url_req.get(url_req.ssl_checker(url), proxy_address)
			http_data = response.read().decode()
			headers = response.headers
			html = http_data
		except Exception as e:
			print('Error:', e)

		# check headers
		if headers:
			for app_name, app_spec in self.data['apps'].items():
				if 'headers' in app_spec:
					if self.contains_dict(headers, app_spec['headers']):
						self.add_app(self.techs, app_name, app_spec)
	    
		# check html
		if html:
			for app_name, app_spec in self.data['apps'].items():
				for key in 'html', 'script':
					snippets = app_spec.get(key, [])
					if not isinstance(snippets, list):
						snippets = [snippets]
					for snippet in snippets:
						if self.contains(html, snippet):
							self.add_app(self.techs, app_name, app_spec)
							break

        # check meta
        # XXX add proper meta data parsing
		if six.PY3 and isinstance(html, bytes):
			html = html.decode()
		metas = dict(re.compile('<meta[^>]*?name=[\'"]([^>]*?)[\'"][^>]*?content=[\'"]([^>]*?)[\'"][^>]*?>', re.IGNORECASE).findall(html))
		for app_name, app_spec in self.data['apps'].items():
			for name, content in app_spec.get('meta', {}).items():
				if name in metas:
					if self.contains(metas[name], content):
						self.add_app(self.techs, app_name, app_spec)
						break

		return self.techs

	def add_app(self, techs, app_name, app_spec):
		"""Add this app to technology
		"""
		for category in self.get_categories(app_spec):
			if category['name'] not in self.techs:
				self.techs[category['name']] = []
			if app_name not in self.techs[category['name']]:
				self.techs[category['name']].append(app_name)
				implies = app_spec.get('implies', [])
				if not isinstance(implies, list):
					implies = [implies]
				for app_name in implies:
					self.add_app(self.techs, app_name, self.data['apps'][app_name])
	
	def get_categories(self, app_spec):
		"""Return category names for this app_spec
		"""
		return [self.data['categories'][str(c_id)] for c_id in app_spec['cats']]

	def contains(self, v, regex):
		"""Removes meta data from regex then checks for a regex match
		"""
		if six.PY3 and isinstance(v, bytes):
			v = v.decode()

		return re.compile(regex.split('\\;')[0], flags=re.IGNORECASE).search(v)


	def contains_dict(self, d1, d2):
		"""Takes 2 dictionaries
		
		Returns True if d1 contains all items in d2"""
		for k2, v2 in d2.items():
			v1 = d1.get(k2)
			if v1:
				if not self.contains(v1, v2):
					return False
			else:
				return False
		
		return True

	def load_json_app(self):
		# data from https://github.com/AliasIO/Wappalyzer/
		filename = '{}/plugins/data/apps.json'.format(util.get_current_work_dir())
		json_data = json.load(open(filename))
		return json_data

if __name__ == '__main__':
    cms = CMSDetector()