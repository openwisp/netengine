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
    
    # TODO
