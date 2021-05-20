import unittest
import mock

from netengine.backends.ssh import SSH
from netengine.exceptions import NetEngineError
from paramiko.ssh_exception import SSHException

from ..static import MockOutputMixin


__all__ = ['TestSSH']


class TestSSH(unittest.TestCase, MockOutputMixin):
    @mock.patch('paramiko.SSHClient.connect')
    def setUp(self, mocked_connect):
        self.host = 'test-host.com'
        self.username = 'test-user'
        self.password = 'test-password'
        self.port = 22
        self.device = SSH(self.host, self.username, self.password, self.port)
        self.assertTrue(self.device.__netengine__)
        self.device.connect()
        mocked_connect.assert_called_once_with(
            self.host, username=self.username, password=self.password, port=self.port
        )
        ssh_mock_data = self._load_mock_json('/test-base-ssh.json')
        self.exec_command_patcher = mock.patch(
            'netengine.backends.ssh.base.SSH.run',
            side_effect=lambda x: self._get_mocked_value(oid=x, data=ssh_mock_data),
        )
        self.exec_command_patcher.start()

    @mock.patch('paramiko.SSHClient.connect')
    def test_validate_negative_result(self, mocked_connect):
        mocked_connect.side_effect = SSHException
        wrong = SSH('10.40.0.254', 'root', 'pwd')
        self.assertRaises(NetEngineError, wrong.validate)

    @mock.patch('paramiko.SSHClient.close')
    @mock.patch('paramiko.SSHClient.connect')
    def test_validate_positive_result(self, mocked_connect, mocked_close):
        self.device.disconnect()
        self.device.validate()
        mocked_connect.assert_called_once()
        self.assertEqual(mocked_close.call_count, 2)

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
