"""
NetEngine SNMP OpenWRT backend
"""

__all__ = ['OpenWRT']


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
    
    @property
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
            "interfaces": self.get_interfaces,
            "antennas": [],
            "routing_protocols": None,
        })