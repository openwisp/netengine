import json
import unittest
from unittest.mock import patch

from jsonschema import validate

from netengine.backends.schema import schema
from netengine.backends.snmp import OpenWRT

from ..settings import settings
from ..utils import MockOutputMixin

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
        self.assertIsInstance(self.device.os(), tuple)

    def test_manufacturer(self):
        self.assertIsNotNone(self.device.manufacturer())

    def test_name(self):
        self.assertEqual(
            self.device.name(),
            "HeartOfGold",
            "OpenWRT device name must come from SNMP sysName",
        )

    def test_uptime(self):
        self.assertIsInstance(self.device.uptime(), int)

    def test_uptime_tuple(self):
        self.assertIsInstance(self.device.uptime_tuple(), tuple)

    def test_get_interfaces(self):
        self.assertIsInstance(self.device.get_interfaces(), list)

    def test_interfaces_speed(self):
        self.assertIsInstance(self.device.interfaces_speed(), list)

    def test_interfaces_bytes(self):
        self.assertIsInstance(self.device.interfaces_bytes(), list)

    def test_interfaces_MAC(self):
        self.assertIsInstance(self.device.interfaces_MAC(), list)

    def test_interfaces_type(self):
        self.assertIsInstance(self.device.interfaces_type(), list)

    def test_interfaces_mtu(self):
        self.assertIsInstance(self.device.interfaces_mtu(), list)

    def test_interfaces_state(self):
        self.assertIsInstance(self.device.interfaces_up(), list)

    def test_interfaces_to_dict(self):
        self.assertIsInstance(self.device.interfaces_to_dict(), list)

    def test_interface_addr_and_mask(self):
        self.assertIsInstance(self.device.interface_addr_and_mask(), dict)

    def test_RAM_total(self):
        self.assertIsInstance(self.device.RAM_total(), int)

    def test_RAM_shared(self):
        self.assertIsInstance(self.device.RAM_shared(), int)

    def test_RAM_cached(self):
        self.assertIsInstance(self.device.RAM_cached(), int)

    def test_RAM_free(self):
        self.assertIsInstance(self.device.RAM_free(), int)

    def test_SWAP_total(self):
        self.assertIsInstance(self.device.SWAP_total(), int)

    def test_SWAP_free(self):
        self.assertIsInstance(self.device.SWAP_free(), int)

    def test_CPU_count(self):
        self.assertIsInstance(self.device.CPU_count(), int)

    def test_neighbors(self):
        self.assertIsInstance(self.device.neighbors(), list)

    def test_local_time(self):
        self.assertIsInstance(self.device.local_time(), int)

    def test_local_time_applies_snmp_timezone_offset(self):
        self.oid_mock_data["1.3.6.1.2.1.25.1.2.0"] = {
            "type": "bytes",
            "value": "\\x07\\xe5\\x06\\x0b\\x06\\x00\\r\\x00-\\x05\\x1e",
        }
        self.assertEqual(
            self.device.local_time(),
            1623411013,
            "OpenWRT local time must apply the SNMP UTC offset",
        )

    def test_to_dict(self):
        device_dict = self.device.to_dict(autowalk=False)
        self.assertIsInstance(device_dict, dict)
        self.assertEqual(
            len(device_dict["interfaces"]),
            len(self.device.get_interfaces()),
        )

    def test_netjson_compliance(self):
        device_dict = self.device.to_dict(autowalk=False)
        device_json = self.device.to_json(autowalk=False)
        validate(instance=device_dict, schema=schema)
        validate(instance=json.loads(device_json), schema=schema)

    def test_load(self):
        load = self.device.load()
        self.assertIsInstance(load, list)
        self.assertEqual(len(load), 3)
        self.assertIsInstance(load[0], float)
        self.assertIsInstance(load[1], float)
        self.assertIsInstance(load[2], float)

    def tearDown(self):
        patch.stopall()
