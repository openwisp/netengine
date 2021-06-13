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

logger = logging.getLogger(__name__)


class OpenWRT(SNMP):
    """
    OpenWRT SNMP backend
    """

    _oid_to_retrieve = '1.3.6.1.2.1.2.2.1.1'
    _interface_dict = {}

    def __str__(self):
        """print a human readable object description"""
        return f'<SNMP (OpenWRT): {self.host}>'

    def validate(self):
        """
        raises NetEngineError exception if anything is wrong with the connection
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
        os_name = 'OpenWRT'
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
        return int(self.get_value('1.3.6.1.2.1.1.3.0')) // 100

    @property
    def uptime_tuple(self):
        """
        returns (days, hours, minutes)
        """
        td = timedelta(seconds=self.uptime)

        return td.days, td.seconds // 3600, (td.seconds // 60) % 60

    _interfaces = None

    def get_interfaces(self):
        """
        returns the list of all the interfaces of the device
        """
        if self._interfaces is None:
            interfaces = []
            value_to_get = '1.3.6.1.2.1.2.2.1.2.'

            for i in self._value_to_retrieve():
                value_to_get1 = value_to_get + str(i)

                if value_to_get1:
                    interfaces.append(self.get_value(value_to_get1))

            self._interfaces = [_f for _f in interfaces if _f]

        return self._interfaces

    _interfaces_MAC = None

    @property
    def interfaces_MAC(self):
        """
        Returns an ordered dict with the hardware address of every interface
        """
        if self._interfaces_MAC is None:
            results = []
            mac1 = []
            mac = self.next('1.3.6.1.2.1.2.2.1.6.')[3]
            for i in range(1, len(mac) + 1):
                mac1.append(self.get_value('1.3.6.1.2.1.2.2.1.6.' + str(i)))
            mac_trans = []
            for i in mac1:
                mac_string = self._octet_to_mac(i)
                mac_trans.append(mac_string)
            for i in range(0, len(self.get_interfaces())):
                result = self._dict(
                    {'name': self.get_interfaces()[i], 'mac_address': mac_trans[i]}
                )
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
            starting = '1.3.6.1.2.1.2.2.1.2.'
            tmp = list(starting)
            tmp[18] = str(4)
            to = ''.join(tmp)

            for i in self._value_to_retrieve():
                result = self._dict(
                    {
                        'name': self.get_value(starting + str(i)),
                        'mtu': int(self.get_value(to + str(i))),
                    }
                )
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
                name = self.get_value(starting + str(i))

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
                speed = int(self.get_value(starting_speed + str(i)))

                result = self._dict({'name': name, 'speed': speed})

                results.append(result)
                # increment i
                i += 1

            self._interfaces_speed = results

        return self._interfaces_speed

    _interfaces_up = None

    @property
    def interfaces_up(self):
        """
        Returns an ordereed dict with the interfaces and their state (up: true/false)
        """
        if self._interfaces_up is None:
            results = []
            starting = '1.3.6.1.2.1.2.2.1.2.'
            operative = '1.3.6.1.2.1.2.2.1.8.'
            tmp = list(starting)
            tmp[18] = str(4)
            for i in self._value_to_retrieve():
                if self.get_value(starting + str(i)) != '':
                    result = self._dict(
                        {
                            'name': self.get_value(starting + str(i)),
                            'up': int(self.get_value(operative + str(i))) == 1,
                        }
                    )
                    results.append(result)
                elif self.get_value(starting + str(i)) == '':
                    result = self._dict({'name': '', 'state': ''})
                    results.append(result)

            self._interfaces_up = results

        return self._interfaces_up

    _interfaces_bytes = None

    @property
    def interfaces_bytes(self):
        """
        Returns an ordereed dict with the interface and its tx and rx octets (1 octet = 1 byte = 8 bits)
        """
        if self._interfaces_bytes is None:
            results = []
            starting = '1.3.6.1.2.1.2.2.1.2.'
            starting_rx = '1.3.6.1.2.1.2.2.1.10.'
            starting_tx = '1.3.6.1.2.1.2.2.1.16.'

            for i in self._value_to_retrieve():
                result = self._dict(
                    {
                        'name': self.get_value(starting + str(i)),
                        'tx': int(self.get_value(starting_tx + str(i))),
                        'rx': int(self.get_value(starting_rx + str(i))),
                    }
                )
                results.append(result)

            self._interfaces_bytes = results

        return self._interfaces_bytes

    _interfaces_type = None

    @property
    def interfaces_type(self):
        """
        Returns an ordered dict with the interface type (e.g Ethernet, loopback)
        """
        if self._interfaces_type is None:
            types = {
                '6': 'ethernetCsmacd',
                '24': 'softwareLoopback',
                '131': 'tunnel',
            }
            results = []
            starting = '1.3.6.1.2.1.2.2.1.2.'
            types_oid = '1.3.6.1.2.1.2.2.1.3.'
            for i in self._value_to_retrieve():
                result = self._dict(
                    {
                        'name': self.get_value(starting + str(i)),
                        'type': types[self.get_value(types_oid + str(i))],
                    }
                )
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

            interface_ip_address = self.next('1.3.6.1.2.1.4.20.1.1')[3]
            interface_index = self.next('1.3.6.1.2.1.4.20.1.2')[3]
            interface_netmask = self.next('1.3.6.1.2.1.4.20.1.3')[3]

            results = {}

            for i in range(0, len(interface_ip_address)):
                a = interface_ip_address[i][0][1].asNumbers()
                ip_address = '.'.join(str(a[i]) for i in range(0, len(a)))
                b = interface_netmask[i][0][1].asNumbers()
                netmask = '.'.join(str(b[i]) for i in range(0, len(b)))

                name = self._interface_dict[int(interface_index[i][0][1])]

                results[name] = {'address': ip_address, 'netmask': netmask}

            self._interface_addr_and_mask = results

        return self._interface_addr_and_mask

    @property
    def interfaces_to_dict(self):
        """
        Returns an ordered dict with all the information available about the interface
        """
        results = []
        for i in range(0, len(self.get_interfaces())):

            logger.info(f'====== {i} ======')

            logger.info('... name ...')
            name = self.interfaces_MAC[i]['name']
            logger.info('... if_type ...')
            if_type = self.interfaces_type[i]['type']
            logger.info('... mac_address ...')
            mac_address = self.interfaces_MAC[i]['mac_address']
            logger.info('... rx_bytes ...')
            rx_bytes = int(self.interfaces_bytes[i]['rx'])
            logger.info('... tx_bytes ...')
            tx_bytes = int(self.interfaces_bytes[i]['tx'])
            logger.info('... up ...')
            up = self.interfaces_up[i]['up']
            logger.info('... mtu ...')
            mtu = int(self.interfaces_mtu[i]['mtu'])

            result = self._dict(
                {
                    'name': name,
                    'statistics': {
                        "mac": mac_address,
                        "type": if_type,
                        "up": up,
                        'rx_bytes': rx_bytes,
                        'tx_bytes': tx_bytes,
                        "mtu": mtu,
                    },
                }
            )
            results.append(result)
        return results

    @property
    def local_time(self):
        """
        returns the local time of the host device as a timestamp
        """
        octetstr = bytes(self.get('1.3.6.1.2.1.25.1.2.0')[3][0][1])
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
        logger.warning('Invalid timestring was supplied')

    @property
    def RAM_total(self):
        """
        returns the total RAM of the device
        """
        return int(self.get_value('1.3.6.1.2.1.25.2.3.1.5.1'))

    @property
    def RAM_shared(self):
        """
        returns the shared RAM of the device
        """
        return int(self.get_value('1.3.6.1.2.1.25.2.3.1.6.8'))

    @property
    def RAM_cached(self):
        """
        returns the cached RAM of the device
        """
        return int(self.get_value('1.3.6.1.2.1.25.2.3.1.5.7'))

    @property
    def RAM_free(self):
        """
        returns the free RAM of the device
        """
        RAM_used = int(self.get_value('1.3.6.1.2.1.25.2.3.1.6.1'))
        RAM_free = self.RAM_total - (self.RAM_cached + RAM_used)
        return RAM_free

    @property
    def SWAP_total(self):
        """
        returns the total SWAP of the device
        """
        return int(self.get_value('1.3.6.1.2.1.25.2.3.1.5.10'))

    @property
    def SWAP_free(self):
        """
        returns the free SWAP of the device
        """
        SWAP_used = int(self.get_value('1.3.6.1.2.1.25.2.3.1.6.10'))
        SWAP_free = self.SWAP_total - SWAP_used
        return SWAP_free

    @property
    def CPU_count(self):
        """
        returns the count of CPUs of the device
        """
        return len(self.next('1.3.6.1.2.1.25.3.3.1.2')[3])

    @property
    def resources_to_dict(self):
        """
        returns an ordered dict with hardware resources information
        """
        result = self._dict(
            {
                'cpus': self.CPU_count,
                'memory': {
                    'total': self.RAM_total,
                    'shared': self.RAM_shared,
                    'free': self.RAM_free,
                    'cached': self.RAM_cached,
                },
                'swap': {'total': self.SWAP_total, 'free': self.SWAP_free},
            }
        )
        return result

    @property
    def neighbors(self):
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

        # TODO: find a way to extract IP address from the OID
        neighbors = self.next('1.3.6.1.2.1.4.35.1.4')[3]
        neighbor_states = self.next('1.3.6.1.2.1.4.35.1.7')[3]
        result = []

        for index, neighbor in enumerate(neighbors):
            try:
                mac = EUI(
                    int(neighbor[0][1].prettyPrint(), 16), dialect=mac_unix_expanded
                )
                interface_num = neighbor[0][0].getOid()[10]
                interface = self.get(f'1.3.6.1.2.1.31.1.1.1.1.{interface_num}')[3][0][1]
                state = states_map[str(neighbor_states[index][0][1])]
            except (IndexError, TypeError):
                continue
            result.append(
                self._dict(
                    {'mac': str(mac), 'state': str(state), 'interface': str(interface)}
                )
            )
        return result

    def to_dict(self):
        return self._dict(
            {
                'type': 'DeviceMonitoring',
                'general': {'uptime': self.uptime, "local_time": self.local_time},
                'resources': self.resources_to_dict,
                'interfaces': self.interfaces_to_dict,
                'neighbors': self.neighbors,
            }
        )
