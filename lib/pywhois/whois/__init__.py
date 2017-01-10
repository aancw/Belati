from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from future import standard_library
standard_library.install_aliases()
from builtins import *
import re
import sys
import os
import subprocess
import socket
from .parser import WhoisEntry
from .whois import NICClient


def whois(url, command=False):
    # clean domain to expose netloc
    ip_match = re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", url)
    if ip_match:
        domain = url
        try:
            result = socket.gethostbyaddr(url)
        except socket.herror as e:
            pass
        else:
            domain = result[0]
    else:
        domain = extract_domain(url)
    if command:
        # try native whois command
        r = subprocess.Popen(['whois', domain], stdout=subprocess.PIPE)
        text = r.stdout.read()
    else:
        # try builtin client
        nic_client = NICClient()
        text = nic_client.whois_lookup(None, domain, 0)
    return WhoisEntry.load(domain, text)


def extract_domain(url):
    """Extract the domain from the given URL

    >>> extract_domain('http://www.google.com.au/tos.html')
    'google.com.au'
    >>> extract_domain('www.webscraping.com')
    'webscraping.com'
    >>> extract_domain('198.252.206.140')
    'stackoverflow.com'
    >>> extract_domain('102.112.2O7.net')
    '2o7.net'
    >>> extract_domain('1-0-1-1-1-0-1-1-1-1-1-1-1-.0-0-0-0-0-0-0-0-0-0-0-0-0-10-0-0-0-0-0-0-0-0-0-0-0-0-0.info')
    '0-0-0-0-0-0-0-0-0-0-0-0-0-10-0-0-0-0-0-0-0-0-0-0-0-0-0.info'
    """
    if re.match(r'\d+\.\d+\.\d+\.\d+', url):
        # this is an IP address
        return socket.gethostbyaddr(url)[0]

    tlds_path = os.path.join(os.getcwd(), os.path.dirname(__file__), 'data', 'tlds.txt')
    with open(tlds_path) as tlds_fil:
        suffixes = [line.lower().encode('utf-8')
                    for line in (x.strip() for x in tlds_fil)
                    if not line.startswith('#')]
    suff = 'xn--p1ai'

    if not isinstance(url, str):
        url = url.decode('utf-8')
    url = re.sub('^.*://', '', url)
    url = url.split('/')[0].lower().encode('idna')

    domain = []
    for section in url.split(b'.'):
        if section in suffixes:
            domain.append(section)
        else:
            domain = [section]
    return b'.'.join(domain).decode('idna')


if __name__ == '__main__':
    try:
        url = sys.argv[1]
    except IndexError:
        print('Usage: %s url' % sys.argv[0])
    else:
        print(whois(url))
