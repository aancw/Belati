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

import sys, os, errno
import sqlite3 as db
from .logger import Logger
from .config import Config

# Console color
G = '\033[92m'  # green
Y = '\033[93m'  # yellow
B = '\033[94m'  # blue
R = '\033[91m'  # red
W = '\033[0m'   # white

log = Logger()

class Database(object):
    def __init__(self):
        conf = Config()
        self.conn = None
        db_location = conf.get_config("Database", "db_location")
        try:
            self.conn = db.connect(db_location)
            self.conn.text_factory = str
        except db.Error as e:
            print(("Error: " +  str(e.args[0])))
            sys.exit()

    def create_new_project(self, project_domain, project_org, time):
        cur = self.conn.cursor()
        cur.execute("INSERT INTO projects(`project_domain`, `project_org`, `started_time`) VALUES (?, ?, ?)", (project_domain, project_org, time))
        self.conn.commit()

        return cur.lastrowid

    def check_subdomain_exist(self, project_id, subdomain):
        cur = self.conn.cursor()
        cur.execute("SELECT id from subdomain_results WHERE project_id = ? AND subdomain = ?",(project_id, subdomain))
        data = cur.fetchone()
        return data

    def insert_banner(self, domain, project_id, banner_info):
        cur = self.conn.cursor()
        subdomain_exist = self.check_subdomain_exist(project_id, domain)

        if subdomain_exist == None:
            cur.execute("INSERT INTO subdomain_results(`project_id`, `subdomain`, `banner`) VALUES(?, ?, ?)", (project_id, domain, banner_info))
        else:
            cur.execute("UPDATE subdomain_results SET `banner` = ? WHERE project_id = ? AND subdomain = ? ", (banner_info, project_id, domain))

        self.conn.commit()

    def insert_robots_txt(self, project_id, domain, robots_txt):
        cur = self.conn.cursor()
        subdomain_exist = self.check_subdomain_exist(project_id, domain)

        if subdomain_exist == None:
            cur.execute("INSERT INTO subdomain_results(`project_id`, `subdomain`, `robots_txt`) VALUES(?, ?, ?)", (project_id, domain, robots_txt))
        else:
            cur.execute("UPDATE subdomain_results SET `robots_txt` = ? WHERE project_id = ? AND subdomain = ? ", (robots_txt, project_id, domain))

        self.conn.commit()

    def insert_wappalyzing(self, project_id, domain, wappalyzing_result):
        cur = self.conn.cursor()
        subdomain_exist = self.check_subdomain_exist(project_id, domain)

        if subdomain_exist == None:
            cur.execute("INSERT INTO subdomain_results(`project_id`, `subdomain`, `wappalyzer`) VALUES(?, ?, ?)", (project_id, domain, wappalyzing_result))
        else:
            cur.execute("UPDATE subdomain_results SET `wappalyzer` = ? WHERE project_id = ? AND subdomain = ? ", (wappalyzing_result, project_id, domain))

        self.conn.commit()

    def update_subdomain_ip(self, project_id, subdomain, ipaddress):
        cur = self.conn.cursor()
        subdomain_exist = self.check_subdomain_exist(project_id, subdomain)

        if subdomain_exist:
            cur.execute("UPDATE subdomain_results SET ip_address = ? WHERE project_id = ? AND subdomain = ?", (ipaddress, project_id, subdomain))

        self.conn.commit()

    def update_git_finder(self, project_id, subdomain, status):
        cur = self.conn.cursor()
        subdomain_exist = self.check_subdomain_exist(project_id, subdomain)
        status_fix = "Yes" if status == "Yes" else "No"

        if subdomain_exist:
            cur.execute("UPDATE subdomain_results SET is_contain_git = ? WHERE project_id = ? AND subdomain = ?", (status_fix, project_id, subdomain))

        self.conn.commit()

    def update_svn_finder(self, project_id, subdomain, status):
        cur = self.conn.cursor()
        subdomain_exist = self.check_subdomain_exist(project_id, subdomain)
        status_fix = "Yes" if status == "Yes" else "No"

        if subdomain_exist:
            cur.execute("UPDATE subdomain_results SET is_contain_svn = ? WHERE project_id = ? AND subdomain = ?", (status_fix, project_id, subdomain))

        self.conn.commit()

    def insert_domain_result(self, project_id, domain, domain_whois, email):
        cur = self.conn.cursor()
        cur.execute("INSERT INTO main_domain_results(`project_id`, `domain`, `domain_whois`, `email`) VALUES(?, ?, ?, ?)", (project_id, domain, domain_whois, email))
        self.conn.commit()

    def update_dns_zone(self, project_id, domain, ns_record, mx_record):
        cur = self.conn.cursor()
        cur.execute("UPDATE main_domain_results SET NS_record = ?, MX_record = ? WHERE project_id = ? AND domain = ?", (ns_record, mx_record, project_id, domain))
        self.conn.commit()

    def insert_email_result(self, project_id, mail_results):
        cur = self.conn.cursor()
        cur.execute("INSERT INTO mail_harvest_results(`project_id`, `mail_results`) VALUES(?, ?)", (project_id, mail_results))
        self.conn.commit()

    def update_pgp_email(self, project_id, mail_pgp_results):
        cur = self.conn.cursor()
        cur.execute("UPDATE mail_harvest_results SET mail_pgp_results = ? WHERE project_id = ?", (mail_pgp_results, project_id))
        self.conn.commit()

    def insert_public_doc(self, project_id, doc_ext, doc_url, doc_location, doc_full_location, doc_meta_exif):
        cur = self.conn.cursor()
        cur.execute("INSERT INTO doc_results(`project_id`, `doc_ext`, `doc_url`, `doc_location`, `doc_full_location`, `doc_meta_exif` ) VALUES(?, ?, ?, ?, ?, ?)", (project_id, doc_ext, doc_url, doc_location, doc_full_location, doc_meta_exif))
        self.conn.commit()

    def insert_linkedin_company_info(self, project_id, company_name, company_linkedin_url, company_description):
        cur = self.conn.cursor()
        cur.execute("INSERT INTO linkedin_company_info(`project_id`, `company_name`, `company_linkedin_url`, `company_description`) VALUES  (?, ?, ?, ?)",(project_id, company_name, company_linkedin_url, company_description))
        self.conn.commit()

        return cur.lastrowid

    def insert_company_employees(self, project_id, name, job_title, linkedin_url ):
        cur = self.conn.cursor()
        cur.execute("INSERT INTO linkedin_company_employees(`project_id`, `name`, `job_title`, `linkedin_url`) VALUES(?, ?, ?, ?)", (project_id, name, job_title, linkedin_url))
        self.conn.commit()

    # def read(table, **kwargs):
    # """ Generates SQL for a SELECT statement matching the kwargs passed. """
    # sql = list()
    # sql.append("SELECT * FROM %s " % table)
    # if kwargs:
    #     sql.append("WHERE " + " AND ".join("%s = '%s'" % (k, v) for k, v in kwargs.iteritems()))
    # sql.append(";")
    # return "".join(sql)
    # cursor.execute("INSERT INTO table VALUES ?", args)
    # cursor.execute('INSERT INTO media_files (%s) VALUES (%%s, %%s, %%s, %%s,   ...)' % ','.join(fieldlist), valuelist)
