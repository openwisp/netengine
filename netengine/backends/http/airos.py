"""
NetEngine SNMP Ubiquiti Air OS backend
"""

__all__ = ['AirOS']


import json

try:
    import mechanize
except ImportError:
    raise ImportError('Mechanize library is not installed, install with: "pip install mechanize"')

from netengine.backends.http import HTTP


class AirOS(HTTP):
    """
    Ubiquiti AirOS HTTP backend
    """

    _status_cgi = None
    _iflist_cgi = None
    _sta_cgi = None

    @property
    def info(self):
        if not self._status_cgi:
            browser = mechanize.Browser()
            browser.set_handle_robots(False)   # ignore robots
            browser.addheaders = [('User-agent', 'Firefox')]
            response = browser.open("https://{host}/login.cgi?uri=/status.cgi".format(host=self.host))
            browser.form = list(browser.forms())[0]
            browser.select_form(nr = 0)
            browser.form['username'] = self.username
            browser.form['password'] = self.password
            request = browser.submit()
            result = json.loads(request.read())

            self._status_cgi = result

        return self._status_cgi

    @property
    def iflist(self):
        if not self._iflist_cgi:
            browser = mechanize.Browser()
            browser.set_handle_robots(False)   # ignore robots
            browser.addheaders = [('User-agent', 'Firefox')]
            response = browser.open("https://{host}/login.cgi?uri=/iflist.cgi".format(host=self.host))
            browser.form = list(browser.forms())[0]
            browser.select_form(nr = 0)
            browser.form['username'] = self.username
            browser.form['password'] = self.password
            request = browser.submit()
            result = json.loads(request.read())

            self._iflist_cgi = result

        return self._iflist_cgi

    @property
    def sta(self):
        if not self._sta_cgi:
            browser = mechanize.Browser()
            browser.set_handle_robots(False)   # ignore robots
            browser.addheaders = [('User-agent', 'Firefox')]
            response = browser.open("https://{host}/login.cgi?uri=/sta.cgi".format(host=self.host))
            browser.form = list(browser.forms())[0]
            browser.select_form(nr = 0)
            browser.form['username'] = self.username
            browser.form['password'] = self.password
            request = browser.submit()
            result = json.loads(request.read())

            self._sta_cgi = result

        return self._sta_cgi

    @property
    def name(self):
        """ returns the device name """
        return str(self.info['host']['hostname'])

    @property
    def firewall(self):
        """ returns firewall info about the device """
        return self.info['firewall']

    @property
    def host_info(self):
        """ return host info (uptime, hostname) """
        return self.info['host']

    @property
    def uptime(self):
        """ returns the device uptime time """
        return str(self.info['host']['uptime'])

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
            # interfaces_dict[str(interfaces[i]['ifname'])].pop('ifname', None)
        return interfaces_dict

    @property
    def wireless(self):
        """ returns all wireless info """
        return self.info['wireless']

    @property
    def wireless_stats(self):
        """ returns wireless stats """
        return self.info['wireless']['stats']

    @property
    def wireless_polling(self):
        """ returns wireless polling info """
        return self.info['wireless']['polling']

    @property
    def ssid(self):
        """ returns device's essid """
        return str(self.info['wireless']['essid'])

    @property
    def frequency(self):
        """ returns device operating freq """
        return str(self.info['wireless']['frequency'])

    @property
    def rates(self):
        """ returns antenna tx and rx rates as list """
        rate = []
        rate.append(float(self.info['wireless']['txrate']))
        rate.append(float(self.info['wireless']['rxrate']))
        return rate

    @property
    def ap_addr(self):
        """ returns tha AP MAC address """
        return str(self.info['wireless']['apmac'])

    @property
    def noisefloor(self):
        """ returns the noisefloor (dB)"""
        return int(self.info['wireless']['noisef'])

    @property
    def mode(self):
        """ returns the mode the device is working """
        return str(self.info['wireless']['mode'])

    @property
    def uptime_tuple(self):
        """ returns a tuple (days, hours, minutes) """
        uptime = self.uptime
        seconds = int(uptime)
        minutes = int(seconds // 60)
        hours = int(minutes // 60)
        days = int(hours // 24)
        output = days, hours, minutes
        return output

    @property
    def interface_ip(self):
        key = []
        allinfo = self.iflist
        dict_interface = {}
        for interface in allinfo["interfaces"]:
            if "ipv4" in interface.keys():
                for key, values in interface.iteritems():
                    dict_interface[key]=values
        return dict_interface

    @property
    def connected_stations(self):
        """ return a list of connected stations """
        results = []
        for stations in self.sta:
            results.append(self._dict({
                "station" : stations
            }))
        return results

    def format_interfaces(self):
        list_of_dictionaries = []
        interface_list = self.iflist["interfaces"];
        for i in range(0, len(interface_list)):
            dictionary = {}
            if interface_list[i]["ifname"] in self.interface_ip.values():
                dictionary[interface_list[i]["ifname"]] = interface_list[i]
                list_of_dictionaries.append(dictionary)
        return list_of_dictionaries

    def to_dict(self):
        return self._dict({
            "name": str(self.name),
            "ssid": str(self.ssid),
            "type": "radio",
            "mode": self.mode,
            "uptime": self.uptime,
            "uptime_tuple": self.uptime_tuple,
            "antennas": [],
            "tx_rate": self.rates[0],
            "rx_rate": self.rates[1],
            "interfaces": self.format_interfaces(),
            "connected_stations": self.connected_stations,
            "frequency": str(self.frequency),
            "wireless_dbm": str(self.noisefloor),
        })
