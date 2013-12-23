"""
SSH base class
"""

__all__ = ['SSH']


from pysnmp.entity.rfc3413.oneliner import cmdgen

from netengine.exceptions import NetEngineError


class SNMP(object):
    """
    SNMP base backend
    """
    
    def __init__(self, host, community='public', agent='my-agent', port=161):
        """
        :host string: required
        :community string: defaults to public
        :agent string: defaults to my-agent
        :port integer: defaults to 161
        """
        self.host = host
        self.community = cmdgen.CommunityData(agent, community, 0)
        self.transport = cmdgen.UdpTransportTarget((host, port))
        self.port = port
    
    def __str__(self):
        """ prints a human readable object description """
        return "<SNMP: %s>" % self.host
    
    def __repr__(self):
        """ returns unicode string represantation """
        return self.__str__()
    
    def __unicode__(self):
        """ unicode __str__() for python2.7 """
        return unicode(self.__str__())
    
    @property
    def _command(self):
        """
        alias to cmdgen.CommandGenerator()
        """
        return cmdgen.CommandGenerator()
    
    def _oid(self, oid):
        """
        returns valid oid value to be passed to getCmd() or nextCmd()
        """
        if type(oid) not in (str, unicode, tuple, list):
            raise AttributeError('get accepts only strings, tuples or lists')
        # allow string representations of oids with commas ,
        elif isinstance(oid, basestring):
            # ignore spaces
            oid = oid.replace(' ', '').replace(',', '.')
        # convert lists and tuples into strings
        else:
            # convert each list item to string
            oid = [str(element) for element in oid]
            oid = '.'.join(oid)
        
        # ensure is string (could be unicode)
        return str(oid)
    
    def get(self, oid):
        """
        alias to cmdgen.CommandGenerator().getCmd
        :oid string|tuple|list: string, tuple or list representing the OID to get
        
        example of valid oid parameters:
            * "1,3,6,1,2,1,1,5,0"
            * "1, 3, 6, 1, 2, 1, 1, 5, 0"
            * "1.3.6.1.2.1.1.5.0"
            * [1, 3, 6, 1, 2, 1, 1, 5, 0]
            * (1, 3, 6, 1, 2, 1, 1, 5, 0)
        """
        return self._command.getCmd(self.community, self.transport, self._oid(oid))
    
    def next(self, oid):
        """
        alias to cmdgen.CommandGenerator().nextCmd
        :oid string|tuple|list: string, tuple or list representing the OID to get
        
        example of valid oid parameters:
            * "1,3,6,1,2,1,1,5,0"
            * "1, 3, 6, 1, 2, 1, 1, 5, 0"
            * "1.3.6.1.2.1.1.5.0"
            * [1, 3, 6, 1, 2, 1, 1, 5, 0]
            * (1, 3, 6, 1, 2, 1, 1, 5, 0)
        """
        return self.command.nextCmd(self.community, self.transport, self._oid(oid))
    
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