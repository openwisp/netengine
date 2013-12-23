"""
Class to extract information from  OpenWRT devices
"""

__all__ = ['OpenWRT']


from netengine.backends.ssh import SSH


class OpenWRT(SSH):
    """
    OpenWRT SSH backend
    """
    
    def __str__(self):
        """ print a human readable object description """
        return u"<SSH (OpenWRT): %s@%s>" % (self.username, self.host)
    
    @property
    def name(self):
        """ get device name """
        return self.run('uname -a').split(' ')[1]
    
    @property
    def os(self):
        """ get os name and version, return as tuple """
        # cache command output
        output = self.run('cat /etc/openwrt_release')
        
        # init empty dict
        info = {}
        
        # loop over lines of output
        # parse output and store in python dict
        for line in output.split('\n'):
            # tidy up before filling the dictionary
            key, value = line.split('=')
            key = key.replace('DISTRIB_', '').lower()
            value = value.replace('"', '')
            # fill!
            info[key] = value
        
        os = info['id']
        version = info['release']
        
        if info['description']:
            
            if info['revision']:
                additional_info = "%(description)s, %(revision)s" % info
            else:
                additional_info = "%(description)s" % info
            
            # remove redundant OpenWRT occuerrence
            additional_info = additional_info.replace('OpenWrt ', '')
            
            version = "%s (%s)" % (version, additional_info)
       
        return (os, version)
    
    @property
    def model(self):
        """ get device model name, eg: Nanostation M5, Rocket M5 """
        output = output = self.run('iwinfo | grep -i hardware')
        # will return something like
        # Hardware: 168C:002A 0777:E805 [Ubiquiti Bullet M5]
        # and we'll extract only the string between square brackets
        return output.split('[')[1].replace(']','')
    
    @property
    def RAM_total(self):
        return 0
    
    @property
    def ethernet_standard(self):
        """ determine ethernet standard """
        return 'fast'
    
    @property
    def ethernet_duplex(self):
        """ determine if ethernet interface is full-duplex or not """
        return 'duplex'
    
    @property
    def wireless_mode(self):
        """ retrieve wireless mode (AP/STA) """
        return 'ap'
    
    @property
    def wireless_channel(self):
        """ retrieve wireless channel / frequency """
        return '2412'
    
    @property
    def wireless_channel_width(self):
        """ retrieve wireless channel width """
        return '20'
    
    @property
    def wireless_output_power(self):
        """ retrieve output power """
        return None
    
    @property
    def wireless_dbm(self):
        """ get dbm """
        return None
    
    @property
    def wireless_noise(self):
        """ retrieve noise """
        return None