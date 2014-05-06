"""
NetEngine SNMP OpenWRT backend
"""

__all__ = ['OpenWRT']


import binascii
from datetime import timedelta

from netengine.backends.snmp import SNMP


class OpenWRT(SNMP):
    """
    OpenWRT SNMP backend
    """

    def __str__(self):
        """ print a human readable object description """
        return u"<SNMP (OpenWRT): %s>" % self.host

    def validate(self):
        """
        raises NetEngineError exception if anything is wrong with the connection
        for example: wrong host, invalid community
        """
        # this triggers a connection which
        # will raise an exception if anything is wrong
        return self.name
    
    @property
    def os(self):
        """
        returns (os_name, os_version)
        """
        os_name = 'OpenWRT'
        os_version = self.get_value('1.3.6.1.2.1.1.1.0').split('#')[0].strip()
        return os_name, os_version

    @property
    def name(self):
        """
        returns a string containing the device name
        """
        return self.get_value('1.3.6.1.2.1.1.5.0')
    
    @property
    def uptime(self):
        """
        returns an integer representing the number of seconds of uptime
        """
        return int(self.get_value('1.3.6.1.2.1.1.3.0')) / 100
    
    @property
    def uptime_tuple(self):
        """
        returns (days, hours, minutes)
        """
        td = timedelta(seconds=self.uptime)
        
        return td.days, td.seconds//3600, (td.seconds//60)%60
    
    def _value_to_retrieve(self):
        value_to_retr = []
        tmp = self.next('1.3.6.1.2.1.2.2.1.1')[3]
        for i in range(len(tmp)):
            value_to_retr.append(int(tmp[i][0][1]))
        return value_to_retr
    
    def get_interfaces(self):
        """
        returns the list of all the interfaces of the device
        """
        interfaces = []
        value_to_get = '1.3.6.1.2.1.2.2.1.2.'
        for i in range (1,8):
            value_to_get1 = value_to_get+str(i)
            if value_to_get1:
                interfaces.append(self.get_value(value_to_get1))
        return filter(None,interfaces)
        
    @property
    def interfaces_MAC(self):
        """
        Returns an ordered dict with the hardware address of every interface
        """
        results = []
        mac1 = []
        mac = self.next('1.3.6.1.2.1.2.2.1.6.')[3]
        for i in range(1, len(mac) + 1):
            mac1.append(self.get_value('1.3.6.1.2.1.2.2.1.6.' + str(i)))
        mac_trans = []
        for i in mac1:
            mac_trans.append(':'.join(binascii.b2a_hex(i)[a:a+2] for a in range(0, 12, 2) if i != ""))
        for i in range(0, len(self.get_interfaces())):
            result = self._dict({
                "name" : self.get_interfaces()[i],
                "mac_address" : mac_trans[i]
            })
            results.append(result)
        return results
    
    @property
    def interfaces_mtu(self):
        """
        Returns an ordereed dict with the interface and its MTU
        """
        results = []
        starting = "1.3.6.1.2.1.2.2.1.2."
        tmp = list(starting)
        tmp[18] = str(4)
        to = ''.join(tmp)
        for i in self._value_to_retrieve():
            result = self._dict({
                "name" : self.get_value(starting + str(i)),
                "mtu" : int(self.get_value(to + str(i)))
            })
            results.append(result)
        return results
    
    @property
    def interfaces_speed(self):
        """
        Returns an ordered dict with the interface and ist speed in bps
        """
        results = []
        starting = "1.3.6.1.2.1.2.2.1.2."
        starting_speed = "1.3.6.1.2.1.2.2.1.5."
        for i in range(1, len(self.get_interfaces()) + 1):
            result = self._dict({
                "name" : self.get_value(starting + str(i)),
                "speed" : int(self.get_value(starting_speed + str(i)))
            })
            results.append(result)
        return results
    
    @property
    def interfaces_state(self):
        """
        Returns an ordereed dict with the interfaces and their state (up, down)
        """
        results = []
        starting = "1.3.6.1.2.1.2.2.1.2."
        operative = "1.3.6.1.2.1.2.2.1.8."  
        tmp = list(starting)
        tmp[18] = str(4)
        for i in self._value_to_retrieve():
            if self.get_value(starting + str(i)) != "" :
                if int(self.get_value(operative + str(i))) == 1:
                    result = self._dict({
                        "name" : self.get_value(starting + str(i)),
                        "state" : "up"
                    })
                    results.append(result)
                else:
                    result = self._dict({
                        "name" : self.get_value(starting + str(i)),
                        "state" : "down"
                    })
                    results.append(result)
            elif self.get_value(starting + str(i)) == "" :
                result = self._dict({
                        "name" : "",
                        "state" : ""
                    })
                results.append(result)
        return results
    
    @property
    def interfaces_bytes(self):
        """
        Returns an ordereed dict with the interface and its tx and rx octets (1 octet = 1 byte = 8 bits)
        """
        results = []
        starting = "1.3.6.1.2.1.2.2.1.2."
        starting_rx = "1.3.6.1.2.1.2.2.1.10."
        starting_tx = "1.3.6.1.2.1.2.2.1.16."
        for i in self._value_to_retrieve():
            result = self._dict({
                "name" : self.get_value(starting + str(i)),
                "tx" : int(self.get_value(starting_tx + str(i))),
                "rx" : int(self.get_value(starting_rx + str(i))),
            })
            results.append(result)
        return results
    
    @property
    def interfaces_type(self):
        """
        Returns an ordered dict with the interface type (e.g Ethernet, loopback)
        """
        types = {"6" : "ethernetCsmacd", "24" : "softwareLoopback", "131" : "tunnel"}
        results = []
        starting = "1.3.6.1.2.1.2.2.1.2."
        types_oid = "1.3.6.1.2.1.2.2.1.3."
        for i in self._value_to_retrieve():
            result = self._dict({
                "name" : self.get_value(starting + str(i)),
                "type" : types[self.get_value(types_oid + str(i))],
            })
            results.append(result)
        return results
        
    @property
    def interfaces_to_dict(self):
        """
        Returns an ordered dict with all the information available about the interface
        """
        results = []
        for i in range(0, len(self.get_interfaces())):
            result = self._dict({
                "name" : self.interfaces_MAC[i]['name'],
                "type" : self.interfaces_type[i]['type'],
                "mac_address" : self.interfaces_MAC[i]['mac_address'],
                "rx_bytes" : int(self.interfaces_bytes[i]['rx']),
                "tx_bytes" : int(self.interfaces_bytes[i]['tx']),
                "state" : self.interfaces_state[i]['state'],
                "mtu" : int(self.interfaces_mtu[i]['mtu']),
                "speed" : int(self.interfaces_speed[i]['speed'])
            })
            results.append(result)
        return results

    @property
    def RAM_total(self):
        """
        returns the total RAM of the device
        """
        return int(self.get_value("1.3.6.1.2.1.25.2.3.1.5.1"))
        
    def to_dict(self):
        return self._dict({
            "name": self.name,
            "type": "radio",
            "os": self.os[0],
            "os_version": self.os[1],
            "manufacturer": None,
            "model": None,
            "RAM_total": self.RAM_total,
            "uptime": self.uptime,
            "uptime_tuple": self.uptime_tuple,
            "interfaces": self.get_interfaces(),
            "antennas": [],
            "routing_protocols": None,
        })