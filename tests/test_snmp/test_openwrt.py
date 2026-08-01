import json
import unittest
from unittest.mock import call, patch

from jsonschema import validate
from pysnmp.proto.rfc1902 import OctetString

from netengine.backends.schema import schema
from netengine.backends.snmp import OpenWRT
from netengine.exceptions import NetEngineError

from ..settings import settings
from ..utils import MockOid, MockOutputMixin

__all__ = ["TestSNMPOpenWRT"]


class TestSNMPOpenWRT(unittest.TestCase, MockOutputMixin):
    def setUp(self):
        self.host = settings["openwrt-snmp"]["host"]
        self.community = settings["openwrt-snmp"]["community"]
        self.port = settings["openwrt-snmp"].get("port", 161)
        self.device = OpenWRT(
            host=self.host,
            community=self.community,
            port=self.port,
        )

        # mock calls being made to devices
        self.oid_mock_data = self._load_mock_json("/static/test-openwrt-snmp-oid.json")
        self.nextcmd_patcher = patch(
            "netengine.backends.snmp.base.walk_cmd",
            side_effect=lambda *args: self._get_mocked_walkcmd(
                self._get_mocked_nextcmd(*args)
            ),
        )
        self.getcmd_patcher = patch(
            "netengine.backends.snmp.base.get_cmd",
            side_effect=lambda *args: self._get_mocked_getcmd(
                data=self.oid_mock_data, input=args
            ),
        )
        self.getcmd_patcher.start()
        self.nextcmd_patcher.start()

    def test_os(self):
        self.assertEqual(
            self.device.os(),
            ("OpenWRT", "Linux 08-00-27-0A-F7-6A 4.14.221"),
        )

    def test_manufacturer(self):
        self.assertIsNotNone(self.device.manufacturer())

    def test_name(self):
        self.assertEqual(
            self.device.name(),
            "HeartOfGold",
            "OpenWRT device name must come from SNMP sysName",
        )

    def test_uptime(self):
        self.assertEqual(self.device.uptime(), 10339)

    def test_uptime_tuple(self):
        self.assertEqual(self.device.uptime_tuple(), (0, 2, 52))

    def test_get_interfaces(self):
        self.assertEqual(
            self.device.get_interfaces(),
            [
                "lo",
                "Device 8086:100e",
                "Device 8086:100e",
                "Device 8086:100e",
                "br-lan",
            ],
        )

    def test_memoized_accessors_use_the_current_dump(self):
        first_dump = {}
        second_dump = {}
        with patch.object(self.device, "_value_to_retrieve", return_value=[1]):
            with patch.object(
                self.device,
                "get_value",
                side_effect=lambda oid, snmpdump: (
                    "first" if snmpdump is first_dump else "second"
                ),
            ):
                self.assertEqual(self.device.get_interfaces(first_dump), ["first"])
                self.assertEqual(self.device.get_interfaces(second_dump), ["second"])

    def test_interfaces_speed(self):
        self.assertIsInstance(self.device.interfaces_speed(), list)

    def test_interfaces_bytes(self):
        self.assertIsInstance(self.device.interfaces_bytes(), list)

    def test_interfaces_MAC(self):
        self.assertIsInstance(self.device.interfaces_MAC(), list)

    def test_mac_indexes(self):
        """MAC lookups must use actual SNMP interface indexes."""
        values = {
            "1.3.6.1.2.1.2.2.1.6.1": "\x00\x11\x22\x33\x44\x55",
            "1.3.6.1.2.1.2.2.1.6.3": "\x00\x11\x22\x33\x44\x66",
        }
        with patch.object(self.device, "_value_to_retrieve", return_value=[1, 3]):
            with patch.object(
                self.device, "get_interfaces", return_value=["eth0", "eth1"]
            ):
                with patch.object(
                    self.device,
                    "next",
                    return_value=[None, 0, 0, [[None], [None]]],
                ):
                    with patch.object(
                        self.device,
                        "get_value",
                        side_effect=lambda oid, **kwargs: values[oid],
                    ) as get_value:
                        self.assertEqual(
                            self.device.interfaces_MAC(),
                            [
                                {"name": "eth0", "mac_address": "00:11:22:33:44:55"},
                                {"name": "eth1", "mac_address": "00:11:22:33:44:66"},
                            ],
                        )
        self.assertNotIn(
            "1.3.6.1.2.1.2.2.1.6.2",
            [call.args[0] for call in get_value.call_args_list],
            "MAC collection must not query indexes absent from the SNMP table",
        )

    def test_interfaces_type(self):
        self.assertIsInstance(self.device.interfaces_type(), list)

    def test_interfaces_mtu(self):
        self.assertIsInstance(self.device.interfaces_mtu(), list)

    def test_interfaces_state(self):
        self.assertIsInstance(self.device.interfaces_up(), list)

    def test_empty_interface(self):
        """Fallback interface records retain the boolean state consumed by serialization."""
        with patch.object(self.device, "_value_to_retrieve", return_value=[1]):
            with patch.object(self.device, "get_value", return_value=""):
                self.assertEqual(
                    self.device.interfaces_up(),
                    [{"name": "", "up": False}],
                    "Empty interface records must preserve the boolean up field",
                )

    def test_interfaces_to_dict(self):
        self.assertIsInstance(self.device.interfaces_to_dict(), list)

    def test_interface_fields(self):
        """Monitoring interface fields must match the NetJSON placement used by AirOS."""
        interface = self.device.interfaces_to_dict()[0]
        self.assertIn("mac", interface, "MAC addresses belong on the interface")
        self.assertIn("up", interface, "Interface state belongs on the interface")
        self.assertIn("mtu", interface, "MTU belongs on the interface")
        self.assertIn("addresses", interface, "Addresses belong on the interface")
        self.assertNotIn(
            "mac",
            interface["statistics"],
            "Interface metadata must not be nested in statistics",
        )

    def test_dump_forwarding(self):
        """Dump-backed serialization must not make live SNMP requests."""
        snmpdump = {"unused": "dump"}
        with patch.object(self.device, "get_interfaces", return_value=[]):
            with patch.object(
                self.device, "get_wireless_interfaces", return_value=[]
            ) as method:
                self.device.interfaces_to_dict(snmpdump=snmpdump)
        method.assert_called_once_with(snmpdump=snmpdump)

    def test_interface_addr_and_mask(self):
        self.assertIsInstance(self.device.interface_addr_and_mask(), dict)

    def test_interface_addr_and_mask_preserves_addresses_by_index(self):
        addresses = [
            [[None, OctetString(hexValue="c0000201")]],
            [[None, OctetString(hexValue="c0000202")]],
            [[None, OctetString(hexValue="c6336401")]],
        ]
        indexes = [[[None, 3]], [[None, 3]], [[None, 7]]]
        masks = [[[None, OctetString(hexValue="ffffff00")]]] * 3
        with patch.object(self.device, "_value_to_retrieve", return_value=[3, 7]):
            with patch.object(
                self.device, "get_interfaces", return_value=["duplicate", "duplicate"]
            ):
                with patch.object(
                    self.device,
                    "next",
                    side_effect=[
                        [None, 0, 0, addresses],
                        [None, 0, 0, indexes],
                        [None, 0, 0, masks],
                    ],
                ):
                    result = self.device.interface_addr_and_mask()
        self.assertEqual(
            result,
            {
                3: [
                    {
                        "family": "ipv4",
                        "address": "192.0.2.1",
                        "mask": "255.255.255.0",
                    },
                    {
                        "family": "ipv4",
                        "address": "192.0.2.2",
                        "mask": "255.255.255.0",
                    },
                ],
                7: [
                    {
                        "family": "ipv4",
                        "address": "198.51.100.1",
                        "mask": "255.255.255.0",
                    }
                ],
            },
        )

    def test_interface_addresses_use_indexes_and_preserve_duplicates(self):
        addresses = {
            3: [
                {"family": "ipv4", "address": "192.0.2.1", "mask": "255.255.255.0"},
                {"family": "ipv4", "address": "192.0.2.2", "mask": "255.255.255.0"},
            ],
            7: [{"family": "ipv4", "address": "198.51.100.1", "mask": "255.255.255.0"}],
        }
        with patch.object(self.device, "_value_to_retrieve", return_value=[3, 7]):
            with patch.object(
                self.device, "get_interfaces", return_value=["duplicate", "duplicate"]
            ):
                with patch.object(
                    self.device, "get_wireless_interfaces", return_value=[]
                ):
                    with patch.object(
                        self.device,
                        "interfaces_type",
                        return_value=[{"type": "ethernet"}] * 2,
                    ):
                        with patch.object(
                            self.device,
                            "interfaces_MAC",
                            return_value=[
                                {"mac_address": "00:00:00:00:00:03"},
                                {"mac_address": "00:00:00:00:00:07"},
                            ],
                        ):
                            with patch.object(
                                self.device,
                                "interfaces_bytes",
                                return_value=[{"rx": 0, "tx": 0}] * 2,
                            ):
                                with patch.object(
                                    self.device,
                                    "interfaces_up",
                                    return_value=[{"up": True}] * 2,
                                ):
                                    with patch.object(
                                        self.device,
                                        "interfaces_mtu",
                                        return_value=[{"mtu": 1500}] * 2,
                                    ):
                                        with patch.object(
                                            self.device,
                                            "interface_addr_and_mask",
                                            return_value=addresses,
                                        ):
                                            interfaces = (
                                                self.device.interfaces_to_dict()
                                            )
        self.assertEqual(interfaces[0]["addresses"], addresses[3])
        self.assertEqual(interfaces[1]["addresses"], addresses[7])

    def test_RAM_total(self):
        self.assertEqual(self.device.RAM_total(), 61452288)

    def test_RAM_shared(self):
        self.assertEqual(self.device.RAM_shared(), 98304)

    def test_RAM_cached(self):
        self.assertEqual(self.device.RAM_cached(), 7782400)

    def test_RAM_free(self):
        self.assertEqual(self.device.RAM_free(), 33722368)

    def test_SWAP_total(self):
        self.assertEqual(self.device.SWAP_total(), 0)

    def test_SWAP_free(self):
        self.assertEqual(self.device.SWAP_free(), 0)

    def test_CPU_count(self):
        self.assertEqual(self.device.CPU_count(), 2)

    def test_neighbors(self):
        self.assertEqual(
            self.device.neighbors(),
            [
                {
                    "mac": "04:0e:3c:ca:55:5f",
                    "state": "REACHABLE",
                    "interface": "br-lan",
                    "ip": "192.168.1.1",
                }
            ],
        )

    def test_unknown_neighbor_state(self):
        """Unknown neighbor states must not discard an otherwise valid neighbor."""
        neighbor_info = [
            [
                [
                    MockOid("1.3.6.1.2.1.4.35.1.4.5.1.4.192.168.1.1"),
                    OctetString("0x040e3cca555f"),
                ]
            ],
            [[MockOid("1.3.6.1.2.1.4.35.1.7.5.1.4.192.168.1.1"), 99]],
        ]
        with patch.object(
            self.device, "next", return_value=[None, 0, 0, neighbor_info]
        ):
            with patch.object(
                self.device,
                "get",
                return_value=[None, 0, 0, [[None, "br-lan"]]],
            ):
                self.assertEqual(
                    self.device.neighbors(),
                    [
                        {
                            "mac": "04:0e:3c:ca:55:5f",
                            "state": "UNKNOWN",
                            "interface": "br-lan",
                            "ip": "192.168.1.1",
                        }
                    ],
                )

    def test_neighbor_state_order(self):
        """Neighbor states must be matched by their OID suffix."""
        neighbor_info = [
            [
                [
                    MockOid("1.3.6.1.2.1.4.35.1.4.5.1.4.192.168.1.1"),
                    OctetString("0x040e3cca555f"),
                ]
            ],
            [
                [
                    MockOid("1.3.6.1.2.1.4.35.1.4.5.1.4.192.168.1.2"),
                    OctetString("0x040e3cca5560"),
                ]
            ],
            [[MockOid("1.3.6.1.2.1.4.35.1.7.5.1.4.192.168.1.2"), 2]],
            [[MockOid("1.3.6.1.2.1.4.35.1.7.5.1.4.192.168.1.1"), 1]],
        ]
        with patch.object(
            self.device, "next", return_value=[None, 0, 0, neighbor_info]
        ):
            with patch.object(
                self.device,
                "get",
                return_value=[None, 0, 0, [[None, "br-lan"]]],
            ):
                neighbors = self.device.neighbors()
        self.assertEqual(
            [neighbor["state"] for neighbor in neighbors],
            ["REACHABLE", "STALE"],
        )

    def test_local_time(self):
        self.assertEqual(self.device.local_time(), 1623391213)

    def test_local_time_offset(self):
        """Timezone-aware SNMP DateAndTime values convert to UTC timestamps."""
        self.oid_mock_data["1.3.6.1.2.1.25.1.2.0"] = {
            "type": "bytes",
            "value": "\\x07\\xe5\\x06\\x0b\\x06\\x00\\r\\x00-\\x05\\x1e",
        }
        self.assertEqual(
            self.device.local_time(),
            1623411013,
            "OpenWRT local time must apply the SNMP UTC offset",
        )

    def test_invalid_local_time(self):
        """SNMP DateAndTime supports only 8-byte and 11-byte values."""
        self.oid_mock_data["1.3.6.1.2.1.25.1.2.0"] = {
            "type": "bytes",
            "value": "\\x07\\xe5",
        }
        with self.assertRaisesRegex(
            NetEngineError,
            "unexpected DateAndTime length from SNMP: 2 bytes",
            msg="Unsupported SNMP DateAndTime values must report their size",
        ):
            self.device.local_time()

    def test_to_dict(self):
        device_dict = self.device.to_dict(autowalk=False)
        self.assertIsInstance(device_dict, dict)
        self.assertIsInstance(self.device.to_dict(False), dict)
        self.assertEqual(
            len(device_dict["interfaces"]),
            len(self.device.get_interfaces()),
        )

    def test_memory_cache(self):
        """NetJSON names cached memory ``cache``."""
        memory = self.device.to_dict(autowalk=False)["resources"]["memory"]
        self.assertIn("cache", memory, "Memory output must use the NetJSON cache key")

    def test_fresh_snapshot(self):
        """Consecutive serializations must not reuse interface counters."""
        first = self.device.to_dict(autowalk=False)
        self.oid_mock_data["1.3.6.1.2.1.2.2.1.16.1"] = "42"
        second = self.device.to_dict(autowalk=False)
        self.assertEqual(first["interfaces"][0]["statistics"]["tx_bytes"], 719914)
        self.assertEqual(second["interfaces"][0]["statistics"]["tx_bytes"], 42)

    def test_unnamed_interface(self):
        """Unnamed interfaces must not shift later interface metrics."""
        self.oid_mock_data["1.3.6.1.2.1.2.2.1.2.2"] = ""
        interfaces = self.device.to_dict(autowalk=False)["interfaces"]
        self.assertEqual(
            [interface["name"] for interface in interfaces],
            ["lo", "Device 8086:100e", "Device 8086:100e", "br-lan"],
            "Unnamed interfaces must not shift subsequent interface metrics",
        )

    def test_autowalk_root(self):
        """OpenWRT metrics require standard and vendor OID roots."""
        with patch.object(self.device, "walk", return_value={}) as walk:
            with patch.object(self.device, "name", return_value="device"):
                with patch.object(self.device, "uptime", return_value=0):
                    with patch.object(self.device, "local_time", return_value=0):
                        with patch.object(
                            self.device, "resources_to_dict", return_value={}
                        ):
                            with patch.object(
                                self.device, "interfaces_to_dict", return_value=[]
                            ):
                                with patch.object(
                                    self.device, "neighbors", return_value=[]
                                ):
                                    self.device.to_dict()
                                    self.device.to_dict(snmpdump={})
        self.assertEqual(
            walk.call_args_list,
            [call("1.3.6.1"), call("1.2.840.10036")],
            "OpenWRT must preserve supplied dumps and autowalk both OID roots",
        )

    def test_autowalk_continues_without_vendor_data(self):
        with patch.object(
            self.device, "walk", side_effect=[{}, NetEngineError("unsupported")]
        ) as walk:
            with patch.object(self.device, "name", return_value="device"):
                with patch.object(self.device, "uptime", return_value=0):
                    with patch.object(self.device, "local_time", return_value=0):
                        with patch.object(
                            self.device, "resources_to_dict", return_value={}
                        ):
                            with patch.object(
                                self.device, "interfaces_to_dict", return_value=[]
                            ):
                                with patch.object(
                                    self.device, "neighbors", return_value=[]
                                ):
                                    with self.assertLogs(
                                        "netengine.backends.snmp.openwrt", "WARNING"
                                    ):
                                        result = self.device.to_dict()
        self.assertEqual(result["general"]["hostname"], "device")
        self.assertEqual(walk.call_args_list, [call("1.3.6.1"), call("1.2.840.10036")])

    def test_interface_state(self):
        """Address-to-interface mappings belong to a single device instance."""
        other_device = OpenWRT(self.host, self.community, port=self.port)
        self.device._interface_dict[1] = "first-device-interface"
        self.assertNotIn(
            1,
            other_device._interface_dict,
            "OpenWRT interface address state must be isolated per device",
        )

    def test_netjson_compliance(self):
        device_dict = self.device.to_dict(autowalk=False)
        device_json = self.device.to_json(autowalk=False)
        validate(instance=device_dict, schema=schema)
        validate(instance=json.loads(device_json), schema=schema)

    def test_load(self):
        self.assertEqual(self.device.load(), [0.87, 0.37, 0.14])

    def tearDown(self):
        patch.stopall()
