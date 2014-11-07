"""
Class to extract information from  OpenWRT devices
"""

__all__ = ['OpenWRT']


from netengine.backends.ssh import SSH
import json


class OpenWRT(SSH):
    """
    OpenWRT SSH backend
    """

    _ubus_dict = {}
    _iwinfo_dict = {}

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

        if info.get('description'):
            if info.get('revision'):
                additional_info = "%(description)s, %(revision)s" % info
            else:
                additional_info = "%(description)s" % info
            # remove redundant OpenWRT occuerrence
            additional_info = additional_info.replace('OpenWrt ', '')
            version = "%s (%s)" % (version, additional_info)
        return (os, version)

    @property
    def ubus_dict(self):
        if not self._ubus_dict:
            self._ubus_dict = json.loads(self.run('ubus call network.device status'))
        return self._ubus_dict

    @property
    def _ubus_interface_infos(self):
        """
        returns a list of dict with infos about the interfaces
        """
        list = []
        for interface in self.run('ubus list').split():
            if "network.interface." in interface:
                list.append(json.loads(self.run('ubus call '+ interface + ' status')))
        return list

    @property
    def interfaces_to_dict(self):
        for interface in self._ubus_interface_infos:
            for key, values in interface.iteritems():
                self.ubus_dict[interface["l3_device"]][str(key)] = values
        return self.ubus_dict

    @property
    def model(self):
        """ get device model name, eg: Nanostation M5, Rocket M5 """
        output = self.run('iwinfo | grep -i hardware')
        # will return something like
        # Hardware: 168C:002A 0777:E805 [Ubiquiti Bullet M5]
        # and we'll extract only the string between square brackets
        try:
            return output.split('[')[1].replace(']','')
        except IndexError:
            return None

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
    def manufacturer(self):
        """
        returns a string representing the manufacturer of the device
        """
        # returns first not None value
        for interface in self.ubus_dict.keys():
            # ignore loopback interface
            if interface != "lo":
                mac_address = self.ubus_dict[interface]['macaddr']
                manufacturer = self.get_manufacturer(mac_address)
                if manufacturer:
                    return manufacturer

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

    def _filter_radio_interfaces(self):
        """
        returns informations about wireless interfaces as per iw station wlanX dump
        """
        iwinfo_result = self.run('iw wlan0 station dump')
        dictionary = {}
        result = iwinfo_result.split("\t")
        dictionary["Station"] = result[0].strip()
        key  = result[1::2]
        value  = result[2::2]
        try:
            for i in range (0, len(key)):
                dictionary[key[i].strip()] = str(value[i].strip())
        except Exception:
            pass
        return dictionary

    def _filter_radio(self):
        """
        returns a dictionary containing the information extracted from iwinfo <device> info
        """
        dictionary = {}
        # in case there is no wireless interface
        if not "wlan0" in self.ubus_dict:
            return dictionary

        iwinfo_result = self.run('iwinfo wlan0 info')
        lines = iwinfo_result.split("\n")
        char_occurrence = lines[0].find("ESSID")
        first_line = lines[0][char_occurrence:]
        key = first_line.split(":")[0].lower()
        value = first_line.split(":")[1].strip().replace(" ", "-")
        value = value.replace('"', "")
        dictionary[key] = value
        for line in lines[1:]:
            if line.count(": ") == 2:
                partial =  line.strip().split("  ")
                for element in partial:
                    key = element.split(":")[0].lower().replace(" ", "-")
                    value = element.split(":")[1].strip()
                    if "(" and ")" in key:
                        key = key.replace("(", "")
                        key = key.replace(")", "")
                        dictionary[key] = value
                    dictionary[key] = value
            else:
                key = line.split(":")[0].strip().lower().replace(" ", "-")
                value = line.split(":")[1].strip()
                if "(" and ")" in key:
                    key = key.replace("(", "")
                    key = key.replace(")", "")
                    dictionary[key] = value
                dictionary[key] = value
        return dictionary

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
            "manufacturer": self.manufacturer,
            "model": self.model,
            "RAM_total": self.RAM_total,
            "uptime": self.uptime,
            "uptime_tuple": self.uptime_tuple,
            "interfaces": self.interfaces_to_dict,
            "antennas": [],
            "routing_protocols": self._filter_routing_protocols()
        })
