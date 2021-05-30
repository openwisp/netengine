"""
NetEngine SNMP Cisco backend
"""

__all__ = ['Cisco']

import binascii
from datetime import timedelta

from netengine.backends.snmp import SNMP


class Cisco(SNMP):
    """
    Cisco SNMP backend
    """

    _oid_to_retrieve = '1.3.6.1.2.1.2.2.1.1'
    _interface_dict = {}

    def __str__(self):
        """ print a human readable object description """
        return u"<SNMP (Cisco): %s>" % self.host

    def validate(self):
        """
        raises NetEngineError exception if anything
        is wrong with the connection
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
        os_name = 'Cisco'
        os_version = self.get_value('1.3.6.1.2.1.1.1.0').split('#')[0].strip()
        return os_name, os_version

    @property
    def manufacturer(self):
        # TODO: this is dangerous, it might not work in all cases
        return self.get_manufacturer(self.interfaces_MAC[1]['mac_address'])

    @property
    def name(self):
        """
        returns a string containing the device name
        """
        return self.get_value('1.3.6.1.2.1.1.5.0')

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

            self._interfaces = filter(None, interfaces)

        return self._interfaces

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
                        results.append(result)
                    else:
                        result = self._dict({
                            "name": self.get_value(starting + str(i)),
                            "state": "down"
                        })
                        results.append(result)
                elif self.get_value(starting + str(i)) == "":
                    result = self._dict({
                            "name": "",
                            "state": ""
                        })
                    results.append(result)

            self._interfaces_state = results

        return self._interfaces_state

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

    _interfaces_type = None

    @property
    def interfaces_type(self):
        """
        Returns an ordered dict with the interface type
        (e.g Ethernet, loopback)
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

    _interface_addr_and_mask = None

    @property
    def interface_addr_and_mask(self):
        """
        TODO: this method needs to be simplified and explained
        """
        if self._interface_addr_and_mask is None:
            interface_name = self.get_interfaces()

            for i in range(0, len(interface_name)):
                self._interface_dict[self._value_to_retrieve()[i]] = interface_name[i]

            interface_ip_address = self.next("1.3.6.1.2.1.4.20.1.1")[3]
            interface_index = self.next("1.3.6.1.2.1.4.20.1.2")[3]
            interface_netmask = self.next("1.3.6.1.2.1.4.20.1.3")[3]

            results = {}

            for i in range(0, len(interface_ip_address)):
                a = interface_ip_address[i][0][1].asNumbers()
                ip_address = '.'.join(str(a[i]) for i in range(0, len(a)))
                b = interface_netmask[i][0][1].asNumbers()
                netmask = '.'.join(str(b[i]) for i in range(0, len(b)))

                name = self._interface_dict[int(interface_index[i][0][1])]

                results[name] = {
                    "address": ip_address,
                    "netmask": netmask
                }

            self._interface_addr_and_mask = results

        return self._interface_addr_and_mask

    @property
    def interfaces_to_dict(self):
        """
        Returns an ordered dict with all
        the information available about the interface
        """
        results = []
        for i in range(0, len(self.get_interfaces())):

            print '====== %d ======' % i

            print '... name ...'
            name = self.interfaces_MAC[i]['name']
            print '... if_type ...'
            if_type = self.interfaces_type[i]['type']
            print '... mac_address ...'
            mac_address = self.interfaces_MAC[i]['mac_address']
            print '... rx_bytes ...'
            rx_bytes = int(self.interfaces_bytes[i]['rx'])
            print '... tx_bytes ...'
            tx_bytes = int(self.interfaces_bytes[i]['tx'])
            print '... state ...'
            state = self.interfaces_state[i]['state']
            print '... mtu ...'
            mtu = int(self.interfaces_mtu[i]['mtu'])
            print '... speed ...'
            speed = int(self.interfaces_speed[i]['speed'])
            print '... ip address & subnet ...'
            ip_and_netmask = self.interface_addr_and_mask

            if name in ip_and_netmask.keys():
                ip_address = ip_and_netmask[name]['address']
                netmask = ip_and_netmask[name]['netmask']
            else:
                ip_address = None
                netmask = None

            result = self._dict({
                "name": name,
                "type": if_type,
                "mac_address": mac_address,
                "ip_address": ip_address,
                "netmask": netmask,
                "rx_bytes": rx_bytes,
                "tx_bytes": tx_bytes,
                "state": state,
                "mtu": mtu,
                "speed": speed
            })

            # result = self._dict({
            #     "name" : self.interfaces_MAC[i]['name'],
            #     "type" : self.interfaces_type[i]['type'],
            #     "mac_address" : self.interfaces_MAC[i]['mac_address'],
            #     "rx_bytes" : int(self.interfaces_bytes[i]['rx']),
            #     "tx_bytes" : int(self.interfaces_bytes[i]['tx']),
            #     "state" : self.interfaces_state[i]['state'],
            #     "mtu" : int(self.interfaces_mtu[i]['mtu']),
            #     "speed" : int(self.interfaces_speed[i]['speed'])
            # })
            results.append(result)
        return results

    @property
    def RAM_total(self):
        """
        returns the total RAM of the device
        """
        memoryPoolUsed = int(self.get_value("1.3.6.1.4.1.9.9.48.1.1.1.5.2"))
        memoryPoolFree = int(self.get_value("1.3.6.1.4.1.9.9.48.1.1.1.6.2"))
        processorRam = int(self.get_value("1.3.6.1.4.1.9.3.6.6.0"))
        totalRAM = memoryPoolUsed + memoryPoolFree + processorRam
        return totalRAM

    def to_dict(self):
        return self._dict({
            "name": self.name,
            "type": "radio",
            "os": self.os[0],
            "os_version": self.os[1],
            "manufacturer": self.manufacturer,
            "model": None,
            "RAM_total": self.RAM_total,
            "uptime": self.uptime,
            "uptime_tuple": self.uptime_tuple,
            "interfaces": self.get_interfaces(),
            "antennas": [],
            "routing_protocols": None,
        })
