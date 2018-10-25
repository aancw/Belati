# Belati

![Belati](/images/Belati-logo.png?raw=true "Belati Logo")


[![Awesome OSINT](https://img.shields.io/badge/awesome-osint-brightgreen.svg)](https://github.com/jivoi/awesome-osint)
[![OSINT Framework](https://img.shields.io/badge/osint-framework-brightgreen.svg)](http://osintframework.com)
[![n0where](https://img.shields.io/badge/n0where-top%20100-lightgrey.svg)](https://n0where.net/best-cybersecurity-tools/)
[![ToolsWatch](https://img.shields.io/badge/Tools-Watch-brightgreen.svg)](http://www.toolswatch.org/2017/07/belati-v-0-2-2-dev-swiss-army-knife-for-osint/)
[![BlackArch Scanner](https://img.shields.io/badge/BlackArch-Scanner-red.svg)](https://blackarch.org/scanner.html)
[![Echo Ezine 31](https://img.shields.io/badge/Echo-Ezine%2031-yellow.svg)](http://ezine.echo.or.id/issue31/005.txt)


### Belati - The Traditional Swiss Army Knife For OSINT

Belati is tool for Collecting Public Data & Public Document from Website and other service for OSINT purpose. This tools is inspired by Foca and Datasploit for OSINT :)

## Current Version

v0.2.4

## Belati In Action

[![Belati In Action 0.24-stable Preview](https://img.youtube.com/vi/yRSln6BSo-c/0.jpg)](https://www.youtube.com/watch?v=yRSln6BSo-c)

## Why I Made this?
Just for learning stuff and OSINT purpose. Correct me if i'm wrong

## What Belati can do?
- Interactive command line shell
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
- Webserver only mode
- Auto Dependency Checker
- Auto Update system
- Document Metadata/Exif Extractor
- Document Author Metadata
- Graph Visualization( On Progress )

## TODO

Please see Belati TODO list here -> https://github.com/aancw/Belati/issues/12

## Library

- python-whois
- Sublist3r
- Subbrute

## Requirements

- nmap
- git
- sqlite3
- exiftool

```
sudo apt-get install nmap git sqlite3 exiftool
```

## Install/Usage

```
git clone https://github.com/aancw/Belati.git
cd Belati
git submodule update --init --recursive --remote
pip install --upgrade pip
pip install -r requirements.txt #please use pip with python v2
sudo su
python Belati.py --help
```

## Docker Installation

- Download Dockerfile:

```bash
wget https://raw.githubusercontent.com/aancw/Belati/master/Dockerfile
```

- Execute the following command to create a Docker image locally:
  ```bash
  docker build -t belati . #dot
  ```

- To create a container from the image, execute:
  ```bash
  docker run -p 8000:8000 -it belati /bin/bash
  ```

- Running Belati
    ```bash
    belati -h
    ```


For more info, please refer to this guide: https://github.com/espi0n/Dockerfiles/blob/master/Belati/README.md

## Tested On

- Ubuntu 16.04 x86_64
- Arch Linux x86_64
- CentOS 7
- Debian Jessie
- MacOS

## Python Requirements

This tool not compatible with Python 3. I need to migrate this later. So use python v2.7 instead!

## Why Need Root Privilege?

I've try to avoid using Root Privilege, but nmap need Root Privilege. You can add sudo or other way to run nmap without root privilege. It's your choice ;)

Reference -> https://secwiki.org/w/Running_nmap_as_an_unprivileged_user

Don't worry. Belati still running well when you are run with normal user ;)

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
- python-wappalyzer
- future
- beautifulsoup4
- python-whois
- futures
- django
- pyexifinfo
- cmd2
- tabulate

## Missing Dependencies?

If you are seeing this

```
$ python Belati.py

            You are missing a module required for Belati. In order to continue using Belati, please install them with:

            `pip install --upgrade --force-reinstall -r requirements.txt`

            or manually install missing modules with:

            `pip install --upgrade --force-reinstall dnspython requests termcolor colorama future beautifulsoup4 futures`
```

and this

```
You are using pip version 8.1.2, however version 9.0.1 is available.
You should consider upgrading via the 'pip install --upgrade pip' command.
```        

Please upgrade pip version and follow the instructions:

```
pip install --upgrade pip
```

## System Dependencies

For CentOS/Fedora user, please install this:

```
yum install gcc gmp gmp-devel python-devel
```


## Notice

This tool is for educational purposes only. Any damage you make will not affect the author. Do It With Your Own Risk!

## Feedback/Suggestion

Feel free to create Issue in this repository or email me at `cacaddv [at] gmail.com` . Your feedback and suggestion is useful for Belati development progress :)

## Contribution

Belati welcomes contribution from everyone. Please see [CONTRIBUTING.md](https://github.com/aancw/Belati/blob/master/CONTRIBUTING.md)

## Contributors

Please see [CONTRIBUTORS.md](https://github.com/aancw/Belati/blob/master/CONTRIBUTORS.md) and please add your name for credit in that file :)

## Thanks To

Thanks to PyWhois Library, Sublist3r, MailHarvester, Emingoo for being part of my code. Also thanks to Hispagatos, Infosec-ninjas, eCHo, RNDC( Research and development center ) and all other people who are inspiring this project :)

## Publications

Echo Ezine 31 : http://ezine.echo.or.id/issue31/005.txt - Belati : Collecting Public Data & Public Document for OSINT Purpose - Petruknisme

IDSECCONF 2017 : https://www.slideshare.net/idsecconf/belati-the-traditional-swiss-army-knife-for-osint - Belati: The Traditional Swiss Army Knife for OSINT


## License

**Author:** Aan Wahyu( https://petruknisme.com )

Belati is licensed under GPL V2. You can use, modify, or redistribute this tool under the terms of GNU General Public License (GPLv2). Please see [LICENSE](https://github.com/aancw/Belati/blob/master/LICENSE) for the full license text.
