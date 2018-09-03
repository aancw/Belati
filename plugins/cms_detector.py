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

import sys, re, time, json
from .url_request import URLRequest
from .util import Util

url_req = URLRequest()
util = Util()

class CMSDetector(object):
	def __init__(self):

		data = load_json_app()

		techs = {}

		# check URL
	    for app_name, app_spec in data['apps'].items():
	        if 'url' in app_spec:
	            if contains(url, app_spec['url']):
	                add_app(techs, app_name, app_spec)

	        # download content
	    if None in (headers, html):
	        try:
	            request = urllib2.Request(url, None, {'User-Agent': user_agent})
	            if html:
	                # already have HTML so just need to make HEAD request for headers
	                request.get_method = lambda: 'HEAD'
	            response = urllib2.urlopen(request)
	            if headers is None:
	                headers = response.headers
	            if html is None:
	                html = response.read()
	        except Exception as e:
	            print('Error:', e)

    def crawl_search(self, domain, proxy_address):
        url = 'https://www.google.com/search?num=200&start=0&filter=0&hl=en&q=@' + domain
        try:
            response = url_req.standart_request(url, proxy_address)
            data = response.read().decode()
            dataStrip = re.sub('<[^<]+?>', '', data) # strip all html tags like <em>
            dataStrip1 =  re.findall(r'[a-zA-Z0-9._+-]+@[a-zA-Z0-9._+-]+' + domain, dataStrip)
            dataStrip2 = re.findall(r'[a-zA-Z0-9._+-]+@' + domain, dataStrip)
            dataEmail = set(dataStrip1 + dataStrip2)
            dataFix = [x for x in dataEmail if not x.startswith('x22') and not x.startswith('3D') and not x.startswith('x3d') and not x.startswith('Cached') and not x.startswith('page')] # ignore email because bad parsing
            return list(dataFix)
        except:
            pass

    def load_json_app():
    	filename = '{}/plugins/data/apps.json'.format(util.get_current_work_dir())
    	return json.load(open(filename))