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

import sys
import logging
import time

class logger(object):
    def __init__(self):
        timestamp = int(time.time())
        datetime = time.strftime("%d%m%Y")
        log_dir = "logs/"
        log_filename = log_dir + "Belati-" + datetime + "-" + str(timestamp) + ".log"

        if not os.path.exists(os.path.dirname(log_filename)):
            try:
                os.makedirs(os.path.dirname(log_filename))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

        logging.basicConfig(filename=log_filename, format='%(message)s')

    def consoleLog(self, log_word, newline=1):
        logging.warning(log_word)
        if newline == 1:
            print(log_word)
        else:
            sys.stdout.write(log_word)

if __name__ == '__main__':
    LoggerApp = Logger()
    LoggerApp
