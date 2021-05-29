*****
Usage
*****

The usage of Netengine module requires it to be installed properly as explained in :doc:`index<../index>`.
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

Install test reqirements::

    pip install -r reqirements.txt
    pip install -r requirements-test.txt

Clone repo::

    git clone git://github.com/openwisp/netengine

    ./runtests.py

To run tests on real devices, first copy the settings file::

    cp test-settings.example.json test-settings.json

Then change the credentials accordingly, now run tests with::

    DISABLE_MOCKS=1 TEST_SETTINGS_FILE='test-settings.json' ./runtests.py

See test coverage with::

    nosetests --with-coverage --cover-package=netengine

Run specific tests by specifying the relative path::

    # base tests
    nosetests tests.base

    # snmp tests
    nosetests tests.snmp
    # snmp openwrt specific tests
    nosetests tests.snmp.openwrt

    # run without mocks with a custom test file
    DISABLE_MOCKS=1 TEST_SETTINGS_FILE='test-settings.json' nosetests tests.snmp
