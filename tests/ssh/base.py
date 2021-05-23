import unittest

from netengine.backends.ssh import SSH
from netengine.exceptions import NetEngineError
from paramiko.ssh_exception import SSHException

from ..settings import settings
from ..static import MockOutputMixin


__all__ = ['TestSSH']


class TestSSH(unittest.TestCase, MockOutputMixin):

    def setUp(self):
        self.host = settings['base-ssh']['host']
        self.username = settings['base-ssh']['username']
        self.password = settings['base-ssh']['password']
        self.port = settings['base-ssh'].get('port', 22)
        self.device = SSH(self.host, self.username, self.password, self.port)
        self.assertTrue(self.device.__netengine__)

        # mock calls being made to devices
        ssh_mock_data = self._load_mock_json('/test-base-ssh.json')
        self.exec_command_patcher = self._patch(
            'paramiko.SSHClient.exec_command',
            side_effect=lambda x: self._get_mocked_exec_command(
                command=x, data = ssh_mock_data
            ),
        )
        self.connect_patcher = self._patch('paramiko.SSHClient.connect')
        self.close_patcher = self._patch('paramiko.SSHClient.close')
        with self.connect_patcher as p:
            self.device.connect()
            p.assert_called_once_with(
                self.host, username=self.username, password=self.password, port=self.port
            )
        self.exec_command_patcher.start()
        self.connect_patcher.start()

    def test_validate_negative_result(self):
        with self.connect_patcher as p:
            p.side_effect = SSHException
            wrong = SSH('10.40.0.254', 'root', 'pwd')
            self.assertRaises(NetEngineError, wrong.validate)

    def test_validate_positive_result(self):
        with self.connect_patcher as cn, self.close_patcher as cl:
            self.device.disconnect()
            self.device.validate()
            cn.assert_called_once()
            if not settings['disable_mocks']:
                self.assertEqual(cl.call_count, 2)

    def test_olsr(self):
        print(self.device.olsr)

    def test_not_implemented_methods(self):
        device = self.device

        with self.assertRaises(NotImplementedError):
            device.os
        with self.assertRaises(NotImplementedError):
            device.name
        with self.assertRaises(NotImplementedError):
            device.model
        with self.assertRaises(NotImplementedError):
            device.RAM_total
        with self.assertRaises(NotImplementedError):
            device.ethernet_standard
        with self.assertRaises(NotImplementedError):
            device.ethernet_duplex
        with self.assertRaises(NotImplementedError):
            device.wireless_channel_width
        with self.assertRaises(NotImplementedError):
            device.wireless_mode
        with self.assertRaises(NotImplementedError):
            device.wireless_channel
        with self.assertRaises(NotImplementedError):
            device.wireless_output_power
        with self.assertRaises(NotImplementedError):
            device.wireless_dbm
        with self.assertRaises(NotImplementedError):
            device.wireless_noise

        device.disconnect()

    def test_iwconfig(self):
        self.assertIs(type(self.device.iwconfig()), list)

    def test_ifconfig(self):
        self.assertIs(type(self.device.ifconfig()), list)

    def test_get_interface_mtu(self):
        interfaces = self.device.ifconfig()
        # ensure MTU for first 2 interfaces is not empty
        self.assertNotEqual(interfaces[0]['mtu'], '')
        self.assertNotEqual(interfaces[1]['mtu'], '')

    def tearDown(self):
        self.exec_command_patcher.stop()
