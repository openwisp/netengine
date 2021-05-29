import unittest
from unittest.mock import patch

from pysnmp.entity.rfc3413.oneliner import cmdgen
from pysnmp.smi.error import NoSuchObjectError

from netengine.backends.snmp import AirOS
from netengine.exceptions import NetEngineError

from ..settings import settings
from ..utils import MockOutputMixin, SpyMock

__all__ = ['TestSNMPAirOS']


class TestSNMPAirOS(unittest.TestCase, MockOutputMixin):
    def setUp(self):
        self.host = settings['airos-snmp']['host']
        self.community = settings['airos-snmp']['community']
        self.port = settings['airos-snmp'].get('port', 161)
        self.device = AirOS(self.host, self.community, port=self.port)

        # mock calls being made to devices
        self.oid_mock_data = self._load_mock_json('/static/test-airos-snmp.json')
        self.nextcmd_patcher = SpyMock._patch(
            target=cmdgen.CommandGenerator,
            attribute='nextCmd',
            wrap_obj=self.device._command,
            return_value=[0, 0, 0, [[[0, 1]]] * 5],
        )
        self.getcmd_patcher = SpyMock._patch(
            target=cmdgen.CommandGenerator,
            attribute='getCmd',
            wrap_obj=self.device._command,
            side_effect=lambda *args: self._get_mocked_getcmd(
                data=self.oid_mock_data, input=args
            ),
        )
        self.getcmd_patcher.start()

    def test_get_value_error(self):
        self.getcmd_patcher.stop()
        with self.assertRaises(NoSuchObjectError):
            self.device.get_value('.')

    def test_validate_negative_result(self):
        self.getcmd_patcher.stop()
        wrong = AirOS('10.40.0.254', 'wrong', 'wrong')
        self.assertRaises(NetEngineError, wrong.validate)

    def test_validate_positive_result(self):
        self.device.validate()

    def test_get(self):
        with self.assertRaises(AttributeError):
            self.device.get({})
        with self.assertRaises(AttributeError):
            self.device.get(object)
        self.device.get('1,3,6,1,2,1,1,5,0')
        self.device.get('1,3,6,1,2,1,1,5,0')
        self.device.get((1, 3, 6, 1, 2, 1, 1, 5, 0))
        self.device.get([1, 3, 6, 1, 2, 1, 1, 5, 0])

    def test_properties(self):
        device = self.device

        device.os
        device.name
        device.model
        device.os
        device.uptime
        device.uptime_tuple

    def test_name(self):
        self.assertIsInstance(self.device.name, str)

    def test_os(self):
        self.assertIsInstance(self.device.os, tuple)

    def test_get_interfaces(self):
        with self.nextcmd_patcher:
            self.assertIsInstance(self.device.get_interfaces(), list)

    def test_get_interfaces_mtu(self):
        with self.nextcmd_patcher:
            self.assertIsInstance(self.device.interfaces_mtu, list)

    def test_interfaces_state(self):
        with self.nextcmd_patcher:
            self.assertIsInstance(self.device.interfaces_state, list)

    def test_interfaces_speed(self):
        with self.nextcmd_patcher:
            self.assertIsInstance(self.device.interfaces_speed, list)

    def test_interfaces_bytes(self):
        with self.nextcmd_patcher:
            self.assertIsInstance(self.device.interfaces_bytes, list)

    def test_interfaces_MAC(self):
        with self.nextcmd_patcher:
            self.assertIsInstance(self.device.interfaces_MAC, list)

    def test_interfaces_type(self):
        with self.nextcmd_patcher:
            self.assertIsInstance(self.device.interfaces_type, list)

    def test_interfaces_to_dict(self):
        with self.nextcmd_patcher:
            self.assertIsInstance(self.device.interfaces_to_dict, list)

    def test_wireless_dbm(self):
        with self.nextcmd_patcher:
            self.assertIsInstance(self.device.wireless_dbm, list)

    def test_interfaces_number(self):
        self.assertIsInstance(self.device.interfaces_number, int)

    def test_wireless_to_dict(self):
        with self.nextcmd_patcher as np:
            SpyMock._update_patch(
                np,
                _mock_side_effect=lambda *args: self._get_mocked_wireless_links(
                    data=args
                ),
            )
            self.assertIsInstance(self.device.wireless_links, list)

    def test_RAM_free(self):
        self.assertIsInstance(self.device.RAM_free, int)

    def test_RAM_total(self):
        self.assertIsInstance(self.device.RAM_total, int)

    def test_to_dict(self):
        with self.nextcmd_patcher as np:
            SpyMock._update_patch(
                np,
                _mock_side_effect=lambda *args: self._get_mocked_wireless_links(
                    data=args
                ),
            )
            self.assertTrue(isinstance(self.device.to_dict(), dict))

    def test_manufacturer_to_dict(self):
        with self.nextcmd_patcher as np:
            SpyMock._update_patch(
                np,
                _mock_side_effect=lambda *args: self._get_mocked_wireless_links(
                    data=args
                ),
            )
            self.assertIsNotNone(self.device.to_dict()['manufacturer'])

    def test_manufacturer(self):
        with self.nextcmd_patcher:
            self.assertIsNotNone(self.device.manufacturer)

    def test_model(self):
        self.assertIsInstance(self.device.model, str)

    def test_firmware(self):
        self.assertIsInstance(self.device.firmware, str)

    def test_uptime(self):
        self.assertIsInstance(self.device.uptime, int)

    def test_uptime_tuple(self):
        self.assertIsInstance(self.device.uptime_tuple, tuple)

    def tearDown(self):
        patch.stopall()
