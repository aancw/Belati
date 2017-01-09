# Belati
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
- Scrapping Public Document for Domain from Search Engine

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
- Proxy Support for Harvesting
- Scanning Report export to PDF

## Install/Usage
```
git clone https://github.com/aancw/Belati.git
pip2 install -r requirements.txt
sudo su
python Belati.py --help
```

Still on progress. Be patient.

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
- python-nmap

## Library
- python-whois
- Sublist3r
- Subbrute
- nmap

## Notice
I'm using PyWhois Library, Sublist3r, MailHarvester, Emingoo as part of my code. This tool is for educational purposes only. Any damage you make will not affect the author. Do It With Your Own Risk

## Author
Aan Wahyu a.k.a Petruknisme(https://petruknisme.com)

## License
Belati is licensed under GPL V2. You can use, modify, or redistribute this tool under the terms of GNU General Public License (GPLv2).
