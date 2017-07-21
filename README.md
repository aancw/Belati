# Belati

[![Awesome OSINT](https://img.shields.io/badge/awesome-osint-brightgreen.svg)](https://github.com/jivoi/awesome-osint)
[![OSINT Framework](https://img.shields.io/badge/osint-framework-brightgreen.svg)](http://osintframework.com)
[![n0where](https://img.shields.io/badge/n0where-top%20100-lightgrey.svg)](https://n0where.net/best-cybersecurity-tools/)
[![ToolsWatch](https://img.shields.io/badge/Tools-Watch-brightgreen.svg)](http://www.toolswatch.org/2017/07/belati-v-0-2-2-dev-swiss-army-knife-for-osint/)
[![Echo Ezine 31](https://img.shields.io/badge/Echo-Ezine%2031-yellow.svg)](http://ezine.echo.or.id/issue31/005.txt)



Belati - The Traditional Swiss Army Knife For OSINT

Belati is tool for Collecting Public Data & Public Document from Website and other service for OSINT purpose. This tools is inspired by Foca and Datasploit for OSINT :)

## Version

v.0.2.2-dev

## Belati In Action

[Belati In Action Preview](https://www.youtube.com/watch?v=AGvsIWoaX_k)

## Why I Made this?
Just for learning stuff and OSINT purpose. Correct me if i'm wrong

## What Belati can do?
- Whois(Indonesian TLD Support)
- Banner Grabbing
- Subdomain Enumeration
- Service Scanning for all Subdomain Machine
- Web Appalyzer Support
- DNS mapping / Zone Scanning
- Mail Harvester from Website & Search Engine
- Mail Harvester from MIT PGP Public Key Server
- Scrapping Public Document for Domain from Search Engine
- Fake and Random User Agent ( Prevent from blocking )
- Proxy Support for Harvesting Emails and Documents
- Public Git Finder in domain/subdomain
- Public SVN Finder in domain/subdomain
- Robot.txt Scraper in domain/subdomain
- Gather Public Company Info & Employee
- SQLite3 Database Support for storing Belati Results
- Setup Wizard/Configuration for Belati
- Django Web Management

## TODO
- Automatic OSINT with Username and Email support
- Organization or Company OSINT Support
- Collecting Data from Public service with Username and Email for LinkedIn and other service.
- Setup Wizard for Token and setting up Belati
- Token Support
- Email Harvesting with multiple content(github, linkedin, etc)
- Scrapping Public Document with multiple search engine(yahoo, yandex, bing etc)
- Metadata Extractor
- Scanning Report export to PDF
- domain or subdomain reputation checker
- Reporting Support to JSON, PDF
- Belati Updater

## Install/Usage
```
git clone https://github.com/aancw/Belati.git
cd Belati
git submodule update --init --recursive --remote
pip install -r requirements.txt #please use pip with python v2
sudo su
python Belati.py --help
```

## Tested On

Ubuntu 16.04 x86_64
Arch Linux x86_64
CentOS 7

## Python Requirements

This tool not compatible with Python 3. I need to migrate this later. So use python v2.7 instead!

## Why Need Root Privilege?

I've try to avoid using Root Privilege, but nmap need Root Privilege. You can add sudo or other way to run nmap without root privilege. It's your choice ;)

Reference -> https://secwiki.org/w/Running_nmap_as_an_unprivileged_user

Don't worry. Belati still running when you are run with normal user ;)

## Dependencies
- urllib2
- dnspython
- requests
- argparse
- texttable
- python-geoip-geolite2
- python-geoip
- dnsknife
- termcolor
- colorama
- validators
- tqdm
- tldextract
- fake-useragent

## Missing Dependencies?

If you are seeing this

```
$ python Belati.py

            You are missing a module required for Belati. In order to continue using Belati, please install them with:

            `pip install -r requirements.txt`

            or manually install missing modules with:

            `pip install dnspython requests termcolor colorama future beautifulsoup4 futures`
```

and this

```
You are using pip version 8.1.2, however version 9.0.1 is available.
You should consider upgrading via the 'pip install --upgrade pip' command.
```        

Please upgrade pip version:

```
pip install --upgrade pip
```

## System Dependencies

For CentOS/Fedora user, please install this:

```
yum install gcc gmp gmp-devel python-devel
```

## Library
- python-whois
- Sublist3r
- Subbrute
- nmap
- git
- sqlite3

## Notice
This tool is for educational purposes only. Any damage you make will not affect the author. Do It With Your Own Risk!

## Author
Aan Wahyu a.k.a Petruknisme(https://petruknisme.com)

## Thanks To

Thanks to PyWhois Library, Sublist3r, MailHarvester, Emingoo for being part of my code. Also thanks to Hispagatos, Infosec-ninjas, eCHo, RNDC( Research and development center ) and all other people who are inspiring this project :)

Thanks to Echo-Zine Staff for approving my Ezine : http://ezine.echo.or.id/issue31/005.txt - Belati : Collecting Public Data & Public Document for OSINT Purpose - Petruknisme

## Feedback/Suggestion

Feel free to create Issue in this repository or email me at `cacaddv [at] gmail.com` . Your feedback and suggestion is useful for Belati development progress :)

## License
Belati is licensed under GPL V2. You can use, modify, or redistribute this tool under the terms of GNU General Public License (GPLv2).

```
    Belati is tool for Collecting Public Data & Public Document from Website and other service for OSINT purpose.
    This tools is inspired by Foca and Datasploit for OSINT
    Copyright (C) 2017  cacaddv@gmail.com (Petruknisme a.k.a Aan Wahyu)

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
```
