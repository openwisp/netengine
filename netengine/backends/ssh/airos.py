"""
Class to extract information from Ubiquiti AirOS devices
"""

__all__ = ['AirOS']


from netengine.backends.ssh import SSH


class AirOS(SSH):
    """
    Ubiquiti AirOS SSH backend
    """
    
    __ubntbox = None
    __systemcfg = None
    
    def __str__(self):
        """ print a human readable object description """
        return u"<SSH (Ubiquity AirOS): %s@%s>" % (self.username, self.host)
    
    @property
    def _ubntbox(self):
        """
        returns "ubntbox mca-status" output in a python dictionary
        """
        # get result if not present in memory yet
        if not self.__ubntbox:
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
        
            self.__ubntbox = info
        
        # return output
        return self.__ubntbox
    
    @property
    def _systemcfg(self):
        """
        return main system configuration in a python dictionary
        """
        # if config hasn't been retrieved yet do it now
        if not self.__systemcfg:
            output = self.run('cat /tmp/system.cfg')
        
            info = {}
            
            for line in output.split('\n'):
                parts = line.split('=')
                
                if len(parts) == 2:
                    info[parts[0]] = parts[1]
            
            self.__systemcfg = info
        
        # return config
        return self.__systemcfg
    
    @property
    def os(self):
        """ get OS string, return tuple with OS name and OS version """
        return ('AirOS', self._ubntbox['firmwareVersion'])
    
    @property
    def name(self):
        """ get device name """
        return self.run('uname -a').split(' ')[1]
    
    @property
    def model(self):
        """ get device model name, eg: Nanostation M5, Rocket M5 """
        return self._ubntbox['platform']
    
    @property
    def RAM_total(self):
        return int(self._ubntbox['memTotal'])
    
    @property
    def ethernet_standard(self):
        """ determine ethernet standard """
        if '100Mbps' in self._ubntbox['lanSpeed']:
            return 'fast'
        elif '1000Mbps' in self._ubntbox['lanSpeed']:
            return 'gigabit'
        elif '10Mbps' in self._ubntbox['lanSpeed']:
            return 'legacy'
        else:
            return None
    
    @property
    def ethernet_duplex(self):
        """ determine if ethernet interface is full-duplex or not """
        if 'Full' in self._ubntbox['lanSpeed']:
            return 'full'
        elif 'Half' in self._ubntbox['lanSpeed']:
            return 'half'
    
    @property
    def wireless_channel_width(self):
        """ retrieve wireless channel width """
        if '20' in self._systemcfg['radio.1.ieee_mode']:
            return 20
        elif '40' in self._systemcfg['radio.1.ieee_mode']:
            return 40
        else:
            return None
    
    @property
    def wireless_mode(self):
        """ retrieve wireless mode (AP/STA) """
        return self._ubntbox['wlanOpmode']
    
    @property
    def wireless_channel(self):
        """ retrieve wireless channel / frequency """
        return self._ubntbox['freq']
    
    @property
    def wireless_output_power(self):
        """ retrieve output power """
        return int(self._systemcfg['radio.1.txpower'])
    
    @property
    def wireless_dbm(self):
        """ get dbm """
        return self._ubntbox['signal']
    
    @property
    def wireless_noise(self):
        """ retrieve noise """
        return self._ubntbox['noise']
    
    def _filter_interfaces(self):
        """
        tmp
        """
        interfaces = self.get_interfaces()
        
        results = [] 
        
        for interface in interfaces:
            # if this is an interesting interface
            if interface['ip_address'] == '':
                continue
            
            result = None
            
            # is it Ethernet?
            if 'eth' in interface['interface']:
                
                result = self._dict({
                    "type": "ethernet",
                    "name": interface['interface'],
                    "mac_address": interface['hardware_address'],
                    "mtu": 1500,  # TODO
                    "standard": self.ethernet_standard,
                    "duplex": self.ethernet_duplex,
                    "tx_rate": None,
                    "rx_rate": None,
                    "ip": [
                        self._dict({
                            "version": 4,
                            "address": interface['ip_address']
                        })
                    ]
                })
            # is it Wireless?
            elif 'wlan' in interface['interface'] or 'ath' in interface['interface']:
                
                result = self._dict({
                    "type": "wireless",
                    "name": interface['interface'],
                    "mac_address": interface['hardware_address'],
                    "mtu": 1500,  # TODO
                    "standard": "802.11n",
                    "channel": self.wireless_channel,
                    "channel_width": self.wireless_channel_width,
                    "mode": self.wireless_mode,
                    "output_power": self.wireless_output_power,
                    "tx_rate": None,
                    "rx_rate": None,
                    "dbm": self.wireless_dbm,
                    "noise": self.wireless_noise,
                    "ip": [
                        self._dict({
                            "version": 4,
                            "address": interface['ip_address']
                        })
                    ],
                    "vap": [
                        self._dict({
                            "essid": "placeholder",
                            "bssid": "",
                            "encryption": ""
                        })
                    ]
                })
            else:
                # TODO!!! VPN, BRIDGES, VLANS, etc..
                pass
            
            if result:
                
                # check if it has an ipv6 address
                ipv6_address = self.get_ipv6_of_interface(interface['interface'])
                if ipv6_address:
                    # subtract netmask
                    ipv6_address = ipv6_address.split('/')[0]
                    result["ip"].append(self._dict({
                            "version": 6,
                            "address": ipv6_address
                    }))
                
                results.append(result)
        
        return results
    
    def _filter_routing_protocols(self):
        results = []
        
        olsr = self.olsr
        if olsr:
            results.append(self._dict({
                "name": "olsr",
                "version": olsr[0]
            }))
        
        # other routing protocols
        
        return results
    
    def to_dict(self):
        return self._dict({
            "name": self.name,
            "type": "radio",
            "os": self.os[0],
            "os_version": self.os[1],
            "manufacturer": "Ubiquiti Networks",
            "model": self.model,
            "RAM_total": self.RAM_total,
            "uptime": None,
            "uptime_tuple": None,
            "interfaces": self._filter_interfaces(),
            "antennas": [],
            "routing_protocols": self._filter_routing_protocols()
        })
