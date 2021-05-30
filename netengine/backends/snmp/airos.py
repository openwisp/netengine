"""
NetEngine SNMP Ubiquiti Air OS backend
"""

__all__ = ['AirOS']


import binascii
from datetime import timedelta

from netengine.backends.snmp import SNMP


class AirOS(SNMP):
    """
    Ubiquiti AirOS SNMP backend
    """

    _oid_to_retrieve = '1.3.6.1.2.1.1.9.1.1'

    def __str__(self):
        """ print a human readable object description """
        return u"<SNMP (Ubiquity AirOS): %s>" % self.host

    def validate(self):
        """
        raises NetEngineError exception if
        anything is wrong with the connection
        for example: wrong host, invalid community
        """
        # this triggers a connection which
        # will raise an exception if anything is wrong
        return self.name

    @property
    def os(self):
        """
        returns (os_name, os_version)
        """
        os_name = 'AirOS'
        os_version = self.get_value('1.3.6.1.2.1.1.1.0').split('#')[0].strip()
        return os_name, os_version

    @property
    def name(self):
        """
        returns a string containing the device name
        """
        return self.get_value('1.3.6.1.2.1.1.5.0')

    @property
    def model(self):
        """
        returns a string containing the device model
        """
        oids = ['1.2.840.10036.3.1.2.1.3.5', '1.2.840.10036.3.1.2.1.3.8']
        for oid in oids:
            model = self.get_value(oid)
            if model != '':
                return model

    @property
    def firmware(self):
        """
        returns a string containing the device firmware
        """
        oids = ['1.2.840.10036.3.1.2.1.4.5', '1.2.840.10036.3.1.2.1.4.8']
        for oid in oids:
            tmp = self.get_value(oid).split('.')
            if tmp is not None:
                length = len(tmp)
                i = 0
                for piece in tmp:
                    if "v" in piece:
                        return 'AirOS ' + '.'.join(tmp[i:length])
                    i = i + 1

    @property
    def manufacturer(self):
        return self.get_manufacturer(self.interfaces_MAC[1]['mac_address'])

    @property
    def ssid(self):
        """
        returns a string containing the wireless ssid
        """
        oids = ['1.2.840.10036.1.1.1.9.5', '1.2.840.10036.1.1.1.9.8']
        for oid in oids:
            if self.get_value(oid) != '':
                return self.get_value(oid)

    @property
    def uptime(self):
        """
        returns an integer representing the number of seconds of uptime
        """
        return int(self.get_value('1.3.6.1.2.1.1.3.0')) / 100

    @property
    def uptime_tuple(self):
        """
        returns (days, hours, minutes)
        """
        td = timedelta(seconds=self.uptime)

        return td.days, td.seconds//3600, (td.seconds//60) % 60

    @property
    def interfaces_number(self):
        """
        Returns the number of the network interfaces
        """
        return int(self.get_value('1.3.6.1.2.1.2.1.0'))

    _interfaces = None

    def get_interfaces(self):
        """
        returns the list of all the interfaces of the device
        """
        if self._interfaces is None:
            interfaces = []
            value_to_get = '1.3.6.1.2.1.2.2.1.2.'

            for i in self._value_to_retrieve():
                value_to_get1 = value_to_get+str(i)
                if value_to_get1:
                    interfaces.append(self.get_value(value_to_get1))

            self._interfaces = interfaces

        return self._interfaces

    _interfaces_mtu = None

    @property
    def interfaces_mtu(self):
        """
        Returns an ordereed dict with the interface and its MTU
        """
        if self._interfaces_mtu is None:
            results = []
            starting = "1.3.6.1.2.1.2.2.1.2."
            tmp = list(starting)
            tmp[18] = str(4)
            to = ''.join(tmp)

            for i in self._value_to_retrieve():
                result = self._dict({
                    "name": self.get_value(starting + str(i)),
                    "mtu": int(self.get_value(to + str(i)))
                })
                results.append(result)

            self._interfaces_mtu = results

        return self._interfaces_mtu

    _interfaces_state = None

    @property
    def interfaces_state(self):
        """
        Returns an ordereed dict with the interfaces and their state (up, down)
        """
        if self._interfaces_state is None:
            results = []
            starting = "1.3.6.1.2.1.2.2.1.2."
            operative = "1.3.6.1.2.1.2.2.1.8."
            tmp = list(starting)
            tmp[18] = str(4)
            for i in self._value_to_retrieve():
                if self.get_value(starting + str(i)) != "":
                    if int(self.get_value(operative + str(i))) == 1:
                        result = self._dict({
                            "name": self.get_value(starting + str(i)),
                            "state": "up"
                        })
                    else:
                        result = self._dict({
                            "name": self.get_value(starting + str(i)),
                            "state": "down"
                        })
                elif self.get_value(starting + str(i)) == "":
                    result = self._dict({
                        "name": "",
                        "state": ""
                    })
                # append result to list
                results.append(result)

            self._interfaces_state = results

        return self._interfaces_state

    _interfaces_speed = None

    @property
    def interfaces_speed(self):
        """
        Returns an ordered dict with the interface and ist speed in bps
        """
        if self._interfaces_speed is None:
            results = []
            starting = "1.3.6.1.2.1.2.2.1.2."
            starting_speed = "1.3.6.1.2.1.2.2.1.5."

            for i in self._value_to_retrieve():
                result = self._dict({
                    "name": self.get_value(starting + str(i)),
                    "speed": int(self.get_value(starting_speed + str(i)))
                })
                results.append(result)

            self._interfaces_speed = results

        return self._interfaces_speed

    _interfaces_bytes = None

    @property
    def interfaces_bytes(self):
        """
        Returns an ordereed dict with the interface
        and its tx and rx octets (1 octet = 1 byte = 8 bits)
        """
        if self._interfaces_bytes is None:
            results = []
            starting = "1.3.6.1.2.1.2.2.1.2."
            starting_rx = "1.3.6.1.2.1.2.2.1.10."
            starting_tx = "1.3.6.1.2.1.2.2.1.16."

            for i in self._value_to_retrieve():
                result = self._dict({
                    "name": self.get_value(starting + str(i)),
                    "tx": int(self.get_value(starting_tx + str(i))),
                    "rx": int(self.get_value(starting_rx + str(i))),
                })
                results.append(result)
            self._interfaces_bytes = results

        return self._interfaces_bytes

    _interfaces_MAC = None

    @property
    def interfaces_MAC(self):
        """
        Returns an ordered dict with the hardware address of every interface
        """
        if self._interfaces_MAC is None:
            results = []
            starting = "1.3.6.1.2.1.2.2.1.2."
            starting_mac = "1.3.6.1.2.1.2.2.1.6."

            for i in self._value_to_retrieve():
                mac = binascii.b2a_hex(self.get_value(starting_mac + str(i)))
                # now we are going to format mac as the canonical way as a MAC
                # address is intended by inserting ':' every two chars of mac
                # to obtain something as 00:11:22:22:33:44:55

                mac_transformed = ':'.join(mac[j:j+2] for j in range(0, 12, 2) if mac != "")
                result = self._dict({
                    "name": self.get_value(starting + str(i)),
                    "mac_address": mac_transformed
                })
                results.append(result)

            self._interfaces_MAC = results

        return self._interfaces_MAC

    _interfaces_type = None

    @property
    def interfaces_type(self):
        """
        Returns an ordered dict with
        the interface type (e.g Ethernet, loopback)
        """
        if self._interfaces_type is None:
            results = []
            starting = "1.3.6.1.2.1.2.2.1.2."
            types_oid = "1.3.6.1.2.1.2.2.1.3."

            for i in self._value_to_retrieve():
                value_type = self.get_value(types_oid + str(i))
                result = self._dict({
                    "name": self.get_value(starting + str(i)),
                    "type": self.interfaces(value_type),
                })
                results.append(result)

            self._interfaces_type = results

        return self._interfaces_type

    @property
    def interfaces_to_dict(self):
        """
        Returns an ordered dict with all the
        information available about the interface
        """
        results = []
        for i in range(0, len(self.get_interfaces())):
            print '===== %d =====' % i
            result = self._dict({
                "name": self.interfaces_MAC[i]['name'],
                "type": self.interfaces_type[i]['type'],
                "mac_address": self.interfaces_MAC[i]['mac_address'],
                "rx_bytes": int(self.interfaces_bytes[i]['rx']),
                "tx_bytes": int(self.interfaces_bytes[i]['tx']),
                "state": self.interfaces_state[i]['state'],
                "mtu": int(self.interfaces_mtu[i]['mtu']),
                "speed": int(self.interfaces_speed[i]['speed'])
            })
            results.append(result)
        return results

    @property
    def wireless_dbm(self):
        """
        returns a list with the wireless signal (dbm) of the link/s
        """
        res = self.next('1.3.6.1.4.1.14988.1.1.1.2.1.3.0')
        dbm = []
        for i in range(0, len(res[3])):
            dbm.append(int(res[3][i][0][1]))
        return dbm

    @property
    def wireless_links(self):
        '''
        Returns an ordered dict with all the infos about the wireless link/s
        '''
        final = []
        results = self.next('1.3.6.1.4.1.14988.1.1.1.2.1')
        link_number = len(self.next('1.3.6.1.4.1.14988.1.1.1.2.1.3')[3])
        separated_by_meaning = []
        dbm = []
        tx_bytes = []
        rx_bytes = []
        tx_packets = []
        rx_packets = []
        tx_rate = []
        rx_rate = []

        for i in range(0, len(results[3]), link_number):
            separated_by_meaning.append(results[3][i:i+link_number])

        for i in range(0, len(separated_by_meaning[0])):
            dbm.append(int(separated_by_meaning[0][i][0][1]))
            tx_bytes.append(int(separated_by_meaning[1][i][0][1]))
            rx_bytes.append(int(separated_by_meaning[2][i][0][1]))
            tx_packets.append(int(separated_by_meaning[3][i][0][1]))
            rx_packets.append(int(separated_by_meaning[4][i][0][1]))
            tx_rate.append(int(separated_by_meaning[5][i][0][1]))
            rx_rate.append(int(separated_by_meaning[6][i][0][1]))

        for i in range(0, link_number):
            result = self._dict({
                "dbm": dbm[i],
                "tx_bytes": tx_bytes[i],
                "rx_bytes": rx_bytes[i],
                "tx_packets": tx_packets[i],
                "rx_packets": rx_packets[i],
                "tx_rate": tx_rate[i],
                "rx_rate": rx_rate[i]
            })
            final.append(result)
        return final

    @property
    def RAM_total(self):
        """
        Returns the total RAM of the device
        """
        total = self.get_value('1.3.6.1.4.1.10002.1.1.1.1.1.0')
        return int(total)

    @property
    def RAM_free(self):
        """
        Returns the free RAM of the device
        """
        free = self.get_value('1.3.6.1.4.1.10002.1.1.1.1.2.0')
        return int(free)

    def to_dict(self):
        return self._dict({
            "name": self.name,
            "type": "radio",
            "os": self.os[0],
            "os_version": self.os[1],
            "manufacturer": self.manufacturer,
            "model": self.model,
            "RAM_total": self.RAM_total,
            "RAM_free": self.RAM_free,
            "uptime": self.uptime,
            "uptime_tuple": self.uptime_tuple,
            "interfaces": self.interfaces_to_dict,
            "antennas": [],
            "wireless_dbm": self.wireless_dbm,
            "wireless_links": self.wireless_links,
            "routing_protocols": None
        })
