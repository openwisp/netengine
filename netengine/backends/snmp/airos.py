"""
NetEngine SNMP Ubiquiti Air OS backend
"""

__all__ = ['AirOS']


import binascii
import logging
from datetime import datetime

from pytrie import StringTrie as Trie

from .base import SNMP

logger = logging.getLogger(__name__)


class AirOS(SNMP):
    """
    Ubiquiti AirOS SNMP backend
    """

    _oid_to_retrieve = '1.3.6.1.2.1.1.9.1.1.'

    def __str__(self, snmpdump=None):
        """print a human readable object description"""
        return f'<SNMP (Ubiquity AirOS): {self.host}>'

    def validate(self, snmpdump=None):
        """
        raises NetEngineError exception if anything is wrong with the connection
        for example: wrong host, invalid community
        """
        # this triggers a connection which
        # will raise an exception if anything is wrong
        return self.name(snmpdump=snmpdump)

    def os(self, snmpdump=None):
        """
        returns (os_name, os_version)
        """
        os_name = 'AirOS'
        os_version = (
            self.get_value('1.3.6.1.2.1.1.1.0', snmpdump=snmpdump).split('#')[0].strip()
        )
        return os_name, os_version

    def name(self, snmpdump=None):
        """
        returns a string containing the device name
        """
        return self.get_value('1.3.6.1.2.1.1.5.0', snmpdump=snmpdump)

    def model(self, snmpdump=None):
        """
        returns a string containing the device model
        """
        oids = ['1.2.840.10036.3.1.2.1.3.5', '1.2.840.10036.3.1.2.1.3.8']
        for oid in oids:
            model = self.get_value(oid, snmpdump=snmpdump)
            if model != '':
                return model

    def firmware(self, snmpdump=None):
        """
        returns a string containing the device firmware
        """
        oids = ['1.2.840.10036.3.1.2.1.4.5', '1.2.840.10036.3.1.2.1.4.8']
        for oid in oids:
            tmp = self.get_value(oid, snmpdump=snmpdump).split('.')
            if tmp is not None:
                length = len(tmp)
                i = 0
                for piece in tmp:
                    if 'v' in piece:
                        return 'AirOS ' + '.'.join(tmp[i:length])
                    i = i + 1

    def manufacturer(self, snmpdump=None):
        return self.get_manufacturer(
            self.interfaces_MAC(snmpdump=snmpdump)[1]['mac_address']
        )

    def ssid(self, snmpdump=None):
        """
        returns a string containing the wireless ssid
        """
        oids = ['1.2.840.10036.1.1.1.9.5', '1.2.840.10036.1.1.1.9.8']
        for oid in oids:
            if self.get_value(oid, snmpdump=snmpdump) != '':
                return self.get_value(oid, snmpdump=snmpdump)

    def uptime(self, snmpdump=None):
        """
        returns an integer representing the number of seconds of uptime
        """
        return int(self.get_value('1.3.6.1.2.1.1.3.0', snmpdump=snmpdump)) // 100

    def interfaces_number(self, snmpdump=None):
        """
        Returns the number of the network interfaces
        """
        return int(self.get_value('1.3.6.1.2.1.2.1.0', snmpdump=snmpdump))

    _interfaces = None

    def get_interfaces(self, snmpdump=None):
        """
        returns the list of all the interfaces of the device
        """
        if self._interfaces is None:
            interfaces = []
            value_to_get = '1.3.6.1.2.1.2.2.1.2.'

            for i in self._value_to_retrieve(snmpdump=snmpdump):
                value_to_get1 = value_to_get + str(i)
                if value_to_get1:
                    interfaces.append(self.get_value(value_to_get1, snmpdump=snmpdump))

            self._interfaces = interfaces

        return self._interfaces

    _interfaces_mtu = None

    def interfaces_mtu(self, snmpdump=None):
        """
        Returns an ordereed dict with the interface and its MTU
        """
        if self._interfaces_mtu is None:
            results = []
            starting = '1.3.6.1.2.1.2.2.1.2.'
            tmp = list(starting)
            tmp[18] = str(4)
            to = ''.join(tmp)

            for i in self._value_to_retrieve(snmpdump=snmpdump):
                result = self._dict(
                    {
                        'name': self.get_value(starting + str(i), snmpdump=snmpdump),
                        'mtu': int(self.get_value(to + str(i), snmpdump=snmpdump)),
                    }
                )
                results.append(result)

            self._interfaces_mtu = results

        return self._interfaces_mtu

    _interfaces_state = None

    def interfaces_state(self, snmpdump=None):
        """
        Returns an ordereed dict with the interfaces and their state (up, down)
        """
        if self._interfaces_state is None:
            results = []
            starting = '1.3.6.1.2.1.2.2.1.2.'
            operative = '1.3.6.1.2.1.2.2.1.8.'
            tmp = list(starting)
            tmp[18] = str(4)
            for i in self._value_to_retrieve(snmpdump=snmpdump):
                if self.get_value(starting + str(i), snmpdump=snmpdump) != '':
                    if int(self.get_value(operative + str(i), snmpdump=snmpdump)) == 1:
                        result = self._dict(
                            {
                                'name': self.get_value(
                                    starting + str(i), snmpdump=snmpdump
                                ),
                                'state': 'up',
                            }
                        )
                    else:
                        result = self._dict(
                            {
                                'name': self.get_value(
                                    starting + str(i), snmpdump=snmpdump
                                ),
                                'state': 'down',
                            }
                        )
                elif self.get_value(starting + str(i), snmpdump=snmpdump) == '':
                    result = self._dict({'name': '', 'state': ''})
                # append result to list
                results.append(result)

            self._interfaces_state = results

        return self._interfaces_state

    _interfaces_speed = None

    def interfaces_speed(self, snmpdump=None):
        """
        Returns an ordered dict with the interface and ist speed in bps
        """
        if self._interfaces_speed is None:
            results = []
            starting = '1.3.6.1.2.1.2.2.1.2.'
            starting_speed = '1.3.6.1.2.1.2.2.1.5.'

            for i in self._value_to_retrieve(snmpdump=snmpdump):
                result = self._dict(
                    {
                        'name': self.get_value(starting + str(i), snmpdump=snmpdump),
                        'speed': int(
                            self.get_value(starting_speed + str(i), snmpdump=snmpdump)
                        ),
                    }
                )
                results.append(result)

            self._interfaces_speed = results

        return self._interfaces_speed

    _interfaces_bytes = None

    def interfaces_bytes(self, snmpdump=None):
        """
        Returns an ordereed dict with the interface and its tx and rx octets (1 octet = 1 byte = 8 bits)
        """
        if self._interfaces_bytes is None:
            results = []
            starting = '1.3.6.1.2.1.2.2.1.2.'
            starting_rx = '1.3.6.1.2.1.2.2.1.10.'
            starting_tx = '1.3.6.1.2.1.2.2.1.16.'

            for i in self._value_to_retrieve(snmpdump=snmpdump):
                result = self._dict(
                    {
                        'name': self.get_value(starting + str(i), snmpdump=snmpdump),
                        'tx': int(
                            self.get_value(starting_tx + str(i), snmpdump=snmpdump)
                        ),
                        'rx': int(
                            self.get_value(starting_rx + str(i), snmpdump=snmpdump)
                        ),
                    }
                )
                results.append(result)
            self._interfaces_bytes = results

        return self._interfaces_bytes

    _interfaces_MAC = None

    def interfaces_MAC(self, snmpdump=None):
        """
        Returns an ordered dict with the hardware address of every interface
        """
        if self._interfaces_MAC is None:
            results = []
            starting = '1.3.6.1.2.1.2.2.1.2.'
            starting_mac = '1.3.6.1.2.1.2.2.1.6.'

            for i in self._value_to_retrieve(snmpdump=snmpdump):
                mac = binascii.b2a_hex(
                    self.get_value(starting_mac + str(i), snmpdump=snmpdump).encode()
                ).decode()
                # now we are going to format mac as the canonical way as a MAC
                # address is intended by inserting ':' every two chars of mac
                # to obtain something as 00:11:22:22:33:44:55
                mac_transformed = ':'.join(
                    mac[slice(j, j + 2)] for j in range(0, 12, 2) if mac != ''
                )
                result = self._dict(
                    {
                        'name': self.get_value(starting + str(i), snmpdump=snmpdump),
                        'mac_address': mac_transformed,
                    }
                )
                results.append(result)

            self._interfaces_MAC = results

        return self._interfaces_MAC

    _interfaces_type = None

    def interfaces_type(self, snmpdump=None):
        """
        Returns an ordered dict with the interface type (e.g Ethernet, loopback)
        """
        if self._interfaces_type is None:
            types = {
                '6': 'ethernet',
                '24': 'loopback',
                '157': 'wireless',
                '209': 'bridge',
            }
            results = []
            starting = '1.3.6.1.2.1.2.2.1.2.'
            types_oid = '1.3.6.1.2.1.2.2.1.3.'

            for i in self._value_to_retrieve(snmpdump=snmpdump):
                result = self._dict(
                    {
                        'name': self.get_value(starting + str(i), snmpdump=snmpdump),
                        'type': types.get(
                            self.get_value(types_oid + str(i), snmpdump=snmpdump),
                            'unknown',
                        ),
                    }
                )
                results.append(result)

            self._interfaces_type = results

        return self._interfaces_type

    def interfaces_to_dict(self, snmpdump=None):
        """
        Returns an ordered dict with all the information available about the interface
        """
        results = []
        for i in range(0, len(self.get_interfaces(snmpdump=snmpdump))):
            logger.info(f'===== {i} =====')
            result = self._dict(
                {
                    'name': self.interfaces_MAC(snmpdump=snmpdump)[i]['name'],
                    'statistics': {
                        'rx_bytes': int(
                            self.interfaces_bytes(snmpdump=snmpdump)[i]['rx']
                        ),
                        'tx_bytes': int(
                            self.interfaces_bytes(snmpdump=snmpdump)[i]['tx']
                        ),
                    },
                }
            )
            results.append(result)
        return results

    def wireless_dbm(self, snmpdump=None):
        """
        returns a list with the wireless signal (dbm) of the link/s
        """
        res = self.next('1.3.6.1.4.1.14988.1.1.1.2.1.3.0.', snmpdump=snmpdump)
        dbm = []
        for i in range(0, len(res[3])):
            dbm.append(int(res[3][i][0][1]))
        return dbm

    def wireless_links(self, snmpdump=None):
        '''
        Returns an ordered dict with all the infos about the wireless link/s
        '''
        final = []
        results = self.next('1.3.6.1.4.1.14988.1.1.1.2.1.', snmpdump=snmpdump)
        link_number = len(
            self.next('1.3.6.1.4.1.14988.1.1.1.2.1.3.', snmpdump=snmpdump)[3]
        )
        separated_by_meaning = []
        dbm = []
        tx_bytes = []
        rx_bytes = []
        tx_packets = []
        rx_packets = []
        tx_rate = []
        rx_rate = []

        for i in range(0, len(results[3]), link_number):
            separated_by_meaning.append(results[3][slice(i, i + link_number)])

        for i in range(0, len(separated_by_meaning[0])):
            dbm.append(int(separated_by_meaning[0][i][0][1]))
            tx_bytes.append(int(separated_by_meaning[1][i][0][1]))
            rx_bytes.append(int(separated_by_meaning[2][i][0][1]))
            tx_packets.append(int(separated_by_meaning[3][i][0][1]))
            rx_packets.append(int(separated_by_meaning[4][i][0][1]))
            tx_rate.append(int(separated_by_meaning[5][i][0][1]))
            rx_rate.append(int(separated_by_meaning[6][i][0][1]))

        for i in range(0, link_number):
            result = self._dict(
                {
                    'dbm': dbm[i],
                    'tx_bytes': tx_bytes[i],
                    'rx_bytes': rx_bytes[i],
                    'tx_packets': tx_packets[i],
                    'rx_packets': rx_packets[i],
                    'tx_rate': tx_rate[i],
                    'rx_rate': rx_rate[i],
                }
            )
            final.append(result)
        return final

    def local_time(self, snmpdump=None):
        """
        returns the local time of the host device as a timestamp
        """
        epoch = str(self.get('1.3.6.1.4.1.41112.1.4.8.1.0', snmpdump=snmpdump)[3][0][1])
        timestamp = int(datetime.strptime(epoch, '%Y-%m-%d %H:%M:%S').timestamp())
        return timestamp

    def RAM_total(self, snmpdump=None):
        """
        Returns the total RAM of the device
        """
        total = self.get_value('1.3.6.1.4.1.10002.1.1.1.1.1.0', snmpdump=snmpdump)
        return int(total)

    def RAM_free(self, snmpdump=None):
        """
        Returns the free RAM of the device
        """
        free = self.get_value('1.3.6.1.4.1.10002.1.1.1.1.2.0', snmpdump=snmpdump)
        return int(free)

    def RAM_buffered(self, snmpdump=None):
        """
        Returns the buffered RAM of the device
        """
        buffered = self.get_value('1.3.6.1.4.1.10002.1.1.1.1.3.0', snmpdump=snmpdump)
        return int(buffered)

    def RAM_cached(self, snmpdump=None):
        """
        Returns the cached RAM of the device
        """
        cached = self.get_value('1.3.6.1.4.1.10002.1.1.1.1.4.0', snmpdump=snmpdump)
        return int(cached)

    def load(self, snmpdump=None):
        """
        Returns an array with load average values respectively in the last
        minute, in the last 5 minutes and in the last 15 minutes
        """
        array = self.next('1.3.6.1.4.1.10002.1.1.1.4.2.1.3.', snmpdump=snmpdump)[3]
        one = int(array[0][0][1])
        five = int(array[1][0][1])
        fifteen = int(array[2][0][1])
        return [one, five, fifteen]

    def SWAP_total(self, snmpdump=None):
        """
        Returns the total SWAP of the device
        """
        total = self.get_value('1.3.6.1.4.1.10002.1.1.1.2.1.0', snmpdump=snmpdump)
        return int(total)

    def SWAP_free(self, snmpdump=None):
        """
        Returns the free SWAP of the device
        """
        free = self.get_value('1.3.6.1.4.1.10002.1.1.1.2.2.0', snmpdump=snmpdump)
        return int(free)

    def resources_to_dict(self, snmpdump=None):
        """
        returns an ordered dict with hardware resources information
        """
        result = self._dict(
            {
                'load': self.load(snmpdump=snmpdump),
                'memory': {
                    'total': self.RAM_total(snmpdump=snmpdump),
                    'buffered': self.RAM_buffered(snmpdump=snmpdump),
                    'free': self.RAM_free(snmpdump=snmpdump),
                    'cached': self.RAM_cached(snmpdump=snmpdump),
                },
                'swap': {
                    'total': self.SWAP_total(snmpdump=snmpdump),
                    'free': self.SWAP_free(snmpdump=snmpdump),
                },
            }
        )
        return result

    def to_dict(self, snmpdump=None, autowalk=True):
        if autowalk:
            snmpdump = Trie(self.walk('1.3.6'))
        result = self._dict(
            {
                'type': 'DeviceMonitoring',
                'general': {
                    'uptime': self.uptime(snmpdump=snmpdump),
                    'local_time': self.local_time(snmpdump=snmpdump),
                },
                'resources': self.resources_to_dict(snmpdump=snmpdump),
                'interfaces': self.interfaces_to_dict(snmpdump=snmpdump),
            }
        )
        return result
