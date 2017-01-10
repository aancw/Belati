from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import *
import unittest

import os
import sys
sys.path.append('../')

import datetime

import simplejson
from glob import glob

from whois.parser import WhoisEntry, cast_date

class TestParser(unittest.TestCase):
    def test_com_expiration(self):
        data = """
        Status: ok
        Updated Date: 14-apr-2008
        Creation Date: 14-apr-2008
        Expiration Date: 14-apr-2009
        
        >>> Last update of whois database: Sun, 31 Aug 2008 00:18:23 UTC <<<
        """
        w = WhoisEntry.load('urlowl.com', data)
        expires = w.expiration_date.strftime('%Y-%m-%d')
        self.assertEqual(expires, '2009-04-14')

    def test_cast_date(self):
        dates = ['14-apr-2008', '2008-04-14']
        for d in dates:
            r = cast_date(d).strftime('%Y-%m-%d')
            self.assertEqual(r, '2008-04-14')

    def test_com_allsamples(self):
        """
        Iterate over all of the sample/whois/*.com files, read the data,
        parse it, and compare to the expected values in sample/expected/.
        Only keys defined in keys_to_test will be tested.
        
        To generate fresh expected value dumps, see NOTE below.
        """
        keys_to_test = ['domain_name', 'expiration_date', 'updated_date',
                        'creation_date', 'status']
        fail = 0
        total = 0
        for path in glob('test/samples/whois/*.com'):
            # Parse whois data
            domain = os.path.basename(path)
            with open(path) as whois_fp:
                data = whois_fp.read()
            
            w = WhoisEntry.load(domain, data)
            results = {key: w.get(key) for key in keys_to_test}

            # NOTE: Toggle condition below to write expected results from the
            # parse results This will overwrite the existing expected results.
            # Only do this if you've manually confirmed that the parser is
            # generating correct values at its current state.
            if False:
                def date2str4json(obj):
                    if isinstance(obj, datetime.datetime):
                        return str(obj)
                    raise TypeError(
                            '{} is not JSON serializable'.format(repr(obj)))
                outfile_name = os.path.join('test/samples/expected/', domain)
                with open(outfile_name, 'w') as outfil:
                    expected_results = simplejson.dump(results, outfil,
                                                       default=date2str4json)
                continue

            # Load expected result
            with open(os.path.join('test/samples/expected/', domain)) as infil:
                expected_results = simplejson.load(infil)
            
            # Compare each key
            for key in results:
                total += 1
                result = results.get(key)
                if isinstance(result, datetime.datetime):
                    result = str(result)
                expected = expected_results.get(key)
                if expected != result:
                    print("%s \t(%s):\t %s != %s" % (domain, key, result, expected))
                    fail += 1
            
        if fail:
            self.fail("%d/%d sample whois attributes were not parsed properly!"
                      % (fail, total))


    def test_ca_parse(self):
        data = """
        Domain name:           testdomain.ca
        Domain status:         registered
        Creation date:         2000/11/20
        Expiry date:           2020/03/08
        Updated date:          2016/04/29
        DNSSEC:                Unsigned

        Registrar:
            Name:              Webnames.ca Inc.
            Number:            70

        Registrant:
            Name:              Test Industries

        Administrative contact:
            Name:              Test Person1
            Postal address:    Test Address
                               Test City, TestVille
            Phone:             +1.1235434123x123
            Fax:               +1.123434123
            Email:             testperson1@testcompany.ca

        Technical contact:
            Name:              Test Persion2
            Postal address:    Other TestAddress
                               TestTown OCAS Canada
            Phone:             +1.09876545123
            Fax:               +1.12312993873
            Email:             testpersion2@testcompany.ca

        Name servers:
            ns1.testserver1.net
            ns2.testserver2.net
        """
        results = WhoisEntry.load('testcompany.ca', data)
        expected_results = {
            "updated_date": "2016-04-29 00:00:00", 
            "registrant_name": [
                "Webnames.ca Inc.", 
                "Test Industries", 
                "Test Person1", 
                "Test Persion2"
            ], 
            "fax": [
                "+1.123434123", 
                "+1.12312993873"
            ], 
            "dnssec": "Unsigned", 
            "registrant_number": "70", 
            "expiration_date": "2020-03-08 00:00:00", 
            "domain_name": "testdomain.ca", 
            "creation_date": "2000-11-20 00:00:00", 
            "phone": [
                "+1.1235434123x123", 
                "+1.09876545123"
            ], 
            "domain_status": "registered", 
            "emails": [
                "testperson1@testcompany.ca", 
                "testpersion2@testcompany.ca"
            ]
        }
        
        fail = 0
        total = 0

        # Compare each key
        for key in expected_results:
            total += 1
            result = results.get(key)
            if isinstance(result, datetime.datetime):
                result = str(result)
            expected = expected_results.get(key)
            if expected != result:
                print("%s \t(%s):\t %s != %s" % (domain, key, result, expected))
                fail += 1
        if fail:
            self.fail("%d/%d sample whois attributes were not parsed properly!"
                      % (fail, total))



        

if __name__ == '__main__':
    unittest.main()
