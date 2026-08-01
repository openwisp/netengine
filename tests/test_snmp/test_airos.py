import json
import unittest
from datetime import timezone
from unittest.mock import call, patch

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
            side_effect=lambda *args, **kwargs: self._get_mocked_walkcmd(
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
        wrong = AirOS("10.40.0.254", "wrong", "wrong")
        with patch(
            "netengine.backends.snmp.base.get_cmd",
            return_value=(Exception("request timed out"), 0, 0, []),
        ):
            with self.assertRaisesRegex(NetEngineError, "request timed out"):
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
        self.assertEqual(self.device.name(), "DeviceName")

    def test_os(self):
        self.assertEqual(self.device.os(), ("AirOS", "Linux DeviceName 2.6.32.71"))

    def test_get_interfaces(self):
        self.assertIsInstance(self.device.get_interfaces(), list)

    def test_interface_indexes_come_from_if_mib(self):
        with patch.object(
            self.device, "next", return_value=[None, 0, 0, [[[None, 1]]]]
        ) as next:
            self.assertEqual(self.device._value_to_retrieve(), [1])
        next.assert_called_once_with("1.3.6.1.2.1.2.2.1.1.", snmpdump=None)

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

    def test_unnamed_interface(self):
        """Unnamed interfaces must not be included in monitoring output."""
        self.oid_mock_data["1.3.6.1.2.1.2.2.1.2.2"] = ""
        interfaces = self.device.interfaces_to_dict()
        self.assertNotIn("", [interface["name"] for interface in interfaces])

    def test_dump_forwarding(self):
        """Dump-backed serialization must not make live SNMP requests."""
        snmpdump = {"unused": "dump"}
        with patch.object(self.device, "get_interfaces", return_value=[]):
            with patch.object(
                self.device, "get_wireless_interfaces", return_value=[]
            ) as method:
                self.device.interfaces_to_dict(snmpdump=snmpdump)
        method.assert_called_once_with(snmpdump=snmpdump)

    def test_wireless_dbm(self):
        self.assertIsInstance(self.device.wireless_dbm(), list)

    def test_interfaces_number(self):
        self.assertEqual(self.device.interfaces_number(), 5)

    def test_wireless_to_dict(self):
        self.assertIsInstance(self.device.wireless_links(), list)

    def test_RAM_free(self):
        self.assertEqual(self.device.RAM_free(), 67076096)

    def test_RAM_total(self):
        self.assertEqual(self.device.RAM_total(), 129302528)

    def test_to_dict(self):
        self.assertTrue(isinstance(self.device.to_dict(autowalk=False), dict))
        self.assertTrue(isinstance(self.device.to_dict(False), dict))

    def test_memory_cache(self):
        """NetJSON names cached memory ``cache``."""
        memory = self.device.to_dict(autowalk=False)["resources"]["memory"]
        self.assertIn("cache", memory, "Memory output must use the NetJSON cache key")

    def test_fresh_snapshot(self):
        """Consecutive serializations must not reuse interface counters."""
        first = self.device.to_dict(autowalk=False)
        self.oid_mock_data["1.3.6.1.2.1.2.2.1.16.1"] = "42"
        second = self.device.to_dict(autowalk=False)
        self.assertEqual(first["interfaces"][0]["statistics"]["tx_bytes"], 3214378817)
        self.assertEqual(second["interfaces"][0]["statistics"]["tx_bytes"], 42)

    def test_autowalk_roots(self):
        """AirOS metadata is split between standard and vendor OID roots."""
        with patch.object(self.device, "walk", return_value={}) as walk:
            with patch.object(self.device, "uptime", return_value=0):
                with patch.object(self.device, "local_time", return_value=0):
                    with patch.object(self.device, "name", return_value="device"):
                        with patch.object(self.device, "model", return_value="model"):
                            with patch.object(
                                self.device, "os", return_value=("AirOS", "Linux")
                            ):
                                with patch.object(
                                    self.device, "firmware", return_value="AirOS v1"
                                ):
                                    with patch.object(
                                        self.device,
                                        "resources_to_dict",
                                        return_value={},
                                    ):
                                        with patch.object(
                                            self.device,
                                            "interfaces_to_dict",
                                            return_value=[],
                                        ):
                                            self.device.to_dict()
                                            self.device.to_dict(snmpdump={})
        self.assertEqual(
            walk.call_args_list,
            [call("1.3.6"), call("1.2.840.10036")],
            "AirOS must preserve supplied dumps and autowalk both OID roots",
        )

    def test_autowalk_continues_without_vendor_data(self):
        with patch.object(
            self.device, "walk", side_effect=[{}, NetEngineError("unsupported")]
        ) as walk:
            with patch.object(self.device, "uptime", return_value=0):
                with patch.object(self.device, "local_time", return_value=0):
                    with patch.object(self.device, "name", return_value="device"):
                        with patch.object(self.device, "model", return_value="model"):
                            with patch.object(
                                self.device, "os", return_value=("AirOS", "Linux")
                            ):
                                with patch.object(
                                    self.device, "firmware", return_value="AirOS v1"
                                ):
                                    with patch.object(
                                        self.device,
                                        "resources_to_dict",
                                        return_value={},
                                    ):
                                        with patch.object(
                                            self.device,
                                            "interfaces_to_dict",
                                            return_value=[],
                                        ):
                                            with self.assertLogs(
                                                "netengine.backends.snmp.airos",
                                                "WARNING",
                                            ):
                                                result = self.device.to_dict()
        self.assertEqual(result["general"]["hostname"], "device")
        self.assertEqual(walk.call_args_list, [call("1.3.6"), call("1.2.840.10036")])

    def test_monitoring_metadata(self):
        """Serialized monitoring data follows the NetJSON metadata placement."""
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
        self.assertEqual(self.device.model(), "NanoStation Loco M2")

    def test_firmware(self):
        self.assertEqual(self.device.firmware(), "AirOS v5.5.12536.120406.1455")

    def test_uptime(self):
        self.assertEqual(self.device.uptime(), 373)

    def test_RAM_buffered(self):
        self.assertEqual(self.device.RAM_buffered(), 2711552)

    def test_RAM_cached(self):
        self.assertEqual(self.device.RAM_cached(), 0)

    def test_SWAP_total(self):
        self.assertEqual(self.device.SWAP_total(), 0)

    def test_swap_conversion(self):
        """AirOS reports swap values in KiB."""
        self.oid_mock_data["1.3.6.1.4.1.10002.1.1.1.2.1.0"] = "2"
        self.oid_mock_data["1.3.6.1.4.1.10002.1.1.1.2.2.0"] = "3"
        self.assertEqual(
            self.device.SWAP_total(),
            2048,
            "AirOS SWAP total must convert KiB to bytes",
        )
        self.assertEqual(
            self.device.SWAP_free(),
            3072,
            "AirOS SWAP free must convert KiB to bytes",
        )

    def test_SWAP_free(self):
        self.assertEqual(self.device.SWAP_free(), 0)

    def test_CPU_count(self):
        self.assertEqual(self.device.CPU_count(), 0)

    def test_local_time(self):
        self.assertEqual(self.device.local_time(), 1580734874)

    def test_local_time_utc(self):
        """AirOS does not expose a timezone, so timestamps use the UTC assumption."""
        with patch("netengine.backends.snmp.airos.datetime") as datetime:
            parsed_time = datetime.strptime.return_value
            self.device.local_time()
        parsed_time.replace.assert_called_once_with(tzinfo=timezone.utc)

    def test_load(self):
        self.assertEqual(self.device.load(), [0.51, 0.18, 0.24])

    def tearDown(self):
        patch.stopall()
