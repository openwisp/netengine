import unittest
import mock
from netengine.backends.snmp import OpenWRT

from ..settings import settings
from ..static import MockOutputMixin

__all__ = ['TestSNMPOpenWRT']


class TestSNMPOpenWRT(unittest.TestCase, MockOutputMixin):
    def setUp(self):
        self.host = settings['openwrt-snmp']['host']
        self.community = settings['openwrt-snmp']['community']
        self.port = settings['openwrt-snmp'].get('port', 161)

        self.device = OpenWRT(self.host, self.community, self.port)

        self.oid_mock_data = self._load_mock_json('/test-openwrt-snmp-oid.json')
        self.get_value_patcher = mock.patch(
            'netengine.backends.snmp.openwrt.OpenWRT.get_value',
            side_effect=lambda x: self._get_mocked_value(
                oid=x, data=self.oid_mock_data
            ).encode('ascii', 'ignore'),
        )
        self.get_value_patcher.start()

    def test_os(self):
        self.assertTrue(type(self.device.os) == tuple)

    @mock.patch('netengine.backends.snmp.openwrt.SNMP._value_to_retrieve')
    @mock.patch('netengine.backends.snmp.openwrt.SNMP.next')
    def test_manufacturer(self, mock_nextcmd, mock_value_to_retr):
        mock_value_to_retr.return_value = [1, 2, 3, 4, 5]
        mock_nextcmd.return_value = [0, 0, 0, [0] * 5]
        self.assertIsNotNone(self.device.manufacturer)
        mock_nextcmd.assert_called_once_with('1.3.6.1.2.1.2.2.1.6.')

    def test_name(self):
        self.assertTrue(type(self.device.name) == str)

    def test_uptime(self):
        self.assertTrue(type(self.device.uptime) == int)

    def test_uptime_tuple(self):
        self.assertTrue(type(self.device.uptime_tuple) == tuple)

    @mock.patch('netengine.backends.snmp.openwrt.SNMP._value_to_retrieve')
    def test_get_interfaces(self, mock_interfaces_count):
        mock_interfaces_count.return_value = [1, 2, 3, 4, 5]
        self.assertTrue(type(self.device.get_interfaces()) == list)

    def test_interfaces_speed(self):
        self.assertTrue(type(self.device.interfaces_speed) == list)

    @mock.patch('netengine.backends.snmp.openwrt.SNMP._value_to_retrieve')
    def test_interfaces_bytes(self, mock_interfaces_count):
        self.assertTrue(type(self.device.interfaces_bytes) == list)

    @mock.patch('netengine.backends.snmp.openwrt.SNMP._value_to_retrieve')
    @mock.patch('netengine.backends.snmp.openwrt.SNMP.next')
    def test_interfaces_MAC(self, mock_nextcmd, mock_interfaces_count):
        mock_interfaces_count.return_value = [1, 2, 3, 4, 5]
        mock_nextcmd.return_value = [0, 0, 0, [0] * 5]
        self.assertTrue(type(self.device.interfaces_MAC) == list)

    @mock.patch('netengine.backends.snmp.openwrt.SNMP._value_to_retrieve')
    def test_interfaces_type(self, mock_interfaces_count):
        mock_interfaces_count.return_value = [1, 2, 3, 4, 5]
        self.assertTrue(type(self.device.interfaces_type) == list)

    @mock.patch('netengine.backends.snmp.openwrt.SNMP._value_to_retrieve')
    def test_interfaces_mtu(self, mock_interfaces_count):
        mock_interfaces_count.return_value = [1, 2, 3, 4, 5]
        self.assertTrue(type(self.device.interfaces_mtu) == list)

    @mock.patch('netengine.backends.snmp.openwrt.SNMP._value_to_retrieve')
    def test_interfaces_state(self, mock_interfaces_count):
        mock_interfaces_count.return_value = [1, 2, 3, 4, 5]
        self.assertTrue(type(self.device.interfaces_state) == list)

    @mock.patch('netengine.backends.snmp.openwrt.SNMP.next')
    def test_interfaces_to_dict(self, mock_nextcmd):
        mock_nextcmd.return_value = (0, 0, 0, [])
        self.assertTrue(type(self.device.interfaces_to_dict) == list)

    @mock.patch('netengine.backends.snmp.openwrt.SNMP.next')
    def test_interface_addr_and_mask(self, mock_nextcmd):
        mock_nextcmd.return_value = (0, 0, 0, [])
        self.assertTrue(type(self.device.interface_addr_and_mask) == dict)

    def test_RAM_total(self):
        self.assertTrue(type(self.device.RAM_total) == int)

    @mock.patch('netengine.backends.snmp.openwrt.SNMP._value_to_retrieve')
    @mock.patch('netengine.backends.snmp.openwrt.SNMP.next')
    def test_to_dict(self, mock_nextcmd, mock_interfaces_count):
        mock_interfaces_count.return_value = [1, 2, 3, 4, 5]
        mock_nextcmd.return_value = [0, 0, 0, [0] * 5]
        device_dict = self.device.to_dict()

        self.assertTrue(isinstance(device_dict, dict))
        self.assertEqual(
            len(device_dict['interfaces']), len(self.device.get_interfaces())
        )

    @mock.patch('netengine.backends.snmp.openwrt.SNMP._value_to_retrieve')
    @mock.patch('netengine.backends.snmp.openwrt.SNMP.next')
    def test_manufacturer_to_dict(self, mock_nextcmd, mock_interfaces_count):
        mock_interfaces_count.return_value = [1, 2, 3, 4, 5]
        mock_nextcmd.return_value = [0, 0, 0, [0] * 5]
        self.assertIsNotNone(self.device.to_dict()['manufacturer'])

    def tearDown(self):
        self.get_value_patcher.stop()
