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
import shlex, subprocess

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
from plugins.json_beautifier import JsonBeautifier
from plugins.logger import Logger
from plugins.meta_exif_extractor import MetaExifExtractor
from plugins.robots_scraper import RobotsScraper
from plugins.scan_nmap import ScanNmap
from plugins.subdomain_enum import SubdomainEnum
from plugins.svn_finder import SVNFinder
from plugins.updater import Updater
from plugins.url_request import URLRequest
from plugins.util import Util
from plugins.wappalyzer import Wappalyzer

from lib.CheckMyUsername.check_my_username import CheckMyUsername
from dnsknife.scanner import Scanner
from urlparse import urlparse

from cmd2 import Cmd
from tabulate import tabulate
from texttable import Texttable

# Console color
G = '\033[92m'  # green
Y = '\033[93m'  # yellow
B = '\033[94m'  # blue
R = '\033[91m'  # red
W = '\033[0m'   # white
UNDERLINE = '\033[4m'
ENDC = '\033[0m'

log = Logger()
util = Util()

class Belati(Cmd):
    def __init__(self):
        self.about = AboutProject()
        self.url_req = URLRequest()

        Cmd.doc_header = "Core Commands"
        Cmd.prompt = "{}belati{} > ".format(UNDERLINE, ENDC)
        Cmd.path_complete

        Cmd.__init__(self)

        self.list_parameter = ['domain', 'username', 'email', 'orgcomp', 'proxy', 'proxy_file']
        self.parameters = {}
        self.multiple_proxy_list = []
        self.current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        self.show_banner()
        self.conf = Config()
        self.db = Database()


    def show_banner(self):
        banner = """
        {}

         /$$$$$$$  /$$$$$$$$ /$$        /$$$$$$  /$$$$$$$$     .
        | $$__  $$| $$_____/| $$       /$$__  $$|__  $$__/    J:L
        | $$  \ $$| $$      | $$      | $$  \ $$   | $$       |:|
        | $$$$$$$ | $$$$$   | $$      | $$$$$$$$   | $$       |:|
        | $$__  $$| $$__/   | $$      | $$__  $$   | $$       |:|
        | $$  \ $$| $$      | $$      | $$  | $$   | $$       |:|
        | $$$$$$$/| $$$$$$$$| $$$$$$$$| $$  | $$   | $$   /]  |:|  [\ 
        |_______/ |________/|________/|__/  |__/   |__/   \:-'\"""'-:/
                                                            ""III""
                                                              III
                                                              III
                                                              III
                                                             (___)

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

    def do_help(self, line):
    	'print help message'

    	print("\nCore commands")
    	print("==============\n")
    	print tabulate([["Name","Description"],
    		["?", "Help menu"],
    		["!", "Run OS Command"],
    		["history", "Show command history"],
    		["set", "Set parameters option value"],
    		["show", "Display list available parameter option"],
    		["start", "Start Automatic Scanning Belati"],
    		["startws", "Start Web Server Only Mode"],
    		["version", "Show application version number"],
    		["quit", "Exit the application"]],
			headers="firstrow")


    def do_set(self, arg, opts=None):
    	'''Set Variable for Belati parameters.\nUsage: set [option] [value]\n\nAvailable options:\ndomain, username, email, orgcomp, proxy, proxy_file'''

    	if not arg:
    		log.console_log('{} Set Variable for Belati parameters.\nUsage: set [option] [value]\n\nAvailable options:\ndomain, username, email, orgcomp, proxy, proxy_file {}'.format(W, W))
    	else:
            param = shlex.split(arg)
            key = param[0]
            value = param[1]
            if key in self.list_parameter:
                self.parameters[key] = value
                log.console_log('{} => {}'.format(self.parameters[key], value))
            else:
                log.console_log("Available parameters: domain, username, email, orgcomp, proxy, proxy_file")

    def do_show(self, arg, opts=None):
    	'Show available parameter options'
    	
    	domain_val = self.parameters['domain'] if 'domain' in self.parameters else None
    	orgcomp = self.parameters['orgcomp'] if 'orgcomp' in self.parameters else None
     	email = self.parameters['email'] if 'email' in self.parameters else None
     	username = self.parameters['username'] if 'username' in self.parameters else None
     	proxy = self.parameters['proxy'] if 'proxy' in self.parameters else None
     	proxy_file = self.parameters['proxy_file'] if 'proxy_file' in self.parameters else None
     	org_val = ""
    	arg = shlex.split(arg)

    	if not arg:
    		print("Please use command 'show options' to see list of option parameters")

    	elif arg[0] == "options":
            print tabulate([["Name","Value", "Required", "Description"],
    			["domain", domain_val, "Yes", "Domain name for OSINT"],
    			["orgcomp", orgcomp, "Yes", "Organization/Company name for OSINT"],
    			["email", email, "Optional", "Email address for OSINT"],
    			["username", username, "Optional", "Username for OSINT"],
    			["proxy", proxy, "Optional", "Proxy server(e.g http://127.0.0.1:8080)"],
    			["proxy_file", proxy_file, "Optional", "Proxy file list location"]],
    			headers="firstrow")

    def do_startws(self, line):
    	'Start Belati in Web Server Only Mode'
    	
    	log.console_log("{}[*] Entering Web Server Only Mode...{}".format(Y,W))
    	self.start_web_server()
    	sys.exit()

    def do_version(self, line):
    	'Check current Belati version'
    	
    	log.console_log('{} {} by {}\n'.format(self.about.__name__, self.about.__version__, self.about.__author__))
    	log.console_log('Project URL: {}'.format(self.about.__giturl__))

    def do_start(self, line):
    	'Start automatic scanning'
    	domain = self.parameters['domain'] if 'domain' in self.parameters else None
    	orgcomp = self.parameters['orgcomp'] if 'orgcomp' in self.parameters else None
     	email = self.parameters['email'] if 'email' in self.parameters else None
     	username = self.parameters['username'] if 'username' in self.parameters else None
     	proxy = self.parameters['proxy'] if 'proxy' in self.parameters else ''
     	proxy_file = self.parameters['proxy_file'] if 'proxy_file' in self.parameters else ''

    	if domain is None and orgcomp is None:
    		log.console_log("{}[-] Please specify domain/organization {}".format(R,W))
    		sys.exit()
			
		log.console_log("{}[*] Starting at: {} {}".format(Y, self.current_time , W))

        self.updater = Updater()
        self.updater.check_update(self.about.__version__)

        # Setup project
        self.project_id = self.db.create_new_project(domain, orgcomp, self.current_time)
        log.console_log("{}[+] Creating New Belati Project... {}".format(G, W))
        log.console_log("---------------------------------------------------------")
        log.console_log("Project ID: {}".format(str(self.project_id)))
        log.console_log("Project Domain: {}".format(domain))
        log.console_log("Project Organization/Company: {}".format(orgcomp))
        log.console_log("---------------------------------------------------------")

        if domain is not None:
            if proxy is not '':
                log.console_log("{}[*] Checking Proxy Status... {}".format(G, W))
                if self.check_single_proxy_status(proxy, "http://" + str(domain)) == 'ok':
                    pass
                else:
                    log.console_log('{}[-] Please use another proxy or disable proxy! {}'.format(R, W))
                    sys.exit()

            if proxy_file is not '':
                log.console_log("{}[*] Checking Proxy Status from file {}{}".format(G, proxy_file, W))
                self.check_multiple_proxy_status(proxy_file, "http://" + str(domain))
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

        log.console_log("{}All done sir! All logs saved in {}logs{} directory and dowloaded file saved in {}belatiFiles{} {}".format(Y, B, Y, B, Y, W))

        self.start_web_server()

    def check_domain(self, domain_name, proxy_address):
        check = CheckDomain()

        log.console_log(G + "{}[*] Checking Domain Availability... {}".format(G, W) , 0)
        log.console_log(check.domain_checker(domain_name, proxy_address))
        
        log.console_log("{}[*] Checking URL Alive... {}".format(G, W), 0)
        log.console_log(check.alive_check(domain_name, proxy_address))

        log.console_log("{}[*] Perfoming Whois... {}".format(G, W))
        whois_result = check.whois_domain(domain_name)
        log.console_log(whois_result)
        email = re.findall(r'[a-zA-Z0-9._+-]+@[a-zA-Z0-9._+-]+\s*', str(whois_result))

        # JSON Beautifier
        json_bf = JsonBeautifier()
        json_whois = json_bf.beautifier(str(whois_result))
        self.db.insert_domain_result(self.project_id, util.strip_scheme(domain_name), str(json_whois), util.clean_list_string(email))

    def banner_grab(self, domain_name, proxy_address):
        banner = BannerGrab()
        log.console_log("{}[*] Perfoming HTTP Banner Grabbing... {}".format(G, W))
        banner_info = banner.show_banner(domain_name, proxy_address)
        log.console_log(banner_info)
        self.db.insert_banner(domain_name, self.project_id, str(banner_info))

    def enumerate_subdomains(self, domain_name, proxy):
        log.console_log("{}[*] Perfoming Subdomains Enumeration...{}".format(G, W))
        sub_enum = SubdomainEnum()
        log.console_log("{}[+] Grabbing data from dnsdumpster...{}\n".format(B, W))
        dnsdumpster = sub_enum.scan_dnsdumpster(domain_name)
        subdomain_list = []
        data_table = [["Domain", "IP", "Provider", "Country"]]
        for entry in dnsdumpster['dns_records']['host']:
            data_table.extend([[entry['domain'], entry['ip'], entry['provider'], entry['country']]])
            subdomain_list.append(entry['domain'])

        log.console_log( tabulate(data_table, headers='firstrow') )

        log.console_log("{}[+] Grabbing data from crt.sh...{}\n".format(B, W))
        crt_list = sub_enum.scan_crtsh(domain_name, proxy)
        
        if crt_list is not None:
            log.console_log("\n".join(crt_list))
            subdomain_list = list(set(subdomain_list + crt_list))
        
        log.console_log("{}[+] Grabbing data from findsubdomains.com...{}\n".format(B, W))
        findsubdomains_list = sub_enum.scan_findsubdomainsCom(domain_name,proxy)
        
        if findsubdomains_list is not None:
            log.console_log("\n".join(findsubdomains_list))
            subdomain_list = list(set(subdomain_list + findsubdomains_list))

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

            self.db.update_dns_zone(self.project_id, domain_name, util.clean_list_string(ns_record_list), util.clean_list_string(mx_record_list))

        except Exception, exc:
            print("{}[*] No response from server... SKIP!{}".format(R, W))

    def harvest_email_search(self, domain_name, proxy_address):
        log.console_log("{}[*] Perfoming Email Harvest from Google Search...{}".format(G, W) )
        harvest = HarvestEmail()
        harvest_result = harvest.crawl_search(domain_name, proxy_address)
        try:
            log.console_log("{}[*] Found {} emails on domain {}{}".format(Y, str(len(harvest_result)), domain_name, W))
            log.console_log("{}{}{}".format(R, '\n'.join(harvest_result), W))
            self.db.insert_email_result(self.project_id, util.clean_list_string(harvest_result))
        except Exception, exc:
            log.console_log("{}[-] Not found or Unavailable. {}{}".format(R, str(harvest_result), W ))

    def harvest_email_pgp(self, domain_name, proxy_address):
        log.console_log("{}[*] Perfoming Email Harvest from PGP Server...{}".format(G, W) )
        harvest = HarvestEmail()
        harvest_result = harvest.crawl_pgp_mit_edu(domain_name, proxy_address)
        try:
            log.console_log("{}[*] Found {} emails on domain {}{}".format(Y, str(len(harvest_result)), domain_name, W))
            log.console_log("{}{}{}".format(R, '\n'.join(harvest_result), W))
            self.db.update_pgp_email(self.project_id, util.clean_list_string(harvest_result))
        except Exception, exc:
            log.console_log("{}[-] Not found or Unavailable. {}{}".format(R, str(harvest_result), W ))

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

    def start_web_server(self):
        log.console_log("{}Starting Django Web Server at http://127.0.0.1:8000/{}".format(Y, W))
        py_bin = self.conf.get_config("Environment", "py_bin")
        command = "{} web/manage.py runserver 0.0.0.0:8000".format(py_bin)
        process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE)
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                log.console_log(output.strip())
        rc = process.poll()
        return rc

    def complete_set(self, text, line, start_index, end_index):
        if text:
            return [
                param for param in self.list_parameter
                if param.startswith(text)
            ]
        else:
            return self.list_parameter

    def common_service_check(self, host):
        log.console_log("{}[*] Checking Common Service Check on host {}{}".format(G, host, W))
        service_check = CommonServiceCheck()
        service_check.check_available_service(host)

    def timeLimitHandler(self, signum, frame):
        print("No Response...")

if __name__ == '__main__':
    BelatiApp = Belati()
    BelatiApp.cmdloop()
