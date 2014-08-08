
**************
SSH backend
**************

This backend provides access to remote device through SSH (Secure SHell).
Moreover SSH backend supports two main firmwares:

 * AirOS
 * OpenWRT


AirOS example
=============

Here it is an example of how to import the SSH.AirOS backend, declare a device and invoke methods and properties on it::

 from netengine.backends.ssh import AirOS

Now we can invoke methods and properties by simply typing::


    device = AirOS('10.40.0.1', 'root', 'password')

    device.name
    'RM5PomeziaSNode'
    device.model
    'Rocket M5'
    device.os
    ('AirOS', 'XMar7240.v5.3.3.sdk.9634.1111221.2238')

    device.to_json()



OpenWRT example
================

Now we try to use OpenWRT instead of AirOS

::

 from netengine.backends.ssh import OpenWRT

 device = OpenWRT('10.177.8.100', 'root', 'password')

 device.name
 'owrt1'
 device.os
 '('OpenWrt', '12.09 (Attitude Adjustment 12.09, r36088)')'

 device.to_json()
