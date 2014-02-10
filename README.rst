=========
netengine
=========

.. image:: https://landscape.io/github/nemesisdesign/netengine/master/landscape.png
   :target: https://landscape.io/github/nemesisdesign/netengine/master
   :alt: Code Health

.. image:: https://requires.io/github/nemesisdesign/netengine/requirements.png?branch=master
   :target: https://requires.io/github/nemesisdesign/netengine/requirements/?branch=master
   :alt: Requirements Status

Abstraction layer for extracting information from network devices.

Install
=======

Install via pip::

    pip install -e git+git://github.com/nemesisdesign/netengine#egg=netengine

Usage
=====

SSH example::

    from netengine.backends.ssh import AirOS
    
    device = AirOS('10.40.0.1', 'root', 'password')
    
    device.name
    'RM5PomeziaSNode'
    device.model
    'Rocket M5'
    device.os
    ('AirOS', 'XMar7240.v5.3.3.sdk.9634.1111221.2238')

    device.to_json()
    
Specific backend (protocol) commands, SSH example::

    print device.run('ls -l')
    -rw-------    1 root     admin         459 Jan 26  2011 dropbear_dss_host_key
    -rw-------    1 root     admin         427 Jan 26  2011 dropbear_rsa_host_key
    drwxr-xr-x    3 root     admin           0 Oct 21  2011 mcuser
    -rwxr-xr-x    1 root     admin         662 Nov 11 18:12 ninux
    -rw-------    1 root     admin        1133 Nov 12 00:27 olsrd.conf
    -rw-r--r--    1 root     admin         786 Dec 21  2011 olsrd6.conf
    -rw-r--r--    1 root     admin         234 Jan  4  2012 radvd.conf

SNMP example::

    from netengine.backends.snmp import AirOS
    
    device = AirOS('10.40.0.1', community='public')
    
    device.name
    'RM5PomeziaSNode'
    device.model
    'Rocket M5'
    device.os
    ('AirOS', 'XMar7240.v5.3.3.sdk.9634.1111221.2238')

Specific SNMP command example::

    from netengine.backends.snmp import OpenWRT
    
    device = OpenWRT('10.40.0.1', community='public')
    # get a certain OID
    device.get('1.2.840.10036.3.1.2.1.4.8')
    

HTTP example::

    # TODO

MUNIN example::

    # TODO

Running tests
=============

Install nose::

    pip install nose

Clone repo::

    git clone git://github.com/nemesisdesign/netengine
    
    cd netengine/

Edit settings json file according to your network::

    cp test-settings.example.json test-settings.json
    vim test-settings.json

Run tests with::

    nosetests

See test coverage with::

    nosetests --with-coverage --cover-package=netengine

Run specific tests by specifying the relative path::

    # base tests
    nosetests tests.base

    # snmp tests
    nosetests tests.snmp
    
    # ssh tests
    nosetests tests.ssh

Contribute
==========

1. Join the `ninux-dev mailing list`_
2. Fork this repo
3. Follow `PEP8, Style Guide for Python Code`_
4. Write code
5. Write tests for your code
6. Ensure all tests pass
7. Ensure test coverage is not under 90%
8. Document your changes
9. Send pull request

.. _PEP8, Style Guide for Python Code: http://www.python.org/dev/peps/pep-0008/
.. _ninux-dev mailing list: http://ml.ninux.org/mailman/listinfo/ninux-dev

License
=======

Copyright (c) 2013 Federico Capoano

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

Except as contained in this notice, the name(s) of the above copyright holders
shall not be used in advertising or otherwise to promote the sale,
use or other dealings in this Software without prior written authorization.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
