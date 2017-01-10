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

import re, os
import urllib2, urllib
from logger import logger
from tqdm import tqdm
import requests

# Console color
G = '\033[92m'  # green
Y = '\033[93m'  # yellow
B = '\033[94m'  # blue
R = '\033[91m'  # red
W = '\033[0m'   # white

log = logger()

class harvestPublicDocument(object):
    def init_crawl(self, domain):
        log.consoleLog(G + "[*] Gather Link from Google Search for domain " + domain + W)
        self.harvestPublicDoc(domain, "pdf")
        self.harvestPublicDoc(domain, "doc")
        self.harvestPublicDoc(domain, "xls")
        self.harvestPublicDoc(domain, "odt")
        self.harvestPublicDoc(domain, "ppt")
        self.harvestPublicDoc(domain, "rtf")
        self.harvestPublicDoc(domain, "txt")
        #https://www.google.com/search?q=site:domain.com%20ext:pdf&filter=0&num=100#q=site:domain.com+ext:txt&start=100&filter=0

    def harvestPublicDoc(self, domain, extension):
        log.consoleLog(G + "[*] Searching " + extension.upper() + " Document..." + W)
        totalFiles = 0
        try:
            url = 'https://www.google.com/search?q=site:' + domain + '%20ext:' + extension + '&filter=0&num=200'
            req = urllib2.Request(url, headers={'User-Agent' : "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:19.0) Gecko/20100101 Firefox/49.0"})
            data = urllib2.urlopen(req).read()
            regex = "(?P<url>https?://[^:]+\.%s)" % extension
            data = re.findall(regex, data)
            listFilesDownload = list(set(data))
            totalFiles = str(len(listFilesDownload))
            log.consoleLog(Y + "[*] Found " + totalFiles + " " + extension.upper() + " files!" + W )
            if totalFiles is not 0:
                log.consoleLog(G + "[*] Please wait, lemme download it for you ;) " + W)
                for filesDownload in listFilesDownload:
                    self.downloadFiles(filesDownload)
        except urllib2.URLError, e:
            log.consoleLog(e)

    def downloadFiles(self, url):
        filename = url.split('/')[-1]
        fullFilename = 'belatiFiles/%s' % filename
        if not os.path.exists(os.path.dirname(fullFilename)):
            try:
                os.makedirs(os.path.dirname(fullFilename))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

        with tqdm(unit='B', unit_scale=True, miniters=1,desc=filename) as t:
            urllib.urlretrieve(url, filename=fullFilename,reporthook=self.my_hook(t), data=None)

    def my_hook(self,t):
      """
      Wraps tqdm instance. Don't forget to close() or __exit__()
      the tqdm instance once you're done with it (easiest using `with` syntax).

      Example
      -------

      >>> with tqdm(...) as t:
      ...     reporthook = my_hook(t)
      ...     urllib.urlretrieve(..., reporthook=reporthook)

      """
      last_b = [0]

      def inner(b=1, bsize=1, tsize=None):
        """
        b  : int, optional
            Number of blocks just transferred [default: 1].
        bsize  : int, optional
            Size of each block (in tqdm units) [default: 1].
        tsize  : int, optional
            Total size (in tqdm units). If [default: None] remains unchanged.
        """
        if tsize is not None:
            t.total = tsize
        t.update((b - last_b[0]) * bsize)
        last_b[0] = b
      return inner

if __name__ == '__main__':
    harvestPublicDocumentApp = harvestPublicDocument()
    harvestPublicDocument
