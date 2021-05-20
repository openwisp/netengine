import unittest
import mock

from netengine.backends.ssh import OpenWRT

from ..static import MockOutputMixin


__all__ = ['TestSSHOpenWRT']


class TestSSHOpenWRT(unittest.TestCase, MockOutputMixin):

    @mock.patch('paramiko.SSHClient.connect')
    def setUp(self, mocked_connect):
        self.device = OpenWRT('test-host.com', 'test-user', 'test-pass', 22)
        self.device.connect()
        mocked_connect.assert_called_once()
        ssh_mock_data = self._load_mock_json('/test-openwrt-ssh.json')
        self.ssh_patcher = mock.patch(
            'netengine.backends.ssh.openwrt.SSH.run',
            side_effect=lambda x: self._get_mocked_value(
                oid=x, data=ssh_mock_data
            ),
        )
        self.ssh_patcher.start()

    def test_properties(self):
        device = self.device
        device.os
        device.name
        device.olsr
        device.disconnect()

    def test_wireless_mode(self):
        self.assertTrue(self.device.wireless_mode in ['ap', 'sta'])

    def test_RAM_total(self):
        self.assertTrue(type(self.device.RAM_total) == int)

    def test_uptime(self):
        self.assertTrue(type(self.device.uptime) == int)

    def test_interfaces_to_dict(self):
        self.assertTrue(type(self.device.interfaces_to_dict) == dict)

    def test_uptime_tuple(self):
        self.assertTrue(type(self.device.uptime_tuple) == tuple)

    def test_to_dict(self):
        self.assertTrue(isinstance(self.device.to_dict(), dict))

    def test_filter_radio_interfaces(self):
        self.assertTrue(isinstance(self.device._filter_radio_interfaces(), dict))

    def test_filter_radio(self):
        self.assertTrue(isinstance(self.device._filter_radio(), dict))

    def test_manufacturer(self):
        self.assertTrue(type(self.device.manufacturer) == str)

    def test_filter_routing_protocols(self):
        self.assertTrue(isinstance(self.device._filter_routing_protocols(), list))

    def tearDown(self):
        self.ssh_patcher.stop()
