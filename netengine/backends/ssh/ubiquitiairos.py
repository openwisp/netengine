"""
Class to extract information from Ubiquiti AirOS devices
"""

__all__ = ['UbiquitiAirOS']


from netengine.backends.ssh import SSH


class UbiquitiAirOS(SSH):
    """
    Ubiquiti AirOS SSH backend
    """
    
    _ubntbox = None
    _systemcfg = None
    
    def __str__(self):
        """ print a human readable object description """
        return u"<SSH (Ubiquity AirOS): %s@%s>" % (self.username, self.host)
    
    @property
    def ubntbox(self):
        """
        returns "ubntbox mca-status" output in a python dictionary
        """
        # get result if not present in memory yet
        if not self._ubntbox:
            output = self.run('ubntbox mca-status')
            
            info = {}
            
            for line in output.split('\r\n'):
                parts = line.split('=')
                
                # main device info
                if len(parts) > 2:
                    subparts = line.split(',')
                    for subpart in subparts:
                        key, value = subpart.split('=')
                        info[key] = value
                # all other stuff
                elif len(parts) == 2:
                    info[parts[0]] = parts[1]
                else:
                    pass
        
            self._ubntbox = info
        
        # return output
        return self._ubntbox
    
    @property
    def systemcfg(self):
        """
        return main system configuration in a python dictionary
        """
        # if config hasn't been retrieved yet do it now
        if not self._systemcfg:
            output = self.run('cat /tmp/system.cfg')
        
            info = {}
            
            for line in output.split('\n'):
                parts = line.split('=')
                
                if len(parts) == 2:
                    info[parts[0]] = parts[1]
            
            self._systemcfg = info
        
        # return config
        return self._systemcfg
    
    @property
    def os(self):
        """ get OS string, return tuple with OS name and OS version """
        return ('AirOS', self.ubntbox['firmwareVersion'])
    
    @property
    def name(self):
        """ get device name """
        return self.run('uname -a').split(' ')[1]
    
    @property
    def model(self):
        """ get device model name, eg: Nanostation M5, Rocket M5 """
        return self.ubntbox['platform']
    
    @property
    def RAM_total(self):
        return int(self.ubntbox['memTotal'])
    
    @property
    def ethernet_standard(self):
        """ determine ethernet standard """
        if '100Mbps' in self.ubntbox['lanSpeed']:
            return 'fast'
        elif '1000Mbps' in self.ubntbox['lanSpeed']:
            return 'gigabit'
        elif '10Mbps' in self.ubntbox['lanSpeed']:
            return 'legacy'
        else:
            return None
    
    @property
    def ethernet_duplex(self):
        """ determine if ethernet interface is full-duplex or not """
        if 'Full' in self.ubntbox['lanSpeed']:
            return 'full'
        elif 'Half' in self.ubntbox['lanSpeed']:
            return 'half'
    
    @property
    def wireless_channel_width(self):
        """ retrieve wireless channel width """
        if '20' in self.systemcfg['radio.1.ieee_mode']:
            return 20
        elif '40' in self.systemcfg['radio.1.ieee_mode']:
            return 40
        else:
            return None
    
    @property
    def wireless_mode(self):
        """ retrieve wireless mode (AP/STA) """
        return self.ubntbox['wlanOpmode']
    
    @property
    def wireless_channel(self):
        """ retrieve wireless channel / frequency """
        return self.ubntbox['freq']
    
    @property
    def wireless_output_power(self):
        """ retrieve output power """
        return int(self.systemcfg['radio.1.txpower'])
    
    @property
    def wireless_dbm(self):
        """ get dbm """
        return self.ubntbox['signal']
    
    @property
    def wireless_noise(self):
        """ retrieve noise """
        return self.ubntbox['noise']