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
import urllib
from logger import Logger
from tqdm import tqdm
import requests
from url_request import URLRequest

# Console color
G = '\033[92m'  # green
Y = '\033[93m'  # yellow
B = '\033[94m'  # blue
R = '\033[91m'  # red
W = '\033[0m'   # white

url_req = URLRequest()
log = Logger()

class HarvestPublicDocument(object):
    def init_crawl(self, domain, proxy_address):
        log.console_log("{}[*] Gather Link from Google Search for domain {}{}".format(G, domain, W))
        self.harvest_public_doc(domain, "pdf", proxy_address)
        self.harvest_public_doc(domain, "doc", proxy_address)
        self.harvest_public_doc(domain, "xls", proxy_address)
        self.harvest_public_doc(domain, "odt", proxy_address)
        self.harvest_public_doc(domain, "ppt", proxy_address)
        self.harvest_public_doc(domain, "rtf", proxy_address)
        self.harvest_public_doc(domain, "txt", proxy_address)
        #https://www.google.com/search?q=site:domain.com%20ext:pdf&filter=0&num=100#q=site:domain.com+ext:txt&start=100&filter=0

    def harvest_public_doc(self, domain, extension, proxy_address):
        log.console_log("{}[*] Searching {} Document... {}".format(G, extension.upper(), W))
        total_files = 0
        url = 'https://www.google.com/search?q=site:' + domain + '%20ext:' + extension + '&filter=0&num=200'
        data = data = url_req.standart_request(url, proxy_address)
        regex = "(?P<url>https?://[^:]+\.%s)" % extension
        data = re.findall(regex, data)
        list_files_download = list(set(data))
        total_files = str(len(list_files_download))
        log.console_log("{}[*] Found {} {} files!".format(G, total_files, extension.upper(), W) )
        if total_files != "0":
            log.console_log("{}[*] Please wait, lemme download it for you ;) {}[NO PROXY] {}".format(G, Y, W))
            for files_download in list_files_download:
                log.no_console_log(files_download.split('/')[-1])
                self.download_files(files_download, domain)

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
            try:
                urllib.urlretrieve(url, filename=full_filename,reporthook=self.my_hook(t), data=None)
            except:
                pass

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
