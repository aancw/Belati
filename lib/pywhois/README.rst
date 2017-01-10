Goal
====

-  Create a simple importable Python module which will produce parsed
   WHOIS data for a given domain.
-  Able to extract data for all the popular TLDs (com, org, net, ...)
-  Query a WHOIS server directly instead of going through an
   intermediate web service like many others do.
-  Works with Python 2 & 3



Example
=======

.. sourcecode:: python

    >>> import whois
    >>> w = whois.whois('webscraping.com')
    >>> w.expiration_date  # dates converted to datetime object
    datetime.datetime(2013, 6, 26, 0, 0)
    >>> w.text  # the content downloaded from whois server
    u'\nWhois Server Version 2.0\n\nDomain names in the .com and .net 
    ...'

    >>> print w  # print values of all found attributes
    creation_date: 2004-06-26 00:00:00
    domain_name: [u'WEBSCRAPING.COM', u'WEBSCRAPING.COM']
    emails: [u'WEBSCRAPING.COM@domainsbyproxy.com', u'WEBSCRAPING.COM@domainsbyproxy.com']
    expiration_date: 2013-06-26 00:00:00
    ...



Install
=======

Install from pypi:

.. sourcecode:: bash

    pip install python-whois

Or checkout latest version from repository:

.. sourcecode:: bash

    hg clone https://bitbucket.org/richardpenman/pywhois

Note that then you will need to manually install the futures module, which allows supporting both Python 2 & 3:


.. sourcecode:: bash

    pip install futures




Changelog
=========

0.6 - 2016-03-02:

* support added for python 3
* updated TLD list

0.5 - 2015-09-05:

* added native client, which now handles whois requests by default
* added pretty formatting to string representation
* return None instead of raising KeyError when an attribute does not exist
* new TLD's: .mobi, .io, .kg, .su, .biz

0.4 - 2015-08-13:

* new TLD's: .de, .nl, .ca, .be
* migrated to bitbucket
* added socket timeout

0.3 - 2015-03-31:

* improved datetime parsing with python-dateutil when available
* base WhoisEntry class inherits from dict
* fixed TLD's: .org, .info



Contact
=======

You can post ideas or patches here:
https://bitbucket.org/richardpenman/pywhois/issues

Thanks to the many who have sent patches for additional domains!
