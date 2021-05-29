from .base import BaseBackend


class Dummy(BaseBackend):
    """
    Dummy backend
    """

    def __init__(self, host, port=0):
        """dummy netengine backend for development or testing"""
        self.host = host
        self.port = port

    def validate(self):
        """
        raises NetEngineError exception if anything is wrong with the connection
        for example: wrong host, invalid credentials
        """
        pass

    def __str__(self):
        """print a human readable object description"""
        return f'<Dummy NetEngine {self.host}>'

    def get_interfaces(self):
        return [
            {},
            {
                'ipv6_address_link': '',
                'hardware_address': '00:16:3E:26:9D:13',
                'rx_packets': '147684',
                'broadcast_address': '',
                'rx_bytes': '12956143',
                'link_encap': 'Ethernet',
                'metric': '1',
                'txqueuelen': '1000',
                'net_mask': '',
                'ip_address': '',
                'collisions': '0',
                'interface': 'eth0',
                'tx_bytes': '12523266',
                'mtu': '1500',
                'tx_packets': '132602',
                'ipv6_address_global': '',
            },
            {
                'ipv6_address_link': '',
                'hardware_address': '',
                'rx_packets': '',
                'broadcast_address': '',
                'rx_bytes': '',
                'link_encap': 'Local',
                'metric': '',
                'txqueuelen': '',
                'net_mask': '',
                'ip_address': '',
                'collisions': '',
                'interface': 'lo',
                'tx_bytes': '',
                'mtu': '',
                'tx_packets': '',
                'ipv6_address_global': '',
            },
        ]

    def to_dict(self):
        return self._dict(
            {
                'name': 'dummy',
                'type': 'radio',  # maybe remove
                'os': 'dummyOS',
                'os_version': '0.1',
                'manufacturer': 'dummy inc.',
                'model': 'dummy model',
                'RAM_total': 65536,
                'uptime': 0,
                'uptime_tuple': (0, 0, 0),
                'interfaces': [
                    {
                        'type': 'wireless',
                        'name': 'wifi0',
                        'mac_address': 'de:9f:db:30:c9:c5',
                        'mtu': 1500,
                        'standard': '802.11n',
                        'channel': 5745,
                        'channel_width': 20,
                        'mode': 'ap',
                        'output_power': 18,
                        'tx_rate': None,
                        'rx_rate': None,
                        'dbm': -27,
                        'noise': -97,
                        'ip': [
                            {'version': 4, 'address': '192.168.1.1'},
                            {'version': 6, 'address': '2001:4c00:893b:fede::1'},
                        ],
                        'vap': [{'essid': 'dummyssid', 'bssid': '', 'encryption': ''}],
                    },
                    {
                        'type': 'ethernet',
                        'name': 'eth0',
                        'mac_address': 'de:9f:db:30:c9:c4',
                        'mtu': 1500,
                        'standard': 'fast',
                        'duplex': 'full',
                        'tx_rate': None,
                        'rx_rate': None,
                        'ip': [
                            {'version': 4, 'address': '192.168.1.2'},
                            {'version': 6, 'address': '2001:4c00:893b:fede::2'},
                        ],
                    },
                ],
                'antennas': [],
                'routing_protocols': [{'name': 'olsr', 'version': 'dummy version'}],
            }
        )
