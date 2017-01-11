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
from plugins.check_domain import CheckDomain
from plugins.banner_grab import BannerGrab
from plugins.logger import Logger
from plugins.harvest_email import HarvestEmail
from plugins.harvest_public_document import HarvestPublicDocument
from plugins.scan_nmap import ScanNmap
from plugins.wappalyzer import Wappalyzer
from lib.Sublist3r import sublist3r
from dnsknife.scanner import Scanner
import dns.resolver


# Console color
G = '\033[92m'  # green
Y = '\033[93m'  # yellow
B = '\033[94m'  # blue
R = '\033[91m'  # red
W = '\033[0m'   # white

log = Logger()

class Belati(object):
    def __init__(self):
        # Passing arguments
        parser = argparse.ArgumentParser(description='=[ Belati v0.1-dev by Petruknisme]')
        parser.add_argument('-d', action='store', dest='domain' , help='Perform OSINT from Domain e.g petruknisme.com')
        parser.add_argument('-u', action='store', dest='username' , help='Perform OSINT from username e.g petruknisme')
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
            self.show_banner()
            #self.check_domain("http://" + domain)
            #self.banner_grab("http://" + domain)
            #self.enumerate_subdomains(domain)
            #self.scan_DNS_zone(domain)
            #self.harvest_email_search(domain)
            self.harvest_document(domain)

        if username or email or orgcomp is not None:
            log.console_log("This feature will be coming soon. Be patient :)")

        log.console_log(Y + "All done sir! All log saved in log directory and dowloaded file saved in belatiFiles" + W)

    def show_banner(self):
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

        warning_message = """

        This tool is for educational purposes only.
        Any damage you make will not affect the author.
        Do It With Your Own Risk!.

        For Better Privacy, Please Use proxychains or other proxy service!
        """

        log.console_log(G + banner + W)
        log.console_log(R + warning_message + W)

    def check_domain(self, domain_name):
        check = CheckDomain()

        log.console_log(G + "[*] Checking Domain Availability.... " + W, 0)
        check.domain_checker(domain_name)
        log.console_log(G + "[*] Checking URL Alive... " + W, 0)
        check.alive_check(domain_name)
        log.console_log(G + "[*] Perfoming Whois... " + W)
        check.whois_domain(domain_name)

    def banner_grab(self, domain_name):
        banner = BannerGrab()
        log.console_log(G + "[*] Perfoming HTTP Banner Grabbing..." + W)
        banner.show_banner(domain_name)

    def enumerate_subdomains(self, domain_name):
        log.console_log(G + "[*] Perfoming Subdomains Enumeration..." + W)
        subdomain_list = sublist3r.main(domain_name, 100, "", ports=None, silent=False, verbose=False, enable_bruteforce=False, engines=None)
        subdomain_ip_list = []

        log.console_log(G + "[*] Perfoming Wapplyzing Web Page..." + W)
        for subdomain in subdomain_list:
            self.wapplyzing_webpage(subdomain)
            try:
                subdomain_ip_list.append(socket.gethostbyname(subdomain))
            except socket.gaierror:
                pass

        subdomain_ip_listFix = list(set(subdomain_ip_list))

        for ipaddress in subdomain_ip_listFix:
            self.service_scanning(ipaddress)

    def wapplyzing_webpage(self, domain):
        wappalyzing = Wappalyzer()
        log.console_log(G + "[*] Wapplyzing HTTP on domain " + domain + W)
        try:
            targeturl = "http://" + domain
            wappalyzing.run_wappalyze(targeturl)
        except:
            log.console_log(R + "[-] HTTP connection was unavailable" + W)

        log.console_log(G + "[*] Wapplyzing HTTPS on domain " + domain + W)
        try:
            targeturl = "https://" + domain
            wappalyzing.run_wappalyze(targeturl)
        except:
            log.console_log(R + "[-] HTTPS connection was unavailable" + W)

    def service_scanning(self, ipaddress):
        scan_nm = ScanNmap()
        log.console_log(G + "[*] Perfoming Nmap Full Scan on IP " + ipaddress + W)
        log.console_log(G + "[*] nmap -sS -A -Pn " + ipaddress + W)
        scan_nm.run_scanning(ipaddress)

    def scan_DNS_zone(self, domain_name):
        log.console_log(G + "[*] Perfoming DNS Zone Scanning..." + W)
        log.console_log(G + "[*] Please wait, maximum timeout for checking is 1 minutes")
        signal.signal(signal.SIGALRM, self.timeLimitHandler)
        signal.alarm(60)
        try:
            scan_list = str(list(Scanner(domain_name).scan()))
            log.console_log(G + scan_list.replace(",","\n") + W)
            log.console_log(G + "DNS Server:" + W)
            for ns in dns.resolver.query(domain_name, 'NS'):
                log.console_log(G + ns.to_text() + W)
            log.console_log(G + "MX Record:" + W)
            for ns in dns.resolver.query(domain_name, 'MX'):
                log.console_log(G + ns.to_text() + W)
        except Exception, exc:
            print(R + "[*] No response from server... SKIP!" + W)

    def harvest_email_search(self, domain_name):
        log.console_log(G + "[*] Perfoming Email Harvest from Google Search..." + W)
        harvest = HarvestEmail()
        harvest_result = harvest.crawl_search(domain_name)
        log.console_log(Y + "[*] Found " + str(len(harvest_result)) + " emails on domain " + domain_name + W)
        log.console_log(R + '\n'.join(harvest_result) + W)

    def harvest_document(self, domain_name):
        log.console_log(G + "[*] Perfoming Public Document Harvest from Google..." +  W)
        public_doc = HarvestPublicDocument()
        public_doc.init_crawl(domain_name)

    def timeLimitHandler(self, signum, frame):
        print("No Response...")

if __name__ == '__main__':
    BelatiApp = Belati()
    BelatiApp
