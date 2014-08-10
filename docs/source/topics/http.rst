
**************
HTTP backend
**************


This backend is made upon the service provided by AirOS devices, in fact the have an administration page with some dedicated url to take info in json format.

This is what was used to this backend. Since this kind of service is available only for AirOS, this is the only supported firmware.


AirOS example
==============

::

 from netengine.backends.snmp import AirOS
 device = AirOS("10.40.0.130")
 device.name
 'RM5PomeziaSNode'

Many times you can have to deal with an antenna in mode AP (Access Point) with multiple client attached, in this case the backend gives the list of all connected stations by
simply typing::

 device.connected_stations

to have the list of all connected stations with some interesting parameters.
