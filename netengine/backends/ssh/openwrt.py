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
        output = self.run('iwinfo | grep -i hardware')

        if "not found" in output:
            return None

        # will return something like
        # Hardware: 168C:002A 0777:E805 [Ubiquiti Bullet M5]
        # and we'll extract only the string between square brackets
        return output.split('[')[1].replace(']','')

    @property
    def wireless_mode(self):
        """ retrieve wireless mode (AP/STA) """

        output = self.run("iwconfig 2>/dev/null | grep Mode | awk '{print $4}' | awk -F ':' '{print $2}'")
        output = output.strip()

        if output == "Master":
            return "ap"
        else:
            return "sta"

    @property
    def RAM_total(self):
        return int(self.run("cat /proc/meminfo | grep MemTotal | awk '{print $2}'"))

    @property
    def uptime(self):
        """
        returns an integer representing the number of seconds of uptime
        """
        output = self.run('cat /proc/uptime')
        seconds = float(output.split()[0])
        return int(seconds)

    @property
    def uptime_tuple(self):
        """
        Return a tuple (days, hours, minutes)
        """
        uptime = float(self.run('cat /proc/uptime').split()[0])
        seconds = int(uptime)
        minutes = int(seconds // 60)
        hours = int(minutes // 60)
        days = int(hours // 24)
        output = days, hours, minutes
        return output

    def _filter_interfaces(self):
        interfaces = self.get_interfaces()
        results = []

        for interface in interfaces:
            if interface.get('interface', False) is False:
                continue

            elif 'eth' in interface['interface']:
                result = self._dict({
                    "type" : "ethernet",
                    "name" : interface['interface'],
                    "mac_address" : interface['hardware_address'],
                    "mtu" : 1500,
                    "standard" : None,
                    "duplex" : None,
                    "tx_rate" : None,
                    "ip" :[
                        self._dict({
                            "version" : 4,
                            "address" : interface['ip_address']
                        })
                    ]
                })

            if result:
                results.append(result)

        return results

    def _filter_routing_protocols(self):
        results = []
        olsr = self.olsr
        if olsr:
            results.append(self._dict({
            "name" : "olsr",
            "version" : olsr[0]
            }))
        return results

    def to_dict(self):
        return self._dict({
            "name": self.name,
            "type": "radio",
            "os": self.os[0],
            "os_version": self.os[1],
            "manufacturer": self.get_manufacturer(),
            "model": self.model,
            "RAM_total": self.RAM_total,
            "uptime": self.uptime,
            "uptime_tuple": self.uptime_tuple,
            "interfaces": self._filter_interfaces(),
            "antennas": [],
            "routing_protocols": self._filter_routing_protocols(),
        })
