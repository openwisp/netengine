from cached_property import cached_property

from netengine.backends.ssh import SSH


__all__ = ['AirOS']


class AirOS(SSH):
    """
    Ubiquiti AirOS SSH backend
    Version 5.5.8
    """

    def __str__(self):
        """ print a human readable object description """
        return u"<SSH (Ubiquity AirOS): %s@%s>" % (self.username, self.host)

    @cached_property
    def _ubntbox(self):
        """
        returns "ubntbox mca-status" output in a python dictionary
        """
        output = self.run('ubntbox mca-status')
        info = {}
        # loop over output
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
        # return dictionary
        return info

    @cached_property
    def _systemcfg(self):
        """
        return main system configuration in a python dictionary
        """
        output = self.run('cat /tmp/system.cfg')
        info = {}
        # parse lines
        for line in output.split('\n'):
            parts = line.split('=')
            # if subvalues
            if len(parts) == 2:
                # use sub dicttionaries
                info[parts[0]] = parts[1]
        # return dictionary
        return info

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
        wireless_interfaces = self.iwconfig()
        interfaces = self.ifconfig()
        results = []
        # loop over interfaces
        for interface in interfaces:
            # is it Ethernet?
            if 'eth' in interface['name']:
                interface['type'] = 'ethernet'
            # is it Wireless?
            elif 'wlan' in interface['name'] or 'ath' in interface['name']:
                interface['type'] = 'wireless'
                interface['wireless'] = {
                    "channel": self.wireless_channel,
                    "channel_width": self.wireless_channel_width,
                    "mode": self.wireless_mode,
                    "tx_power": self.wireless_output_power,
                    "dbm": self.wireless_dbm,
                    "noise": self.wireless_noise
                }
                # merge with iwconfig
                for wireless_if in wireless_interfaces:
                    if wireless_if['name'] == interface['name']:
                        interface['wireless'].update(wireless_if['wireless'])
            # append result to list of interfaces
            results.append(interface)
        # return results
        return results

    def _filter_routing_protocols(self):
        results = []
        if self.olsr:
            results.append(self._dict({
                "name": "olsr",
                "version": self.olsr[0]
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
            "routing_protocols": self._filter_routing_protocols()
        })
