# Belati
Belati - The Traditional Swiss Army Knife For OSINT

Belati is tool for Collecting Public Data & Public Document from Website and other service for OSINT purpose. This tools is inspired by Foca and Datasploit for OSINT :)

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
- Gather Public Company Employee


## TODO
- Automatic OSINT with Username and Email support
- Organization or Company OSINT Support
- Collecting Data from Public service with Username and Email for LinkedIn and other service.
- Setup Wizard for Token and setting up Belati
- Token Support
- Email Harvesting with multiple content(github, linkedin, etc)
- Scrapping Public Document with multiple search engine(yahoo, yandex, bing etc)
- Metadata Extractor
- Database Support
- Web version with Django
- Scanning Report export to PDF
- domain or subdomain reputation checker
- Reporting Support to JSON, PDF 

## Install/Usage
```
git clone https://github.com/aancw/Belati.git
git submodule update --init --recursive
pip install -r requirements.txt #please use pip with python v2
sudo su
python Belati.py --help
```

Still on progress. Be patient.

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

## Notice
I'm using PyWhois Library, Sublist3r, MailHarvester, Emingoo as part of my code. This tool is for educational purposes only. Any damage you make will not affect the author. Do It With Your Own Risk

## Author
Aan Wahyu a.k.a Petruknisme(https://petruknisme.com)

## Thanks To

Thanks to PyWhois Library, Sublist3r, MailHarvester, Emingoo for being part of my code. Also thanks to Hispagatos, Infosec-ninjas, eCHo, RNDC( Research and development center ) and all other people who are inspiring this project :)

Thanks to Echo-Zine Staff for approving my Ezine : http://ezine.echo.or.id/issue31/005.txt - Belati : Collecting Public Data & Public Document for OSINT Purpose - Petruknisme


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
