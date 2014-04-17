"""
NetEngine SNMP Ubiquiti Air OS backend
"""

__all__ = ['AirOS']


from datetime import timedelta
from netengine.backends.snmp import SNMP


class AirOS(SNMP):
    """
    Ubiquiti AirOS SNMP backend
    """
    
    def __str__(self):
        """ print a human readable object description """
        return u"<SNMP (Ubiquity AirOS): %s>" % self.host
    
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
        os_name = 'AirOS'
        os_version = self.get_value('1.3.6.1.2.1.1.1.0').split('#')[0].strip()
        return os_name, os_version
    
    @property
    def name(self):
        """
        returns a string containing the device name
        """
        return self.get_value('1.3.6.1.2.1.1.5.0')
    
    @property
    def model(self):
        """
        returns a string containing the device model
        """
        oids = ['1.2.840.10036.3.1.2.1.3.5','1.2.840.10036.3.1.2.1.3.8']
        for oid in oids:
            model = self.get_value(oid)
            if model != '':
                return model
    
    @property
    def firmware(self):
        """
        returns a string containing the device firmware
        """
        oids = ['1.2.840.10036.3.1.2.1.4.5','1.2.840.10036.3.1.2.1.4.8']
        for oid in oids:
            tmp = self.get_value(oid).split('.')
            if tmp != None:
                length = len(tmp)
                i = 0
                for piece in tmp:
                    if "v" in piece:
                        return 'AirOS ' + '.'.join(tmp[i:length])
                    i = i + 1
        
    @property
    def manufacturer(self):
        """
        returns a string containing the device manufacturer
        """
        oids = ['1.2.840.10036.3.1.2.1.2.5','1.2.840.10036.3.1.2.1.2.8']
        for oid in oids:
            manufacturer = self.get_value(oid)
            if manufacturer != '':
                return manufacturer
    
    @property
    def ssid(self):
        """
        returns a string containing the wireless ssid
        """
        return self.get_value('1.2.840.10036.1.1.1.9.8')
    
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
    
    @property
    def interfaces_number(self):
        """
        Returns the number of the network interfaces
        """
        return int(self.get_value('1.3.6.1.2.1.2.1.0'))  
    
    @property
    def get_interfaces(self):
        """
        returns the list of all the interfaces of the device
        """
        interfaces = []
        value_to_get = '1.3.6.1.2.1.2.2.1.2.'
        for i in range (1,10):
            value_to_get1 = value_to_get+str(i)
            if value_to_get1:
                interfaces.append(self.get_value(value_to_get1))
        return filter(None,interfaces)
    
    @property
    def get_interfaces_mtu(self):
        """
        Returns an ordereed dict with the interface and its MTU
        """
        results = []
        starting = "1.3.6.1.2.1.2.2.1.2."
        tmp = list(starting)
        tmp[18] = str(4)
        to = ''.join(tmp)
        for i in range(1,10):
            if self.get_value(starting + str(i)) != "":
                result = self._dict({"interface" : self.get_value(starting + str(i)),
                                     "mtu" : self.get_value(to + str(i))})
                results.append(result)
        return results
                
    @property
    def get_signal_strength(self):
        """
        returns the signal strength for the older tested version of AirOS
        """
        sign = self.get_value('1.3.6.1.4.1.14988.1.1.1.1.1.4.8')
        if sign != '':
            return int(sign)
    
    @property
    def RAM_total(self):
        """
        Returns the total RAM of the device
        """
        total = self.get_value('1.3.6.1.4.1.10002.1.1.1.1.1.0')
        return int(total)
    
    @property
    def RAM_free(self):
        """
        Returns the free RAM of the device
        """
        free = self.get_value('1.3.6.1.4.1.10002.1.1.1.1.2.0')
        return int(free)
    
    def to_dict(self):
        return self._dict({
            "name": self.name,
            "type": "radio",
            "os": self.os[0],
            "os_version": self.os[1],
            "manufacturer": self.manufacturer,
            "model": self.model,
            "RAM_total": self.RAM_total,
            "RAM_free" : self.RAM_free,
            "uptime": self.uptime,
            "uptime_tuple": self.uptime_tuple,
            "interfaces": self.get_interfaces,
            "antennas": [],
            "routing_protocols": None,
        })