import asyncio
import binascii
import inspect
import logging

import netaddr

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
except ImportError as exc:
    raise ImportError(
        'pysnmp library is not installed, install it with "pip install pysnmp"'
    ) from exc

from netengine.backends import BaseBackend
from netengine.exceptions import NetEngineError

__all__ = ["SNMP"]

logger = logging.getLogger(__name__)


class SNMP(BaseBackend):
    """SNMP base backend."""

    _oid_to_retrieve = None

    def __init__(self, host, community="public", agent="my-agent", port=161):
        self.host = host
        self.community = CommunityData(agent, community, mpModel=0)
        self.port = port

    def __str__(self):
        return f"<SNMP: {self.host}>"

    async def _command(self, command, oid):
        transport = await UdpTransportTarget.create((self.host, self.port))
        result = command(
            SnmpEngine(),
            self.community,
            transport,
            ContextData(),
            ObjectType(ObjectIdentity(oid)),
        )
        if inspect.isawaitable(result):
            return await result
        return result

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

    def _octet_to_mac(self, octet_mac):
        """Return a MAC address from an SNMP octet string."""
        mac_address = binascii.b2a_hex(octet_mac.encode("latin-1")).decode()
        if mac_address:
            mac_address = ":".join(
                mac_address[slice(i, i + 2)] for i in range(0, 12, 2)
            )
        return mac_address

    def _ascii_blocks_to_ipv6(self, ascii_string):
        """Convert an ASCII representation into an IPv6 address."""
        blocks = ascii_string.split(".")
        for index, block in enumerate(blocks):
            blocks[index] = format(int(block), "02x")
        return netaddr.IPAddress(
            ":".join("".join(blocks[slice(i, i + 2)]) for i in range(0, len(blocks), 2))
        )

    def _oid(self, oid):
        """Normalize an OID accepted by the public query methods."""
        if type(oid) not in (str, tuple, list):
            raise AttributeError("get accepts only strings, tuples or lists")
        if isinstance(oid, str):
            return oid.replace(" ", "").replace(",", ".")
        return ".".join(str(element) for element in oid)

    def walk(self, oid):
        """Retrieve an SNMP subtree in the format consumed by dump-backed calls."""
        result = {}
        error_indication, error_status, _, var_binds_list = self.next(oid)
        if error_indication:
            raise NetEngineError(error_indication)
        if error_status:
            raise NetEngineError(error_status)
        for var_binds in var_binds_list:
            for var_bind in var_binds:
                result[str(var_bind[0])] = [None, None, None, [var_bind]]
        return result

    def get(self, oid, snmpdump=None):
        """Execute an SNMP GET request or read its value from an SNMP dump."""
        oid = self._oid(oid)
        if snmpdump is not None:
            return snmpdump.get(oid, [None, None, None, [[None, ""]]])
        logger.info("SNMP GET %s", oid)
        return asyncio.run(self._command(get_cmd, oid))

    def next(self, oid, snmpdump=None):
        """Execute an SNMP walk request or read its values from an SNMP dump."""
        oid = self._oid(oid)
        if snmpdump is not None:
            items = (
                snmpdump.items(prefix=oid)
                if hasattr(snmpdump, "items") and not isinstance(snmpdump, dict)
                else (
                    (key, value)
                    for key, value in snmpdump.items()
                    if key.startswith(oid)
                )
            )
            return [None, 0, 0, [item[1][3] for item in items]]
        logger.info("SNMP NEXT %s", oid)
        return asyncio.run(self._walk(oid))

    def get_value(self, oid, snmpdump=None):
        """Return the OID value or raise NetEngineError."""
        result = self.get(oid, snmpdump=snmpdump)
        try:
            value = result[3][0][1]
            return value.decode("latin-1") if isinstance(value, bytes) else str(value)
        except IndexError as exc:
            raise NetEngineError(str(result[0])) from exc

    def _value_to_retrieve(self, snmpdump=None):
        """Return the interface indexes used by backend-specific methods."""
        if self._oid_to_retrieve is None:
            raise NetEngineError(
                "Please fix properly the _oid_to_retrieve string in OpenWRT or AirOS SNMP backend"
            )
        indexes = self.next(self._oid_to_retrieve, snmpdump=snmpdump)[3]
        return [int(index[0][1]) for index in indexes]
