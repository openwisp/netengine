
************
SNMP backend
************

SNMP
====

SNMP (Simple Network Management Protocol) is a network protocol very useful for retrieving info from a device.
All the information is retrieved by using codes called MIBs. All MIBs have a tree-like structure, every main information is the root and by adding more detail to the info
the tree gains more depth.
Obviously, by getting the smallest MIB which is "1" or simply " . " one can get all the tree.

The base SNMP backend contains the following methods (some internal methods are not documented and are subject to change in the future):

+--------------+------------------------------------------------------------------------------------------------------------------------------------------+
| **to_dict**  | Returns a dict containing monitoring information depending on the type of the device.                                                    |
|              | It follows the `NetJSON Devicemonitoring <https://netjson.org/rfc.html#name-devicemonitoring>`_ spec                                     |
+--------------+------------------------------------------------------------------------------------------------------------------------------------------+
| **to_json**  | Calls the `to_dict` method and returns a JSON string of the dict                                                                         |
+--------------+------------------------------------------------------------------------------------------------------------------------------------------+
| **validate** | Checks if connection with the device is working and raises `NetengineError` in case something is wrong                                   |
+--------------+------------------------------------------------------------------------------------------------------------------------------------------+

Initializing an SNMP backend class requires the following arguments:

+---------------+---------------------------------------------------------------------+
| **host**      | Management ip or hostname of the device                             |
+---------------+---------------------------------------------------------------------+
| **community** | Community string for the SNMP connection. Default value is 'public' |
+---------------+---------------------------------------------------------------------+
| **agent**     | Agent string for the SNMP connection                                |
+---------------+---------------------------------------------------------------------+
| **port**      | Port for the SNMP connection. Default value is `161`                |
+---------------+---------------------------------------------------------------------+

The SNMP backend provides support for 2 firmwares:
 * AirOS
 * OpenWRT

.. note::

    The data collected by Netengine is dependant on the OIDs available on your device. Some proprietary manufacturers may not
    provide the same information as others.

*****
AirOS
*****

With AirOS, Netengine is able to collect the following information which is returned in the
`NetJSON Devicemonitoring <https://netjson.org/rfc.html#name-devicemonitoring>`_ format:

+------------+------------------------------------------------------------------------------------------------------------+
| general    | - uptime: uptime of the device in seconds                                                                  |
|            | - local_time: local time of the device in timestamp                                                        |
+------------+------------------------------------------------------------------------------------------------------------+
| resources  | - load: array containing average load on the cpu in the past minute, 5 minutes and 15 minutes respectively |
|            | - memory:                                                                                                  |
|            |   - total: total memory in bytes                                                                           |
|            |   - buffered: buffered memory in bytes                                                                     |
|            |   - free: free memory in bytes                                                                             |
|            |   - cached: cached memory in bytes                                                                         |
|            | - swap:                                                                                                    |
|            |   - total: total swap storage in bytes                                                                     |
|            |   - free: free swap storage in bytes                                                                       |
+------------+------------------------------------------------------------------------------------------------------------+
| interfaces | Each interface is listed with the following information:                                                   |
|            |                                                                                                            |
|            | - name                                                                                                     |
|            | - type                                                                                                     |
|            | - statistics:                                                                                              |
|            |                                                                                                            |
|            |  - rx_bytes                                                                                                |
|            |  - tx_bytes                                                                                                |
+------------+------------------------------------------------------------------------------------------------------------+

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

To collect the whole json::
 device.to_json()

*******
OpenWRT
*******

With OpenWRT, Netengine is able to collect the following information which is returned in the
`NetJSON Devicemonitoring <https://netjson.org/rfc.html#name-devicemonitoring>`_ format:

+------------+----------------------------------------------------------+
| general    | - uptime: uptime of the device in seconds                |
|            | - local_time: local time of the device in timestamp      |
+------------+----------------------------------------------------------+
| resources  | - cpus: number of cpus on the device                     |
|            | - memory:                                                |
|            |   - total: total memory in bytes                         |
|            |   - shared: shared memory in bytes                       |
|            |   - used: used memory in bytes                           |
|            |   - free: free memory in bytes                           |
|            |   - cached: cached memory in bytes                       |
|            | - swap:                                                  |
|            |   - total: total swap storage in bytes                   |
|            |   - free: free swap storage in bytes                     |
+------------+----------------------------------------------------------+
| interfaces | Each interface is listed with the following information: |
|            |                                                          |
|            | - name: name of the interface (example: "eth0")          |
|            | - statistics:                                            |
|            |                                                          |
|            |  - mac                                                   |
|            |  - type                                                  |
|            |  - up                                                    |
|            |  - rx_bytes                                              |
|            |  - tx_bytes                                              |
|            |  - mtu                                                   |
|            |  - addresses:                                            |
|            |                                                          |
|            |   - family                                               |
|            |   - address                                              |
|            |   - mask                                                 |
+------------+----------------------------------------------------------+
| neighbors  | Each neighbor is listed with the following information:  |
|            | - mac: mac address of the neighbor                       |
|            | - state: state of the neighbor (REACHABLE/STALE/DELAY)   |
|            | - interface: interface of the neighbor                   |
|            | - ip: ip address of the neighbor                         |
+------------+----------------------------------------------------------+

OpenWRT example
===============

The same instructions typed above can be applied to OpenWRT itself, just remember to import the correct firmware by typing::

 from netengine.backends.snmp import OpenWRT
