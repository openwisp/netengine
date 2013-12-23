"""
NetEngine SNMP OpenWRT backend
"""

__all__ = ['OpenWRT']


from netengine.backends.snmp import SNMP


class OpenWRT(SNMP):
    """
    OpenWRT SNMP backend
    """
    
    
    def __str__(self):
        """ print a human readable object description """
        return u"<SNMP (OpenWRT): %s-%s>" % (self.host, self.community)
    
    @property
    def olsr(self):
        """
        should return tuple with version and url if OLSR is installed
        should return None if not installed
        """
        raise NotImplementedError('Not implemented')
    
    @property
    def os(self):
        """
        Not Implemented
        
        should return a tuple in which
        the first element is the OS name and
        the second element is the OS version
        """
        raise NotImplementedError('Not implemented')
    
    @property
    def name(self):
        """
        Not Implemented
        
        should return a string containing the device name
        """
        raise NotImplementedError('Not implemented')
    
    @property
    def model(self):
        """
        Not Implemented
        
        should return a string containing the device model
        """
        raise NotImplementedError('Not implemented')
    
    @property
    def RAM_total(self):
        """
        Not Implemented
        
        should return a string containing the device RAM in bytes
        """
        raise NotImplementedError('Not implemented')
    
    @property
    def ethernet_standard(self):
        """
        Not Implemented
        """
        raise NotImplementedError('Not implemented')
    
    @property
    def ethernet_duplex(self):
        """
        Not Implemented
        """
        raise NotImplementedError('Not implemented')
    
    @property
    def wireless_channel_width(self):
        """
        Not Implemented
        """
        raise NotImplementedError('Not implemented')
    
    @property
    def wireless_mode(self):
        """
        Not Implemented
        """
        raise NotImplementedError('Not implemented')
    
    @property
    def wireless_channel(self):
        """
        Not Implemented
        """
        raise NotImplementedError('Not implemented')
    
    @property
    def wireless_output_power(self):
        """
        Not Implemented
        """
        raise NotImplementedError('Not implemented')
    
    @property
    def wireless_dbm(self):
        """
        Not Implemented
        """
        raise NotImplementedError('Not implemented')
    
    @property
    def wireless_noise(self):
        """
        Not Implemented
        """
        raise NotImplementedError('Not implemented')