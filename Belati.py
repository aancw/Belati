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


# We need to check Dependency first
from plugins.dep_check import DepCheck

dep_check = DepCheck()
dep_check.check_dependency()

import argparse
import datetime
import urllib2
import sys, signal, socket, re
import time
import dns.resolver
import tldextract

from plugins.about_project import AboutProject
from plugins.banner_grab import BannerGrab
from plugins.check_domain import CheckDomain
from plugins.config import Config
from plugins.common_service_check import CommonServiceCheck
from plugins.database import Database
from plugins.gather_company import GatherCompany
from plugins.git_finder import GitFinder
from plugins.harvest_email import HarvestEmail
from plugins.harvest_public_document import HarvestPublicDocument
from plugins.logger import Logger
from plugins.robots_scraper import RobotsScraper
from plugins.scan_nmap import ScanNmap
from plugins.svn_finder import SVNFinder
from plugins.url_request import URLRequest
from plugins.wappalyzer import Wappalyzer

from lib.Sublist3r import sublist3r
from lib.CheckMyUsername.check_my_username import CheckMyUsername
from dnsknife.scanner import Scanner
from urlparse import urlparse

# Console color
G = '\033[92m'  # green
Y = '\033[93m'  # yellow
B = '\033[94m'  # blue
R = '\033[91m'  # red
W = '\033[0m'   # white

log = Logger()

class Belati(object):
    def __init__(self):
        self.about = AboutProject()
        self.url_req = URLRequest()

        # Passing arguments
        parser = argparse.ArgumentParser(description='=[ {} {} by {}] ({})'.format(self.about.__name__, self.about.__version__, self.about.__author__, self.about.__giturl__))
        parser.add_argument('-d', action='store', dest='domain' , help='Perform OSINT from Domain e.g petruknisme.com(without protocol http/https)')
        parser.add_argument('-u', action='store', dest='username' , help='Perform OSINT from username e.g petruknisme')
        parser.add_argument('-e', action='store', dest='email' , help='Perform OSINT from email address')
        parser.add_argument('-c', action='store', dest='orgcomp' , help='Perform OSINT from Organization or Company Name, use double quote')
        parser.add_argument('-o', action='store', dest='output_files' , help='Save log for output files')
        parser.add_argument('--db-file', action='store', dest='db_file_location' , help='Specify Database File Location(SQLite3)')
        parser.add_argument('--single-proxy', action='store', dest='single_proxy', help='Proxy support with single IP (ex: http://127.0.0.1:8080)' )
        parser.add_argument('--proxy-file', action='store', dest='proxy_file_location', help='Proxy support from Proxy List File')
        parser.add_argument('--auto-proxy', action='store_true', dest='auto_proxy', default=True, help='Auto Proxy Support( Coming soon )' )
        parser.add_argument('--version', action='version', version='=[ {} {} by {}] ({})'.format(self.about.__name__, self.about.__version__, self.about.__author__, self.about.__giturl__))
        results = parser.parse_args()

        domain = results.domain
        username = results.username
        email = results.email
        orgcomp = results.orgcomp
        single_proxy = results.single_proxy
        proxy_file_location = results.proxy_file_location
        proxy = ""
        self.multiple_proxy_list = []

        self.show_banner()

        conf = Config()
        self.db = Database()

        # Setup project
        self.project_id = self.db.create_new_project(domain, orgcomp, datetime.datetime.now())
        log.console_log("{}[+] Creating New Belati Project... {}".format(G, W))
        log.console_log("---------------------------------------------------------")
        log.console_log("Project ID: {}".format(str(self.project_id)))
        log.console_log("Project Domain: {}".format(domain))
        log.console_log("Project Organization/Company: {}".format(orgcomp))
        log.console_log("---------------------------------------------------------")

        if domain is not None:
            if single_proxy is not None:
                log.console_log("{}[*] Checking Proxy Status... {}".format(G, W))
                if self.check_single_proxy_status(single_proxy, "http://" + str(domain)) == 'ok':
                    proxy = single_proxy
                else:
                    log.console_log('{}[-] Please use another proxy or disable proxy! {}'.format(R, W))
                    sys.exit()

            if proxy_file_location is not None:
                log.console_log("{}[*] Checking Proxy Status from file {}{}".format(G, proxy_file_location, W))
                self.check_multiple_proxy_status(proxy_file_location, "http://" + str(domain))
                proxy = self.multiple_proxy_list

            extract_domain = tldextract.extract(domain)

            self.check_domain(self.url_req.ssl_checker(domain), proxy)
            self.banner_grab(self.url_req.ssl_checker(domain), proxy)

            if extract_domain.subdomain == "":
                self.robots_scraper(self.url_req.ssl_checker(domain), proxy)
                self.enumerate_subdomains(domain, proxy)
                self.scan_DNS_zone(domain)
                self.harvest_email_search(domain, proxy)
                self.harvest_email_pgp(domain, proxy)
            else:
                domain = extract_domain.domain + '.' + extract_domain.suffix
                self.robots_scraper(self.url_req.ssl_checker(domain), proxy)
                self.enumerate_subdomains(domain, proxy)
                self.scan_DNS_zone(domain)
                self.harvest_email_search(domain, proxy)
                self.harvest_email_pgp(domain, proxy)

            self.harvest_document(domain, proxy)

        if username is not None:
            self.username_checker(username)

        if orgcomp is not None:
            self.gather_company(orgcomp, proxy)

        if email is not None:
            log.console_log("This feature will be coming soon. Be patient :)")

        log.console_log("{}All done sir! All log saved in log directory and dowloaded file saved in belatiFiles {}".format(Y, W))

    def show_banner(self):
        banner = """
        {}
         /$$$$$$$  /$$$$$$$$ /$$        /$$$$$$  /$$$$$$$$ /$$$$$$
        | $$__  $$| $$_____/| $$       /$$__  $$|__  $$__/|_  $$_/
        | $$  \ $$| $$      | $$      | $$  \ $$   | $$     | $$
        | $$$$$$$ | $$$$$   | $$      | $$$$$$$$   | $$     | $$
        | $$__  $$| $$__/   | $$      | $$__  $$   | $$     | $$
        | $$  \ $$| $$      | $$      | $$  | $$   | $$     | $$
        | $$$$$$$/| $$$$$$$$| $$$$$$$$| $$  | $$   | $$    /$$$$$$
        |_______/ |________/|________/|__/  |__/   |__/   |______/

                                The Traditional Swiss Army Knife for OSINT

        =[ {} {} by {}]=

        + -- --=[ {} ]=-- -- +
        + -- --=[ {} ]=-- -- +
        {}
        """

        warning_message = """
        {}
        This tool is for educational purposes only.
        Any damage you make will not affect the author.
        Do It With Your Own Risk!

        For Better Privacy, Please Use proxychains or other proxy service!
        {}
        """

        log.console_log(banner.format(G, self.about.__name__, self.about.__version__, self.about.__author__, self.about.__info__, self.about.__authorurl__, W))
        log.console_log(warning_message.format(R, W))

    def check_domain(self, domain_name, proxy_address):
        check = CheckDomain()

        log.console_log(G + "{}[*] Checking Domain Availability... {}".format(G, W) , 0)
        check.domain_checker(domain_name, proxy_address)
        log.console_log("{}[*] Checking URL Alive... {}".format(G, W), 0)
        check.alive_check(domain_name, proxy_address)
        log.console_log("{}[*] Perfoming Whois... {}".format(G, W))
        whois_result = check.whois_domain(domain_name)
        email = re.findall(r'[a-zA-Z0-9._+-]+@[a-zA-Z0-9._+-]+\s*', str(whois_result))
        self.db.insert_domain_result(self.project_id, self.strip_scheme(domain_name), str(whois_result), str(email) )


    def banner_grab(self, domain_name, proxy_address):
        banner = BannerGrab()
        log.console_log("{}[*] Perfoming HTTP Banner Grabbing... {}".format(G, W))
        banner_info = banner.show_banner(domain_name, proxy_address)
        self.db.insert_banner(domain_name, self.project_id, str(banner_info))

    def enumerate_subdomains(self, domain_name, proxy):
        log.console_log("{}[*] Perfoming Subdomains Enumeration... {}".format(G, W))
        subdomain_list = sublist3r.main(domain_name, 100, "", ports=None, silent=False, verbose=False, enable_bruteforce=False, engines=None)
        subdomain_ip_list = []

        for subdomain in subdomain_list:
            self.banner_grab(self.url_req.ssl_checker(subdomain), proxy)
            self.robots_scraper(self.url_req.ssl_checker(subdomain), proxy)
            self.wappalyzing_webpage(subdomain)
            self.public_git_finder(subdomain, proxy)
            self.public_svn_finder(subdomain, proxy)
            try:
                subdomain_ip_list.append(socket.gethostbyname(subdomain))
                self.db.update_subdomain_ip(self.project_id, subdomain, str(socket.gethostbyname(subdomain)))
            except socket.gaierror:
                pass

        subdomain_ip_listFix = list(set(subdomain_ip_list))

        # check common service port TODO
        #for ipaddress in subdomain_ip_listFix:
            #self.common_service_check(ipaddress)

        for ipaddress in subdomain_ip_listFix:
            self.service_scanning(ipaddress)

    def wappalyzing_webpage(self, domain):
        log.console_log("{}[*] Wapplyzing on domain {}{}".format(G, domain, W))
        wappalyzing = Wappalyzer()
        targeturl = self.url_req.ssl_checker(domain)
        try:
            data = wappalyzing.run_wappalyze(targeturl)
            self.db.insert_wappalyzing(self.project_id, domain, data)
        except urllib2.URLError as exc:
            log.console_log('URL Error: {0}'.format(str(exc)))
        except urllib2.HTTPError as exc:
            log.console_log('HTTP Error: {0}'.format(str(exc)))
        except Exception as exc:
            log.console_log('Unknow error: {0}'.format(str(exc)))

    def service_scanning(self, ipaddress):
        scan_nm = ScanNmap()
        log.console_log("{}[*] Perfoming Nmap Full Scan on IP {}{}".format(G, ipaddress, W))
        log.console_log("{}[*] nmap -sS -A -Pn {}{}".format(G, ipaddress, W))
        scan_nm.run_scanning(ipaddress)

    def scan_DNS_zone(self, domain_name):
        log.console_log("{}[*] Perfoming DNS Zone Scanning... {}".format(G, W))
        log.console_log("{}[*] Please wait, maximum timeout for checking is 1 minutes {}".format(G, W))
        signal.signal(signal.SIGALRM, self.timeLimitHandler)
        signal.alarm(60)
        try:
            scan_list = str(list(Scanner(domain_name).scan()))
            ns_record_list = []
            mx_record_list = []
            log.console_log("{}{}{}".format(G, scan_list.replace(",","\n"), W))
            log.console_log("{}DNS Server:{}".format(G, W))
            for ns in dns.resolver.query(domain_name, 'NS'):
                log.console_log(G + ns.to_text() + W)
                ns_record_list.append(ns.to_text())

            log.console_log("{}MX Record:{}".format(G, W))
            for ns in dns.resolver.query(domain_name, 'MX'):
                log.console_log("{}{}{}".format(G, ns.to_text(), W))
                mx_record_list.append(ns.to_text())

            self.db.update_dns_zone(self.project_id, domain_name, str(ns_record_list), str(mx_record_list))

        except Exception, exc:
            print("{}[*] No response from server... SKIP!{}".format(R, W))

    def harvest_email_search(self, domain_name, proxy_address):
        log.console_log("{}[*] Perfoming Email Harvest from Google Search...{}".format(G, W) )
        harvest = HarvestEmail()
        harvest_result = harvest.crawl_search(domain_name, proxy_address)
        try:
            log.console_log("{}[*] Found {} emails on domain {}{}".format(Y, str(len(harvest_result)), domain_name, W))
            log.console_log("{}{}{}".format(R, '\n'.join(harvest_result), W))
        except Exception, exc:
            log.console_log("{}[-] Not found or Unavailable. {}{}".format(R, str(harvest_result), W ))

        self.db.insert_email_result(self.project_id, str(harvest_result))

    def harvest_email_pgp(self, domain_name, proxy_address):
        harvest = HarvestEmail()
        harvest_result = harvest.crawl_pgp_mit_edu(domain_name, proxy_address)
        try:
            log.console_log("{}[*] Found {} emails on domain {}{}".format(Y, str(len(harvest_result)), domain_name, W))
            log.console_log("{}{}{}".format(R, '\n'.join(harvest_result), W))
        except Exception, exc:
            log.console_log("{}[-] Not found or Unavailable. {}{}".format(R, str(harvest_result), W ))

        self.db.update_pgp_email(self.project_id, str(harvest_result))

    def harvest_document(self, domain_name, proxy_address):
        log.console_log("{}[*] Perfoming Public Document Harvest from Google... {}".format(G, W))
        public_doc = HarvestPublicDocument()
        public_doc.init_crawl(domain_name, proxy_address, self.project_id)

    def username_checker(self, username):
        log.console_log("{}[*] Perfoming Username Availability Checker... {}".format(G, W))
        user_check = CheckMyUsername()
        username_status_result = user_check.check_username_availability(username)

        for result in username_status_result:
            log.console_log(G + "[+] " + result[0] + " => " + result[1] + ": " + result[2])

    def check_single_proxy_status(self, proxy_address, domain_check):
        try:
            parse = urlparse(proxy_address)
            proxy_scheme = parse.scheme
            proxy = str(parse.hostname) + ':' + str(parse.port)
            proxy_handler = urllib2.ProxyHandler({ proxy_scheme: proxy})
            opener = urllib2.build_opener(proxy_handler)
            opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36')]
            urllib2.install_opener(opener)
            req = urllib2.Request(domain_check)
            start_time = time.time()
            sock = urllib2.urlopen(req)
            end_time = time.time()
            diff_time = round(end_time - start_time, 3)
            log.console_log(Y + "{}[+] {} OK! Response Time : {}s".format(Y, proxy_address, str(diff_time), W ))
            return 'ok'
        except urllib2.HTTPError, e:
            print('Error code: ' + str(e.code))
            return e.code
        except Exception, detail:
            print('ERROR ' +  str(detail))
            return 1

    def check_multiple_proxy_status(self, file_location, domain_check):
        with open(file_location) as data:
            text = [line.rstrip('\n') for line in data]
            for proxy in text:
                if self.check_single_proxy_status(str(proxy), str(domain_check)) == 'ok':
                     self.multiple_proxy_list.append(proxy)

    def public_git_finder(self, domain, proxy_address):
        log.console_log("{}[*] Checking Public GIT Directory on domain {}{}".format(G, domain, W))
        git_finder = GitFinder()
        if git_finder.check_git(domain, proxy_address) == True:
            log.console_log("{}[+] Gotcha! You are in luck, boy![{}/.git/]{}".format(Y, domain, W))
            self.db.update_git_finder(self.project_id, domain, "Yes")

    def public_svn_finder(self, domain, proxy_address):
        log.console_log("{}[*] Checking Public SVN Directory on domain {}{}".format(G, domain, W))
        svn_finder = SVNFinder()
        if svn_finder.check_svn(domain, proxy_address) == 403:
            log.console_log("{}[+] Um... Forbidden :( {}".format(Y, W))
        if svn_finder.check_svn(domain, proxy_address) == 200:
            log.console_log("{}[+] Gotcha! You are in luck, boy![{}/.svn/]{}".format(Y, domain, W))
            self.db.update_svn_finder(self.project_id, domain, "Yes")

    def robots_scraper(self, domain, proxy_address):
        scraper = RobotsScraper()
        data = scraper.check_robots(domain, proxy_address)
        if data is not None and isinstance(data, int) == False and data.code == 200:
            log.console_log("{}[+] Found interesting robots.txt[ {} ] =>{}".format(Y, domain, W))
            log.console_log(data.read())
            self.db.insert_robots_txt(self.project_id, domain, str(data.read()))

    def gather_company(self, company_name, proxy_address):
        log.console_log("{}[+] Gathering Company Employee {} -> {}".format(G, W, company_name))
        gather_company = GatherCompany()
        gather_company.crawl_company_employee(company_name, proxy_address, self.project_id)

    def check_update(self, version):
        log.console_log("{} Checking Version Update for Belati... {}".format(G, W))
        # TODO


    def common_service_check(self, host):
        log.console_log("{}[*] Checking Common Service Check on host {}{}".format(G, host, W))
        service_check = CommonServiceCheck()
        service_check.check_available_service(host)

    def check_python_version(self):
        if sys.version[:3] == "2.7" or "2" in sys.version[:3]:
            log.console_log("{}[*] Python version OK! {}{}".format(G, sys.version[:6], W))
        elif "3" in sys.version[:3]:
            log.console_log("{}[-] Nope. This system not yet compatible for Python 3!{}".format(Y, W))
            sys.exit()
        else:
            log.console_log("{}[-] Duh. Your python version too old for running this :({}".format(Y, W))
            sys.exit()

    def timeLimitHandler(self, signum, frame):
        print("No Response...")

    def strip_scheme(self, url):
        parsed = urlparse(url)
        scheme = "%s://" % parsed.scheme
        return parsed.geturl().replace(scheme, '', 1)

if __name__ == '__main__':
    BelatiApp = Belati()
    BelatiApp
