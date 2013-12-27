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
        return u"<SNMP (OpenWRT): %s>" % self.host
    
    #def validate(self):
    #    """
    #    raises NetEngineError exception if anything is wrong with the connection
    #    for example: wrong host, invalid community
    #    """
    #    self.name
    
    # TODO
