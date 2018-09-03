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

class AboutProject(object):
    def __init__(self):
        self.__info__ = 'Collecting Public Data & Public Document for OSINT purpose'
        self.__author__ = 'Petruknisme'
        self.__version__ = 'v0.2.5'
        self.__name__= "Belati"
        self.__giturl__ = "https://github.com/aancw/Belati"
        self.__authorurl__ = "https://petruknisme.com"

if __name__ == '__main__':
    AboutProjectApp = AboutProject()
    AboutProjectApp
