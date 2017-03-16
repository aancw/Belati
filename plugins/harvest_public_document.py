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

import re, os
import urllib2, urllib
from logger import Logger
from tqdm import tqdm
import requests
from user_agents import UserAgents
from urlparse import urlparse
import random

# Console color
G = '\033[92m'  # green
Y = '\033[93m'  # yellow
B = '\033[94m'  # blue
R = '\033[91m'  # red
W = '\033[0m'   # white

log = Logger()
ua = UserAgents()

class HarvestPublicDocument(object):
    def init_crawl(self, domain, proxy_address):
        log.console_log(G + "[*] Gather Link from Google Search for domain " + domain + W)
        self.harvest_public_doc(domain, "pdf", proxy_address)
        self.harvest_public_doc(domain, "doc", proxy_address)
        self.harvest_public_doc(domain, "xls", proxy_address)
        self.harvest_public_doc(domain, "odt", proxy_address)
        self.harvest_public_doc(domain, "ppt", proxy_address)
        self.harvest_public_doc(domain, "rtf", proxy_address)
        self.harvest_public_doc(domain, "txt", proxy_address)
        #https://www.google.com/search?q=site:domain.com%20ext:pdf&filter=0&num=100#q=site:domain.com+ext:txt&start=100&filter=0

    def harvest_public_doc(self, domain, extension, proxy_address):
        log.console_log(G + "[*] Searching " + extension.upper() + " Document..." + W)
        total_files = 0
        try:
            if type(proxy_address) is list:
                # Get random proxy from list
                proxy_address_fix = random.choice(proxy_address)
            else:
                proxy_address_fix = proxy_address

            log.console_log(Y + "[*] Using Proxy Address : " + proxy_address_fix + W)
            url = 'https://www.google.com/search?q=site:' + domain + '%20ext:' + extension + '&filter=0&num=200'
            parse = urlparse(proxy_address_fix)
            proxy_scheme = parse.scheme
            proxy = str(parse.hostname) + ':' + str(parse.port)
            proxy_handler = urllib2.ProxyHandler({ proxy_scheme: proxy})
            opener = urllib2.build_opener(proxy_handler)
            opener.addheaders = [('User-agent', ua.get_user_agent() )]
            urllib2.install_opener(opener)
            req = urllib2.Request(url)
            data = urllib2.urlopen(req).read()
            regex = "(?P<url>https?://[^:]+\.%s)" % extension
            data = re.findall(regex, data)
            list_files_download = list(set(data))
            total_files = str(len(list_files_download))
            log.console_log(Y + "[*] Found " + total_files + " " + extension.upper() + " files!" + W )
            if total_files != "0":
                log.console_log(G + "[*] Please wait, lemme download it for you ;) [NO PROXY] " + W)
                for files_download in list_files_download:
                    log.no_console_log(files_download.split('/')[-1])
                    self.download_files(files_download, domain)
        except urllib2.URLError, e:
            log.console_log(e)

    def download_files(self, url, folder_domain):
        filename = url.split('/')[-1]
        full_filename = 'belatiFiles/{}/{}'.format(folder_domain, filename)
        if not os.path.exists(os.path.dirname(full_filename)):
            try:
                os.makedirs(os.path.dirname(full_filename))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

        with tqdm(unit='B', unit_scale=True, miniters=1,desc=filename) as t:
            urllib.urlretrieve(url, filename=full_filename,reporthook=self.my_hook(t), data=None)

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
    HarvestPublicDocumentApp = HarvestPublicDocument()
    HarvestPublicDocumentApp
