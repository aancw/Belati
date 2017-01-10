# coding=utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import *
import unittest
from whois import whois


class TestQuery(unittest.TestCase):
    def test_simple_ascii_domain(self):
        domain = 'google.com'
        whois(domain)

    def test_simple_unicode_domain(self):
        domain = 'нарояци.com'
        whois(domain)

    def test_unicode_domain_and_tld(self):
        domain = 'россия.рф'
        whois(domain)
