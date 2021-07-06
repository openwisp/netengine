try:
    from pysnmp.entity.rfc3413.oneliner import cmdgen
except ImportError:
    raise ImportError(
        'pysnmp library is not installed, install it with "pip install pysnmp"'
    )

import binascii
import logging

import netaddr

from netengine.backends import BaseBackend
from netengine.exceptions import NetEngineError

__all__ = ['SNMP']

logger = logging.getLogger(__name__)


class SNMP(BaseBackend):
    """
    SNMP base backend
    """

    _oid_to_retrieve = None

    def __init__(self, host, community='public', agent='my-agent', port=161):
        """
        :host string: required
        :community string: defaults to public
        :agent string: defaults to my-agent
        :port integer: defaults to 161
        """
        self.host = host
        self.community = cmdgen.CommunityData(agent, community, 0)
        self.transport = cmdgen.UdpTransportTarget((host, port))
        self.port = port

    def __str__(self):
        """prints a human readable object description"""
        return f'<SNMP: {self.host}>'

    @property
    def _command(self):
        """
        alias to cmdgen.CommandGenerator()
        """
        return cmdgen.CommandGenerator()

    def _octet_to_mac(self, octet_mac):
        """
        returns a valid mac address for a given octetstring
        """
        mac_address = binascii.b2a_hex(octet_mac.encode()).decode()
        if mac_address != '':
            mac_address = ':'.join(
                [mac_address[slice(i, i + 2)] for i in range(0, 12, 2) if i != '']
            )
        return mac_address

    def _ascii_blocks_to_ipv6(self, ascii_string):
        """
        converts an ascii representation into ipv6 address
        """
        blocks = ascii_string.split('.')
        for b in range(len(blocks)):
            # convert each block of decimal into hexadecimal form without `0x` prefix
            blocks[b] = format(int(blocks[b]), '02x')
        # join the obtained list into a valid IP string
        res = netaddr.IPAddress(
            ':'.join(
                [''.join(blocks[slice(i, i + 2)]) for i in range(0, len(blocks), 2)]
            )
        )
        return res

    def _oid(self, oid):
        """
        returns valid oid value to be passed to getCmd() or nextCmd()
        """
        if type(oid) not in (str, tuple, list):
            raise AttributeError('get accepts only strings, tuples or lists')
        # allow string representations of oids with commas ,
        elif isinstance(oid, str):
            # ignore spaces
            oid = oid.replace(' ', '').replace(',', '.')
        # convert lists and tuples into strings
        else:
            # convert each list item to string
            oid = [str(element) for element in oid]
            oid = '.'.join(oid)

        # ensure is string (could be unicode)
        return str(oid)

    def get(self, oid):
        """
        alias to cmdgen.CommandGenerator().getCmd
        :oid string|tuple|list: string, tuple or list representing the OID to get

        example of valid oid parameters:
            * '1,3,6,1,2,1,1,5,0'
            * '1, 3, 6, 1, 2, 1, 1, 5, 0'
            * '1.3.6.1.2.1.1.5.0'
            * [1, 3, 6, 1, 2, 1, 1, 5, 0]
            * (1, 3, 6, 1, 2, 1, 1, 5, 0)
        """
        logger.info(f'DEBUG: SNMP GET {self._oid(oid)}')
        return self._command.getCmd(self.community, self.transport, self._oid(oid))

    def next(self, oid):
        """
        alias to cmdgen.CommandGenerator().nextCmd
        :oid string|tuple|list: string, tuple or list representing the OID to get

        example of valid oid parameters:
            * '1,3,6,1,2,1,1,5,0'
            * '1, 3, 6, 1, 2, 1, 1, 5, 0'
            * '1.3.6.1.2.1.1.5.0'
            * [1, 3, 6, 1, 2, 1, 1, 5, 0]
            * (1, 3, 6, 1, 2, 1, 1, 5, 0)
        """
        logger.info(f'DEBUG: SNMP NEXT {self._oid(oid)}')
        return self._command.nextCmd(self.community, self.transport, self._oid(oid))

    def get_value(self, oid):
        """
        returns value of oid, or raises NetEngineError Exception is anything wrong
        :oid string|tuple|list: string, tuple or list representing the OID to get
        """
        result = self.get(oid)
        try:
            return str(result[3][0][1])  # snmp stores results in several arrays
        except IndexError:
            raise NetEngineError(str(result[0]))

    def _value_to_retrieve(self):
        """
        return the final SNMP indexes for the interfaces to be used in the other methods and properties
        """
        value_to_retr = []

        if self._oid_to_retrieve is None:
            raise NetEngineError(
                'Please fix properly the _oid_to_retrieve string in OpenWRT or AirOS SNMP backend'
            )

        indexes = self.next(self._oid_to_retrieve)[3]

        for i in range(len(indexes)):
            value_to_retr.append(int(indexes[i][0][1]))

        return value_to_retr
