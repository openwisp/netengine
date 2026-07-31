try:
    from pysnmp.hlapi.v3arch.asyncio import (
        CommunityData,
        ContextData,
        ObjectIdentity,
        ObjectType,
        SnmpEngine,
        UdpTransportTarget,
        get_cmd,
        walk_cmd,
    )
except ImportError:
    raise ImportError(
        'pysnmp library is not installed, install it with "pip install pysnmp"'
    )

import asyncio
import logging

from netengine.backends import BaseBackend
from netengine.exceptions import NetEngineError

__all__ = ["SNMP"]

logger = logging.getLogger(__name__)


class SNMP(BaseBackend):
    """SNMP base backend"""

    _oid_to_retrieve = None

    def __init__(self, host, community="public", agent="my-agent", port=161):
        """:host string: required
        :community string: defaults to public
        :agent string: defaults to my-agent
        :port integer: defaults to 161
        """
        self.host = host
        self.community = CommunityData(agent, community, mpModel=0)
        self.port = port

    def __str__(self):
        """prints a human readable object description"""
        return f"<SNMP: {self.host}>"

    async def _command(self, command, oid):
        transport = await UdpTransportTarget.create((self.host, self.port))
        return await command(
            SnmpEngine(),
            self.community,
            transport,
            ContextData(),
            ObjectType(ObjectIdentity(oid)),
        )

    async def _walk(self, oid):
        transport = await UdpTransportTarget.create((self.host, self.port))
        result = (None, 0, 0, [])
        async for error_indication, error_status, error_index, var_binds in walk_cmd(
            SnmpEngine(),
            self.community,
            transport,
            ContextData(),
            ObjectType(ObjectIdentity(oid)),
        ):
            result = (error_indication, error_status, error_index, result[3])
            if error_indication or error_status:
                return result
            result[3].append(var_binds)
        return result

    def _oid(self, oid):
        """returns valid oid value to be passed to getCmd() or nextCmd()"""
        if type(oid) not in (str, tuple, list):
            raise AttributeError("get accepts only strings, tuples or lists")
        # allow string representations of oids with commas ,
        elif isinstance(oid, str):
            # ignore spaces
            oid = oid.replace(" ", "").replace(",", ".")
        # convert lists and tuples into strings
        else:
            # convert each list item to string
            oid = [str(element) for element in oid]
            oid = ".".join(oid)

        # ensure is string (could be unicode)
        return str(oid)

    def get(self, oid):
        """Execute an SNMP GET request.

        :oid string|tuple|list: string, tuple or list representing the OID
            to get

        example of valid oid parameters:
            - '1,3,6,1,2,1,1,5,0'
            - '1, 3, 6, 1, 2, 1, 1, 5, 0'
            - '1.3.6.1.2.1.1.5.0'
            - [1, 3, 6, 1, 2, 1, 1, 5, 0]
            - (1, 3, 6, 1, 2, 1, 1, 5, 0)
        """
        logger.info(f"DEBUG: SNMP GET {self._oid(oid)}")
        return asyncio.run(self._command(get_cmd, self._oid(oid)))

    def next(self, oid):
        """Execute an SNMP walk request.

        :oid string|tuple|list: string, tuple or list representing the OID
            to get

        example of valid oid parameters:
            - '1,3,6,1,2,1,1,5,0'
            - '1, 3, 6, 1, 2, 1, 1, 5, 0'
            - '1.3.6.1.2.1.1.5.0'
            - [1, 3, 6, 1, 2, 1, 1, 5, 0]
            - (1, 3, 6, 1, 2, 1, 1, 5, 0)
        """
        logger.info(f"DEBUG: SNMP NEXT {self._oid(oid)}")
        return asyncio.run(self._walk(self._oid(oid)))

    def get_value(self, oid):
        """Return the OID value or raise NetEngineError.

        :oid string|tuple|list: string, tuple or list representing the OID
            to get
        """
        result = self.get(oid)
        try:
            return str(result[3][0][1])  # snmp stores results in several arrays
        except IndexError:
            raise NetEngineError(str(result[0]))

    def _value_to_retrieve(self):
        """return the final SNMP indexes for the interfaces to be used in the other methods and properties"""
        value_to_retr = []

        if self._oid_to_retrieve is None:
            raise NetEngineError(
                "Please fix properly the _oid_to_retrieve string in OpenWRT "
                "or AirOS SNMP backend"
            )

        indexes = self.next(self._oid_to_retrieve)[3]

        for i in range(len(indexes)):
            value_to_retr.append(int(indexes[i][0][1]))

        return value_to_retr
