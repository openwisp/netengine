"""
NetEngine SNMP OpenWRT backend
"""

__all__ = ['OpenWRT']


import datetime
import logging
import struct
from datetime import timedelta

import pytz
from netaddr import EUI, mac_unix_expanded

from netengine.backends.snmp import SNMP
from netengine.exceptions import NetEngineError

logger = logging.getLogger(__name__)


class OpenWRT(SNMP):
    """
    OpenWRT SNMP backend
    """

    _oid_to_retrieve = '1.3.6.1.2.1.2.2.1.1.'
    _interface_dict = {}

    def __str__(self):
        """print a human readable object description"""
        return f'<SNMP (OpenWRT): {self.host}>'

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
        os_name = 'OpenWRT'
        os_version = (
            self.get_value('1.3.6.1.2.1.1.1.0', snmpdump=snmpdump).split('#')[0].strip()
        )
        return os_name, os_version

    def manufacturer(self, snmpdump=None):
        # TODO: this is dangerous, it might not work in all cases
        return self.get_manufacturer(
            self.interfaces_MAC(snmpdump=snmpdump)[1]['mac_address']
        )

    def name(self, snmpdump=None):
        """
        returns a string containing the device name
        """
        return self.get_value('1.3.6.1.2.1.1.1.0', snmpdump=snmpdump).split()[1]

    def uptime(self, snmpdump=None):
        """
        returns an integer representing the number of seconds of uptime
        """
        return int(self.get_value('1.3.6.1.2.1.1.3.0', snmpdump=snmpdump)) // 100

    def uptime_tuple(self, snmpdump=None):
        """
        returns (days, hours, minutes)
        """
        td = timedelta(seconds=self.uptime(snmpdump=snmpdump))

        return td.days, td.seconds // 3600, (td.seconds // 60) % 60

    _interfaces = None
    _wireless_interfaces = None

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

            self._interfaces = [_f for _f in interfaces if _f]

        return self._interfaces

    def get_wireless_interfaces(self, snmpdump=None):
        """
        returns the list of all the wireless interfaces of the device
        """
        if self._wireless_interfaces is None:
            interfaces = []
            wireless_if_oid = '1.2.840.10036.1.1.1.1.'
            interfaces_oid = '1.3.6.1.2.1.2.2.1.2.'

            for i in self._value_to_retrieve(snmpdump=snmpdump):
                try:
                    value_to_get1 = self.get_value(
                        wireless_if_oid + str(i), snmpdump=snmpdump
                    )

                    if value_to_get1:
                        interfaces.append(
                            self.get_value(interfaces_oid + str(i), snmpdump=snmpdump)
                        )
                except (NetEngineError, KeyError):
                    pass

            self._wireless_interfaces = [_f for _f in interfaces if _f]

        return self._wireless_interfaces

    _interfaces_MAC = None

    def interfaces_MAC(self, snmpdump=None):
        """
        Returns an ordered dict with the hardware address of every interface
        """
        if self._interfaces_MAC is None:
            results = []
            mac1 = []
            mac = self.next('1.3.6.1.2.1.2.2.1.6.', snmpdump=snmpdump)[3]
            for i in range(1, len(mac) + 1):
                mac1.append(
                    self.get_value('1.3.6.1.2.1.2.2.1.6.' + str(i), snmpdump=snmpdump)
                )
            mac_trans = []
            for i in mac1:
                mac_string = self._octet_to_mac(i)
                mac_trans.append(mac_string)
            for i in range(0, len(self.get_interfaces(snmpdump=snmpdump))):
                result = self._dict(
                    {
                        'name': self.get_interfaces(snmpdump=snmpdump)[i],
                        'mac_address': mac_trans[i],
                    }
                )
                results.append(result)

            self._interfaces_MAC = results

        return self._interfaces_MAC

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

    _interfaces_speed = None

    def interfaces_speed(self, snmpdump=None):
        """
        Returns an ordered dict with the interface and ist speed in bps
        """
        if self._interfaces_speed is None:
            results = []
            starting = '1.3.6.1.2.1.2.2.1.2.'
            starting_speed = '1.3.6.1.2.1.2.2.1.5.'

            STOP_AFTER_FAILS = 3

            i = 1
            consecutive_fails = (
                0  # counter that indicates how many consecutive attempts failed
            )
            while True:
                # break cycles if STOP_AFTER_FAILS reached
                if consecutive_fails == STOP_AFTER_FAILS:
                    break

                # get name
                name = self.get_value(starting + str(i), snmpdump=snmpdump)

                # if nothing found
                if name == '':
                    # increment fail counter
                    consecutive_fails += 1
                    # increment i
                    i += 1
                    # skip to next iteration
                    continue
                else:
                    # reset fail counter
                    consecutive_fails = 0

                # get speed and convert to int
                speed = int(self.get_value(starting_speed + str(i), snmpdump=snmpdump))

                result = self._dict({'name': name, 'speed': speed})

                results.append(result)
                # increment i
                i += 1

            self._interfaces_speed = results

        return self._interfaces_speed

    _interfaces_up = None

    def interfaces_up(self, snmpdump=None):
        """
        Returns an ordereed dict with the interfaces and their state (up: true/false)
        """
        if self._interfaces_up is None:
            results = []
            starting = '1.3.6.1.2.1.2.2.1.2.'
            operative = '1.3.6.1.2.1.2.2.1.8.'
            tmp = list(starting)
            tmp[18] = str(4)
            for i in self._value_to_retrieve(snmpdump=snmpdump):
                if self.get_value(starting + str(i), snmpdump=snmpdump) != '':
                    result = self._dict(
                        {
                            'name': self.get_value(
                                starting + str(i), snmpdump=snmpdump
                            ),
                            'up': int(
                                self.get_value(operative + str(i), snmpdump=snmpdump)
                            )
                            == 1,
                        }
                    )
                    results.append(result)
                elif self.get_value(starting + str(i), snmpdump=snmpdump) == '':
                    result = self._dict({'name': '', 'state': ''})
                    results.append(result)

            self._interfaces_up = results

        return self._interfaces_up

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

    _interfaces_type = None

    def interfaces_type(self, snmpdump=None):
        """
        Returns an ordered dict with the interface type (e.g Ethernet, loopback)
        """
        if self._interfaces_type is None:
            results = []
            starting = '1.3.6.1.2.1.2.2.1.2.'
            types_oid = '1.3.6.1.2.1.2.2.1.3.'
            types = {
                '6': 'ethernet',
                '24': 'loopback',
                '157': 'wireless',
                '209': 'bridge',
            }
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

    _interface_addr_and_mask = None

    def interface_addr_and_mask(self, snmpdump=None):
        """
        TODO: this method needs to be simplified and explained
        """
        if self._interface_addr_and_mask is None:
            interface_name = self.get_interfaces(snmpdump=snmpdump)

            for i in range(0, len(interface_name)):
                self._interface_dict[
                    self._value_to_retrieve(snmpdump=snmpdump)[i]
                ] = interface_name[i]

            interface_ip_address = self.next(
                '1.3.6.1.2.1.4.20.1.1.', snmpdump=snmpdump
            )[3]
            interface_index = self.next('1.3.6.1.2.1.4.20.1.2.', snmpdump=snmpdump)[3]
            interface_netmask = self.next('1.3.6.1.2.1.4.20.1.3.', snmpdump=snmpdump)[3]

            results = {}

            # TODO: Add ipv6 addresses
            for i in range(0, len(interface_ip_address)):
                a = interface_ip_address[i][0][1].asNumbers()
                ip_address = '.'.join(str(a[i]) for i in range(0, len(a)))
                b = interface_netmask[i][0][1].asNumbers()
                netmask = '.'.join(str(b[i]) for i in range(0, len(b)))

                name = self._interface_dict[int(interface_index[i][0][1])]
                results[name] = {
                    'family': 'ipv4',
                    'address': ip_address,
                    'mask': netmask,
                }

            self._interface_addr_and_mask = results

        return self._interface_addr_and_mask

    def interfaces_to_dict(self, snmpdump=None):
        """
        Returns an ordered dict with all the information available about the interface
        """
        results = []
        wireless_if = self.get_wireless_interfaces()
        for i in range(0, len(self.get_interfaces(snmpdump=snmpdump))):

            logger.info(f'====== {i} ======')

            logger.info('... name ...')
            name = self.interfaces_MAC(snmpdump=snmpdump)[i]['name']
            logger.info('... if_type ...')
            if_type = self.interfaces_type(snmpdump=snmpdump)[i]['type']
            logger.info('... mac_address ...')
            mac_address = self.interfaces_MAC(snmpdump=snmpdump)[i]['mac_address']
            logger.info('... rx_bytes ...')
            rx_bytes = int(self.interfaces_bytes(snmpdump=snmpdump)[i]['rx'])
            logger.info('... tx_bytes ...')
            tx_bytes = int(self.interfaces_bytes(snmpdump=snmpdump)[i]['tx'])
            logger.info('... up ...')
            up = self.interfaces_up(snmpdump=snmpdump)[i]['up']
            logger.info('... mtu ...')
            mtu = int(self.interfaces_mtu(snmpdump=snmpdump)[i]['mtu'])
            logger.info('... if_ip ...')
            addr = self.interface_addr_and_mask(snmpdump=snmpdump).get(name)
            addresses = [addr] if addr is not None else []

            if name in wireless_if:
                if_type = 'wireless'

            result = self._dict(
                {
                    'name': name,
                    'type': if_type,
                    'statistics': {
                        'mac': mac_address,
                        'up': up,
                        'rx_bytes': rx_bytes,
                        'tx_bytes': tx_bytes,
                        'mtu': mtu,
                        'addresses': addresses,
                    },
                }
            )
            results.append(result)
        return results

    def local_time(self, snmpdump=None):
        """
        returns the local time of the host device as a timestamp
        """
        octetstr = bytes(self.get('1.3.6.1.2.1.25.1.2.0', snmpdump=snmpdump)[3][0][1])
        size = len(octetstr)
        # string may or may not contain timezone, so size can be 8 or 11
        if size == 8:
            (year, month, day, hour, minutes, seconds, deci_seconds,) = struct.unpack(
                '>HBBBBBB', octetstr
            )
            return int(
                datetime.datetime(
                    year,
                    month,
                    day,
                    hour,
                    minutes,
                    seconds,
                    deci_seconds * 100_000,
                    tzinfo=pytz.utc,
                ).timestamp()
            )
        elif size == 11:
            (
                year,
                month,
                day,
                hour,
                minutes,
                seconds,
                deci_seconds,
                direction,
                hours_from_utc,
                minutes_from_utc,
            ) = struct.unpack('>HBBBBBBcBB', octetstr)
            offset = datetime.timedelta(hours=hours_from_utc, minutes=minutes_from_utc)
            if direction == b'-':
                offset = -offset
            return int(
                datetime.datetime(
                    year,
                    month,
                    day,
                    hour,
                    minutes,
                    seconds,
                    deci_seconds * 100_000,
                    tzinfo=pytz.utc,
                ).timestamp()
            )

    def RAM_total(self, snmpdump=None):
        """
        returns the total RAM of the device in bytes
        """
        return int(self.get_value('1.3.6.1.4.1.2021.4.5.0', snmpdump=snmpdump)) * 1024

    def RAM_shared(self, snmpdump=None):
        """
        returns the shared RAM of the device in bytes
        """
        return int(self.get_value('1.3.6.1.4.1.2021.4.13.0', snmpdump=snmpdump)) * 1024

    def RAM_cached(self, snmpdump=None):
        """
        returns the cached RAM of the device in bytes
        """
        return int(self.get_value('1.3.6.1.4.1.2021.4.15.0', snmpdump=snmpdump)) * 1024

    def RAM_free(self, snmpdump=None):
        """
        returns the free RAM of the device in bytes
        """
        return int(self.get_value('1.3.6.1.4.1.2021.4.11.0', snmpdump=snmpdump)) * 1024

    def RAM_buffered(self, snmpdump=None):
        """
        returns the buffered RAM of the device in bytes
        """
        return int(self.get_value('1.3.6.1.4.1.2021.4.14.0', snmpdump=snmpdump)) * 1024

    def SWAP_total(self, snmpdump=None):
        """
        returns the total SWAP of the device in bytes
        """
        return int(self.get_value('1.3.6.1.4.1.2021.4.3.0', snmpdump=snmpdump)) * 1024

    def SWAP_free(self, snmpdump=None):
        """
        returns the free SWAP of the device in bytes
        """
        return int(self.get_value('1.3.6.1.4.1.2021.4.4.0', snmpdump=snmpdump)) * 1024

    def CPU_count(self, snmpdump=None):
        """
        returns the count of CPUs of the device
        """
        return len(self.next('1.3.6.1.2.1.25.3.3.1.2.', snmpdump=snmpdump)[3])

    def load(self, snmpdump=None):
        """
        Returns an array with load average values respectively in the last
        minute, in the last 5 minutes and in the last 15 minutes
        """
        array = self.next('1.3.6.1.4.1.2021.10.1.3.', snmpdump=snmpdump)[3]
        one = float(array[0][0][1])
        five = float(array[1][0][1])
        fifteen = float(array[2][0][1])
        return [one, five, fifteen]

    def resources_to_dict(self, snmpdump=None):
        """
        returns an ordered dict with hardware resources information
        """
        result = self._dict(
            {
                'load': self.load(snmpdump=snmpdump),
                'cpus': self.CPU_count(snmpdump=snmpdump),
                'memory': {
                    'total': self.RAM_total(snmpdump=snmpdump),
                    'shared': self.RAM_shared(snmpdump=snmpdump),
                    'free': self.RAM_free(snmpdump=snmpdump),
                    'cached': self.RAM_cached(snmpdump=snmpdump),
                    'buffered': self.RAM_buffered(snmpdump=snmpdump),
                },
                'swap': {
                    'total': self.SWAP_total(snmpdump=snmpdump),
                    'free': self.SWAP_free(snmpdump=snmpdump),
                },
            }
        )
        return result

    def neighbors(self, snmpdump=None):
        """
        returns a dict with neighbors information
        """
        states_map = {
            '1': 'REACHABLE',
            '2': 'STALE',
            '3': 'DELAY',
            '4': 'PROBE',
            '5': 'INVALID',
            '6': 'UNKNOWN',
            '7': 'INCOMPLETE',
        }

        neighbors_oid = '1.3.6.1.2.1.4.35.1.4'
        neighbor_states_oid = '1.3.6.1.2.1.4.35.1.7'
        neighbor_info = self.next('1.3.6.1.2.1.4.35.1.', snmpdump=snmpdump)[3]
        neighbors = []
        neighbor_states = []
        result = []

        for oid in neighbor_info:
            if neighbors_oid in str(oid[0][0]):
                neighbors.append(oid)
            elif neighbor_states_oid in str(oid[0][0]):
                neighbor_states.append(oid)

        for index, neighbor in enumerate(neighbors):
            try:
                oid = neighbor[0][0].getOid()
                if oid[12] == 4:
                    ip = oid[13:]
                else:
                    ip = self._ascii_blocks_to_ipv6(str(oid[13:]))
                mac = EUI(
                    int(neighbor[0][1].prettyPrint(), 16), dialect=mac_unix_expanded
                )
                interface_num = neighbor[0][0].getOid()[10]
                interface = self.get(
                    f'1.3.6.1.2.1.31.1.1.1.1.{interface_num}', snmpdump=snmpdump
                )[3][0][1]
                state = states_map[str(neighbor_states[index][0][1])]
            except (IndexError, TypeError, ValueError):
                continue
            result.append(
                self._dict(
                    {
                        'mac': str(mac),
                        'state': str(state),
                        'interface': str(interface),
                        'ip': str(ip),
                    }
                )
            )
        return result

    def to_dict(self, snmpdump=None, autowalk=True):
        if autowalk:
            snmpdump = self.walk('1.2')
        result = self._dict(
            {
                'type': 'DeviceMonitoring',
                'general': {
                    'hostname': self.name(snmpdump=snmpdump),
                    'uptime': self.uptime(snmpdump=snmpdump),
                    'local_time': self.local_time(snmpdump=snmpdump),
                },
                'resources': self.resources_to_dict(snmpdump=snmpdump),
                'interfaces': self.interfaces_to_dict(snmpdump=snmpdump),
                'neighbors': self.neighbors(snmpdump=snmpdump),
            }
        )
        return result
