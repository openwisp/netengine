import json
import unittest
from unittest.mock import patch

from jsonschema import validate
from pysnmp.entity.rfc3413.oneliner import cmdgen

from netengine.backends.schema import schema
from netengine.backends.snmp import OpenWRT

from ..settings import settings
from ..utils import MockOutputMixin, SpyMock

__all__ = ['TestSNMPOpenWRT']


class TestSNMPOpenWRT(unittest.TestCase, MockOutputMixin):
    def setUp(self):
        self.host = settings['openwrt-snmp']['host']
        self.community = settings['openwrt-snmp']['community']
        self.port = settings['openwrt-snmp'].get('port', 161)
        self.device = OpenWRT(host=self.host, community=self.community, port=self.port,)

        # mock calls being made to devices
        self.oid_mock_data = self._load_mock_json('/static/test-openwrt-snmp-oid.json')
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

    def test_os(self):
        self.assertIsInstance(self.device.os, tuple)

    def test_manufacturer(self):
        with self.nextcmd_patcher:
            self.assertIsNotNone(self.device.manufacturer)

    def test_name(self):
        self.assertIsInstance(self.device.name, str)

    def test_uptime(self):
        self.assertIsInstance(self.device.uptime, int)

    def test_uptime_tuple(self):
        self.assertIsInstance(self.device.uptime_tuple, tuple)

    def test_get_interfaces(self):
        with self.nextcmd_patcher:
            self.assertIsInstance(self.device.get_interfaces(), list)

    def test_interfaces_speed(self):
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

    def test_interfaces_mtu(self):
        with self.nextcmd_patcher:
            self.assertIsInstance(self.device.interfaces_mtu, list)

    def test_interfaces_state(self):
        with self.nextcmd_patcher:
            self.assertIsInstance(self.device.interfaces_state, list)

    def test_interfaces_to_dict(self):
        with self.nextcmd_patcher as p:
            p.return_value = (0, 0, 0, [])
            self.assertIsInstance(self.device.interfaces_to_dict, list)

    def test_interface_addr_and_mask(self):
        with self.nextcmd_patcher as p:
            p.return_value = (0, 0, 0, [])
            self.assertIsInstance(self.device.interface_addr_and_mask, dict)

    def test_RAM_total(self):
        self.assertIsInstance(self.device.RAM_total, int)

    def test_to_dict(self):
        with self.nextcmd_patcher as p:
            SpyMock._update_patch(p, _mock_return_value=[0, 0, 0, []])
            device_dict = self.device.to_dict()
            self.assertTrue(isinstance(device_dict, dict))
            self.assertEqual(
                len(device_dict['interfaces']), len(self.device.get_interfaces()),
            )

    def test_netjson_compliance(self):
        with self.nextcmd_patcher as p:
            SpyMock._update_patch(p, _mock_return_value=[0, 0, 0, []])
            device_dict = self.device.to_dict()
            device_json = self.device.to_json()
            validate(instance=device_dict, schema=schema)
            validate(instance=json.loads(device_json), schema=schema)

    def tearDown(self):
        patch.stopall()
