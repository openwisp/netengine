*****
Usage
*****

The usage of Netengine module requires it to be installed properly as explained in :ref:`index_reference`.
If you have an installation under a virtualenv, enter the folder /bin and type::
source activate
otherwise (if you have installed globally) just open an editor as bpython and you we are ready to go.

These are the main steps to follow to use the module:

 * import the correct backend and supported framework
 * declare a device using the proper constructor
 * invoke methods over the device just declared

So we have::

 from netengine.backends.<backend_name> import <supported_firmware>

 <device_name> = supported_firmware_constructor

To invoke methods over the just declared device it's necessary to use the dot notation as::

 <device_name>.<method or property>


Further example will be found inside dedicated docs for every backend

*************
Running tests
*************

Install nose::

    pip install nose

Clone repo::

    git clone git://github.com/ninuxorg/netengine

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
    # snmp openwrt specific tests
    nosetests tests.snmp.openwrt

    # ssh tests
    nosetests tests.ssh
    # ssh airos specific tests
    nosetests tests.ssh.airos
