"""
NetEngine SNMP Ubiquiti Air OS backend
"""

__all__ = ['AirOS']



from netengine.backends.http import HTTP



class AirOS(HTTP):
    """
    Ubiquiti AirOS HTTP backend
    """
    
    @property
    def firewall(self):
        """ returns firewall info about the device """
        return self.info['firewall']
    
    @property
    def host_info(self):
        """ return host info (uptime, hostname) """
        return self.info['host']
    
    @property
    def airview(self):
        """ returns airview state (0 if down, 1 if up) """
        return self.info['airview']
    
    @property
    def services(self):
        """ returns active services on the device (e.g dhcpd, ppoe, dhcpc) """
        return self.info['services']
    
    @property
    def interfaces(self):
        """ return the interfaces name of the device """
        names = []
        all = self.info['interfaces']
        
        for i in range(0, len(all)):
            names.append(all[i]['ifname'])
        return names
    
    @property
    def interfaces_properties(self):
        """ returns a dict which contains properties of every interface """
        interfaces_dict = {}
        interfaces = self.info['interfaces']
        
        for i in range(0, len(interfaces)):
            interfaces_dict[str(interfaces[i]['ifname'])] = interfaces[i]
            interfaces_dict[str(interfaces[i]['ifname'])].pop('ifname', None)
        return interfaces_dict
    

    
    
    
    