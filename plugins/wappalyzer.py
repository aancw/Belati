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

from Wappalyzer import Wappalyzer, WebPage
from logger import logger

log = logger()

class wappalyzer(object):
    def run_wappalyze(self, domain):
        analyzer = Wappalyzer.latest()
        webpage = WebPage.new_from_url(domain)
        analyze_result = analyzer.analyze(webpage)
        if analyze_result:
            for result in analyze_result:
                log.consoleLog(result)
        else:
            log.consoleLog("Result Not Found")

if __name__ == '__main__':
    wappalyzerApp = wappalyzer()
    wappalyzerApp
