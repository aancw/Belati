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

import sys, re, time
import urllib2

# This is part of MailHarvester and EMINGOO regex
# Thanks to pantuts and maldevel

class HarvestEmail(object):
    def crawl_search(self, domain):
        try:
            url = 'https://www.google.com/search?num=200&start=0&filter=0&hl=en&q=@' + domain
            req = urllib2.Request(url, headers={'User-Agent' : "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:19.0) Gecko/20100101 Firefox/49.0"})
            data = urllib2.urlopen(req).read()
            dataStrip = re.sub('<[^<]+?>', '', data) # strip all html tags like <em>
            dataStrip1 =  re.findall(r'[a-zA-Z0-9._+-]+@[a-zA-Z0-9._+-]+' + domain, dataStrip)
            dataStrip2 = re.findall(r'[a-zA-Z0-9._+-]+@' + domain, dataStrip)
            dataEmail = set(dataStrip1 + dataStrip2)
            dataFix = [x for x in dataEmail if not x.startswith('x22') and not x.startswith('3D') and not x.startswith('x3d')] # ignore email because bad parsing
            return list(dataFix)
        except urllib2.URLError, e:
            print(e)

if __name__ == '__main__':
    HarvestEmailApp = HarvestEmail()
    HarvestEmailApp
