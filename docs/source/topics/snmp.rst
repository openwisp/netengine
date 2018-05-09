
**************
SNMP backend
**************

SNMP
=======

SNMP (Simple Network Management Protocol) is a network protocol very used to retrieve info from device.
All the information are retrieved by using codes called MIBs. All MIBs have a tree-like structure, every main information is the root and by adding more detail to the info
the tree gains more depth.
Obviously, by getting the smallest MIB which is "1" or simply " . " one can get all the tree.




The SNMP backend provides support for 3 firmwares:
 * AirOS
 * OpenWRT
 * Cisco




AirOS example
=============

::

 from netengine.backends.snmp import AirOS
 device = AirOS("10.40.0.130")
 device.name
 'RM5PomeziaSNode'
 device.uptime_tuple
 (121, 0, 5)  # a tuple containing device uptime hours, mins and seconds

We have just called two simple properties on **device**, but we can ask **device** for more specific values or portions of the SNMP tree not included in the API, just type::
 device.next("1.3.6")

Otherwise, if you want simply a value of the tree just type::
 device.get_value("oid_you_want_to_ask_for")





OpenWRT example
================

The same instructions typed above can be applied to OpenWRT itself, just remember to import the correct firmware by typing::

 from netengine.backends.snmp import OpenWRT




Cisco example
================

The same instructions typed above can be applied to Cisco itself, just remember to import the correct firmware by typing::

  from netengine.backends.snmp import Cisco

