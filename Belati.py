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

import argparse
import urllib2
import sys, signal, socket
from plugins.checkDomain import checkDomain
from plugins.bannerGrab import bannerGrab
from plugins.logger import logger
from plugins.harvestEmail import harvestEmail
from plugins.harvestPublicDocument import harvestPublicDocument
from plugins.scanNmap import scanNmap
from plugins.wappalyzer import wappalyzer
from lib.Sublist3r import sublist3r
from dnsknife.scanner import Scanner
import dns.resolver


# Console color
G = '\033[92m'  # green
Y = '\033[93m'  # yellow
B = '\033[94m'  # blue
R = '\033[91m'  # red
W = '\033[0m'   # white

log = logger()

class Belati(object):
    def __init__(self):
        # Passing arguments
        parser = argparse.ArgumentParser(description='=[ Belati v0.1-dev by Petruknisme]')
        parser.add_argument('-d', action='store', dest='domain' , help='Perform OSINT from Domain')
        parser.add_argument('-u', action='store', dest='username' , help='Perform OSINT from username')
        parser.add_argument('-e', action='store', dest='email' , help='Perform OSINT from email address')
        parser.add_argument('-c', action='store', dest='orgcomp' , help='Perform OSINT from Organization or Company Name')
        parser.add_argument('-o', action='store', dest='output_files' , help='Save log for output files')
        parser.add_argument('--version', action='version', version='=[ Belati v0.1-dev by Petruknisme]')
        results = parser.parse_args()

        domain = results.domain
        username = results.username
        email = results.email
        orgcomp = results.orgcomp

        if domain is not None:
            self.showBanner()
            self.checkDomain("http://" + domain)
            self.bannerGrab("http://" + domain)
            self.enumerateSubdomains(domain)
            self.scanDNSZone(domain)
            self.harvestEmailSearch(domain)
            self.harvestDocument(domain)

        if username or email or orgcomp is not None:
            log.consoleLog("This feature will be coming soon. Be patient :)")

        log.consoleLog(Y + "All done sir! All log saved in log directory and dowloaded file saved in belatiFiles" + W)

    def showBanner(self):
        banner = """
         ____  _____ _        _  _____ ___
        | __ )| ____| |      / \|_   _|_ _|
        |  _ \|  _| | |     / _ \ | |  | |
        | |_) | |___| |___ / ___ \| |  | |
        |____/|_____|_____/_/   \_\_| |___|


        =[ Belati v0.1-dev by Petruknisme]=

        + -- --=[ Collecting Public Data & Public Document for OSINT purpose ]=-- -- +
        + -- --=[ https://petruknisme.com ]=-- -- +

        """

        warningMessage = """

        This tool is for educational purposes only.
        Any damage you make will not affect the author.
        Do It With Your Own Risk!.

        For Better Privacy, Please Use proxychains or other proxy service!
        """

        log.consoleLog(G + banner + W)
        log.consoleLog(R + warningMessage + W)

    def checkDomain(self, domainName):
        check = checkDomain()

        log.consoleLog(G + "[*] Checking Domain Availability.... " + W, 0)
        check.domainChecker(domainName)
        log.consoleLog(G + "[*] Checking URL Alive... " + W, 0)
        check.aliveCheck(domainName)
        log.consoleLog(G + "[*] Perfoming Whois... " + W)
        check.whoisDomain(domainName)

    def bannerGrab(self, domainName):
        banner = bannerGrab()
        log.consoleLog(G + "[*] Perfoming HTTP Banner Grabbing..." + W)
        banner.showBanner(domainName)

    def enumerateSubdomains(self, domainName):
        log.consoleLog(G + "[*] Perfoming Subdomains Enumeration..." + W)
        subdomain_list = sublist3r.main(domainName, 100, "", ports=None, silent=False, verbose=False, enable_bruteforce=False, engines=None)
        subdomain_ip_list = []

        log.consoleLog(G + "[*] Perfoming Wapplyzing Web Page..." + W)
        for subdomain in subdomain_list:
            self.wapplyzingWebPage(subdomain)
            try:
                subdomain_ip_list.append(socket.gethostbyname(subdomain))
            except socket.gaierror:
                pass

        subdomain_ip_listFix = list(set(subdomain_ip_list))

        for ipaddress in subdomain_ip_listFix:
            self.serviceScanning(ipaddress)

    def wapplyzingWebPage(self, domain):
        wappalyzing = wappalyzer()
        log.consoleLog(G + "[*] Wapplyzing HTTP on domain " + domain + W)
        try:
            targeturl = "http://" + domain
            wappalyzing.run_wappalyze(targeturl)
        except:
            log.consoleLog(R + "[-] HTTP connection was unavailable" + W)

        log.consoleLog(G + "[*] Wapplyzing HTTPS on domain " + domain + W)
        try:
            targeturl = "https://" + domain
            wappalyzing.run_wappalyze(targeturl)
        except:
            log.consoleLog(R + "[-] HTTPS connection was unavailable" + W)

    def serviceScanning(self, ipaddress):
        scanNm = scanNmap()
        log.consoleLog(G + "[*] Perfoming Nmap Full Scan on IP " + ipaddress + W)
        log.consoleLog(G + "[*] nmap -sS -A -Pn " + ipaddress + W)
        scanNm.runScanning(ipaddress)

    def scanDNSZone(self, domainName):
        log.consoleLog(G + "[*] Perfoming DNS Zone Scanning..." + W)
        log.consoleLog(G + "[*] Please wait, maximum timeout for checking is 1 minutes")
        signal.signal(signal.SIGALRM, self.timeLimitHandler)
        signal.alarm(60)
        try:
            scanList = str(list(Scanner(domainName).scan()))
            log.consoleLog(G + scanList.replace(",","\n") + W)
            log.consoleLog(G + "DNS Server:" + W)
            for ns in dns.resolver.query(domainName, 'NS'):
                log.consoleLog(G + ns.to_text() + W)
            log.consoleLog(G + "MX Record:" + W)
            for ns in dns.resolver.query(domainName, 'MX'):
                log.consoleLog(G + ns.to_text() + W)
        except Exception, exc:
            print(R + "[*] No response from server... SKIP!" + W)

    def harvestEmailSearch(self, domainName):
        log.consoleLog(G + "[*] Perfoming Email Harvest from Google Search..." + W)
        harvest = harvestEmail()
        harvestResult = harvest.crawlSearch(domainName)
        log.consoleLog(Y + "[*] Found " + str(len(harvestResult)) + " emails on domain " + domainName + W)
        log.consoleLog(R + '\n'.join(harvestResult) + W)

    def harvestDocument(self, domainName):
        log.consoleLog(G + "[*] Perfoming Public Document Harvest from Google..." +  W)
        publicDoc = harvestPublicDocument()
        publicDoc.init_crawl(domainName)

    def timeLimitHandler(self, signum, frame):
        print("No Response...")

if __name__ == '__main__':
    BelatiApp = Belati()
    BelatiApp
