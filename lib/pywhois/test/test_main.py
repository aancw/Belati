# coding=utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import *
import unittest
from whois import extract_domain


class TestExtractDomain(unittest.TestCase):
    def test_simple_ascii_domain(self):
        url = 'google.com'
        domain = url
        self.assertEqual(domain, extract_domain(url))

    def test_ascii_with_schema_path_and_query(self):
        url = 'https://www.google.com/search?q=why+is+domain+whois+such+a+mess'
        domain = 'www.google.com'
        self.assertEqual(domain, extract_domain(url))

    def test_simple_unicode_domain(self):
        url = 'http://нарояци.com/'
        domain = 'нарояци.com'
        self.assertEqual(domain, extract_domain(url))

    def test_unicode_domain_and_tld(self):
        url = 'http://россия.рф/'
        domain = 'россия.рф'
        self.assertEqual(domain, extract_domain(url))
