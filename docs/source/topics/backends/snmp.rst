SNMP backend
============

SNMP
----

SNMP (Simple Network Management Protocol) retrieves information from a
device through a tree of object identifiers (OIDs) defined by management
information bases (MIBs).

The base SNMP backend contains the following methods (some internal
methods are not documented and are subject to change in the future):

============ =============================================================
**to_dict**  Returns a dict containing monitoring information depending on
             the type of the device. It follows the `NetJSON
             Devicemonitoring
             <https://netjson.org/rfc.html#name-devicemonitoring>`_ spec
**to_json**  Calls the `to_dict` method and returns a JSON string of the
             dict
**validate** Checks if connection with the device is working and raises
             `NetengineError` in case something is wrong
============ =============================================================

``to_dict`` and ``to_json`` enable ``autowalk`` by default, collecting the
required OIDs before serializing the result. To serialize an existing SNMP
dump without querying the device, call ``to_dict(snmpdump=dump,
autowalk=False)``.

Initializing an SNMP backend class requires the following arguments:

============= ==========================================================
**host**      Management ip or hostname of the device
**community** Community string for the SNMP connection. Default value is
              'public'
**agent**     Agent string for the SNMP connection
**port**      Port for the SNMP connection. Default value is `161`
============= ==========================================================

The SNMP backend provides support for 2 firmwares:
    - AirOS
    - OpenWRT

.. note::

    The data collected by Netengine is dependant on the OIDs available on
    your device. Some proprietary manufacturers may not provide the same
    information as others.

AirOS
=====

With AirOS, Netengine is able to collect the following information which
is returned in the `NetJSON Devicemonitoring
<https://netjson.org/rfc.html#name-devicemonitoring>`_ format:

- ``general``: uptime, local time, and hostname.
- ``hardware``: device model.
- ``operating_system``: name, description, and firmware version.
- ``resources``: CPU load, memory, and swap usage.
- ``interfaces``: name, MAC address, type, received bytes, and transmitted
  bytes.

AirOS example
-------------

::

    from netengine.backends.snmp import AirOS
    device = AirOS("10.40.0.130")
    device.name()
    'RM5PomeziaSNode'
    device.uptime()
    104405

We have just called two simple methods on **device**, but we can ask **device** for more specific values or portions of the SNMP tree not included in the API, just type::
    device.next("1.3.6")

Otherwise, if you want simply a value of the tree just type::
    device.get_value("oid_you_want_to_ask_for")

To collect the whole json::
    device.to_json()

OpenWRT
=======

With OpenWRT, Netengine is able to collect the following information which
is returned in the `NetJSON Devicemonitoring
<https://netjson.org/rfc.html#name-devicemonitoring>`_ format:

- ``general``: uptime, local time, and hostname.
- ``resources``: CPU count, memory, and swap usage.
- ``interfaces``: name, type, MAC address, state, traffic counters, MTU,
  and addresses.
- ``neighbors``: MAC address, state, interface, and IP address.

OpenWRT example
---------------

The same instructions typed above can be applied to OpenWRT itself. Import
it with ``from netengine.backends.snmp import OpenWRT`` and use the same
methods described for AirOS.
