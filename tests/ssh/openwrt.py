import unittest
import mock

from netengine.backends.ssh import OpenWRT

from ..settings import settings
from ..static import MockOutputMixin


__all__ = ['TestSSHOpenWRT']


class TestSSHOpenWRT(unittest.TestCase, MockOutputMixin):

    def setUp(self):
        self.host = settings['openwrt-ssh']['host']
        self.username = settings['openwrt-ssh']['username']
        self.password = settings['openwrt-ssh']['password']
        self.port = settings['openwrt-ssh'].get('port', 22)
        self.device = OpenWRT(self.host, self.username, self.password, self.port)

        # mock calls being made to devices
        ssh_mock_data = self._load_mock_json('/test-openwrt-ssh.json')
        self.ssh_patcher = mock.patch(
            'netengine.backends.ssh.openwrt.SSH.run',
            side_effect=lambda x: self._get_mocked_value(
                oid=x, data=ssh_mock_data
            ),
        )
        self.connect_patcher = mock.patch('paramiko.SSHClient.connect')
        if settings['disable_mocks']:
            self.ssh_patcher = self.DisableMock()
            self.connect_patcher = self.DisableMock()
        with self.connect_patcher as p:
            self.device.connect()
            p.assert_called_once()
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
