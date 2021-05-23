import json
import unittest

from netengine.backends.ssh import AirOS

from ..settings import settings
from ..static import MockOutputMixin


__all__ = ['TestSSHAirOS']


class TestSSHAirOS(unittest.TestCase, MockOutputMixin):

    def setUp(self):
        self.host = settings['airos-ssh']['host']
        self.username = settings['airos-ssh']['username']
        self.password = settings['airos-ssh']['password']
        self.port = settings['airos-ssh'].get('port', 22)
        self.device = AirOS(self.host, self.username, self.password, self.port)

        # mock calls being made to devices
        ssh_mock_data = self._load_mock_json('/test-airos-ssh.json')
        self.ssh_patcher = self._patch(
            'paramiko.SSHClient.exec_command',
            side_effect=lambda x: self._get_mocked_exec_command(
                command=x, data = ssh_mock_data
            ),
        )
        self.connect_patcher = self._patch('paramiko.SSHClient.connect')
        with self.connect_patcher as p:
            self.device.connect()
            p.assert_called_once()
        self.ssh_patcher.start()
        self.connect_patcher.start()

    def test_to_dict(self):
        self.assertTrue(isinstance(self.device.to_dict(), dict))

    def test_to_json(self):
        json_string = self.device.to_json()
        self.assertTrue(isinstance(json_string, basestring))
        dictionary = json.loads(json_string)
        self.device.disconnect()

    def test_properties(self):
        device = self.device

        device._ubntbox
        device._systemcfg
        device.os
        device.name
        device.model
        device.RAM_total
        device.ethernet_standard
        device.ethernet_duplex
        device.wireless_channel_width
        device.wireless_mode
        device.wireless_channel
        device.wireless_output_power
        device.wireless_dbm
        device.wireless_noise
        device.olsr
        device.disconnect()

    def test_run(self):
        self.device.run('ls -l')
        self.device.disconnect()

    def test_temp_methods(self):
        device = self.device
        self.assertTrue(type(device.get_ipv6_of_interface('eth0')) in [str, type(None)])
        self.assertTrue(type(device.get_ipv6_of_interface('wrong')) is type(None))
        device.disconnect()

    def test_uptime(self):
        self.assertIs(type(self.device.uptime), int)
