=========
netengine
=========

Abstraction layer for extracting information from network devices.

Install
=======

Install via pip::

pip install -e git+git://github.com/nemesisdesign/netengine#egg=netengine

Usage
=====

Basics::

    from netengine.ssh.ssh import SSH
    
    device = SSH('10.40.0.1', 'root', 'password')
    print device.run('ls -l')
    -rw-------    1 root     admin         459 Jan 26  2011 dropbear_dss_host_key
    -rw-------    1 root     admin         427 Jan 26  2011 dropbear_rsa_host_key
    drwxr-xr-x    3 root     admin           0 Oct 21  2011 mcuser
    -rwxr-xr-x    1 root     admin         662 Nov 11 18:12 ninux
    -rw-------    1 root     admin        1133 Nov 12 00:27 olsrd.conf
    -rw-r--r--    1 root     admin         786 Dec 21  2011 olsrd6.conf
    -rw-r--r--    1 root     admin         234 Jan  4  2012 radvd.conf


Running tests
=============

Install nose::

    pip install nose

Clone repo::

    git clone git://github.com/nemesisdesign/netengine
    
    cd netengine/

Edit settings json file according to your network::

    cp test-settings.json.example test-settings.json
    vim test-settings.json

Run tests with::

    nosetests

See test coverage with::

    nosetests --with-coverage --cover-package=netengine
