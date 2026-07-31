import json
import unittest
from unittest.mock import patch

from jsonschema import validate
from pysnmp.smi.error import NoSuchObjectError

from netengine.backends.schema import schema
from netengine.backends.snmp import AirOS
from netengine.exceptions import NetEngineError

from ..settings import settings
from ..utils import MockOutputMixin

__all__ = ["TestSNMPAirOS"]


class TestSNMPAirOS(unittest.TestCase, MockOutputMixin):
    def setUp(self):
        self.host = settings["airos-snmp"]["host"]
        self.community = settings["airos-snmp"]["community"]
        self.port = settings["airos-snmp"].get("port", 161)
        self.device = AirOS(self.host, self.community, port=self.port)

        # mock calls being made to devices
        self.oid_mock_data = self._load_mock_json("/static/test-airos-snmp.json")
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

    def test_get_value_error(self):
        self.getcmd_patcher.stop()
        with self.assertRaises(NoSuchObjectError):
            self.device.get_value(".")

    def test_validate_negative_result(self):
        self.getcmd_patcher.stop()
        wrong = AirOS("10.40.0.254", "wrong", "wrong")
        with self.assertRaises(NetEngineError):
            wrong.validate()

    def test_validate_positive_result(self):
        self.device.validate()

    def test_get(self):
        with self.assertRaises(AttributeError):
            self.device.get({})
        with self.assertRaises(AttributeError):
            self.device.get(object)
        self.device.get("1,3,6,1,2,1,1,5,0")
        self.device.get("1,3,6,1,2,1,1,5,0")
        self.device.get((1, 3, 6, 1, 2, 1, 1, 5, 0))
        self.device.get([1, 3, 6, 1, 2, 1, 1, 5, 0])

    def test_properties(self):
        device = self.device

        device.os()
        device.name()
        device.model()
        device.os()
        device.uptime()

    def test_name(self):
        self.assertIsInstance(self.device.name(), str)

    def test_os(self):
        self.assertIsInstance(self.device.os(), tuple)

    def test_get_interfaces(self):
        self.assertIsInstance(self.device.get_interfaces(), list)

    def test_get_interfaces_mtu(self):
        self.assertIsInstance(self.device.interfaces_mtu(), list)

    def test_interfaces_state(self):
        self.assertIsInstance(self.device.interfaces_state(), list)

    def test_interfaces_speed(self):
        self.assertIsInstance(self.device.interfaces_speed(), list)

    def test_interfaces_bytes(self):
        self.assertIsInstance(self.device.interfaces_bytes(), list)

    def test_interfaces_MAC(self):
        self.assertIsInstance(self.device.interfaces_MAC(), list)

    def test_interfaces_type(self):
        self.assertIsInstance(self.device.interfaces_type(), list)

    def test_interfaces_to_dict(self):
        self.assertIsInstance(self.device.interfaces_to_dict(), list)

    def test_wireless_dbm(self):
        self.assertIsInstance(self.device.wireless_dbm(), list)

    def test_interfaces_number(self):
        self.assertIsInstance(self.device.interfaces_number(), int)

    def test_wireless_to_dict(self):
        self.assertIsInstance(self.device.wireless_links(), list)

    def test_RAM_free(self):
        self.assertIsInstance(self.device.RAM_free(), int)

    def test_RAM_total(self):
        self.assertIsInstance(self.device.RAM_total(), int)

    def test_to_dict(self):
        self.assertTrue(isinstance(self.device.to_dict(autowalk=False), dict))

    def test_to_dict_includes_hostname_and_interface_macs(self):
        device_dict = self.device.to_dict(autowalk=False)
        self.assertEqual(device_dict["general"]["hostname"], "DeviceName")
        self.assertEqual(device_dict["hardware"]["model"], "NanoStation Loco M2")
        self.assertEqual(device_dict["operating_system"]["name"], "AirOS")
        self.assertEqual(
            device_dict["operating_system"]["description"],
            "Linux DeviceName 2.6.32.71",
        )
        self.assertEqual(
            device_dict["operating_system"]["version"],
            "AirOS v5.5.12536.120406.1455",
        )
        self.assertEqual(
            [interface["mac"] for interface in device_dict["interfaces"]],
            [interface["mac_address"] for interface in self.device.interfaces_MAC()],
        )
        self.assertNotIn("system_info", device_dict)

    def test_netjson_compliance(self):
        device_dict = self.device.to_dict(autowalk=False)
        device_json = self.device.to_json(autowalk=False)
        validate(instance=device_dict, schema=schema)
        validate(instance=json.loads(device_json), schema=schema)

    def test_manufacturer(self):
        self.assertIsNotNone(self.device.manufacturer())

    def test_model(self):
        self.assertIsInstance(self.device.model(), str)

    def test_firmware(self):
        self.assertIsInstance(self.device.firmware(), str)

    def test_uptime(self):
        self.assertIsInstance(self.device.uptime(), int)

    def test_RAM_buffered(self):
        self.assertIsInstance(self.device.RAM_buffered(), int)

    def test_RAM_cached(self):
        self.assertIsInstance(self.device.RAM_cached(), int)

    def test_SWAP_total(self):
        self.assertIsInstance(self.device.SWAP_total(), int)

    def test_SWAP_free(self):
        self.assertIsInstance(self.device.SWAP_free(), int)

    def test_CPU_count(self):
        self.assertIsInstance(self.device.CPU_count(), int)

    def test_local_time(self):
        self.assertIsInstance(self.device.local_time(), int)

    def test_load(self):
        load = self.device.load()
        self.assertIsInstance(load, list)
        self.assertEqual(len(load), 3)
        self.assertIsInstance(load[0], float)
        self.assertIsInstance(load[1], float)
        self.assertIsInstance(load[2], float)

    def tearDown(self):
        patch.stopall()
