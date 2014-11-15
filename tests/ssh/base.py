import unittest

from netengine.backends.ssh import SSH
from netengine.exceptions import NetEngineError

from ..settings import settings


__all__ = ['TestSSH']


class TestSSH(unittest.TestCase):

    def setUp(self):
        self.host = settings['base-ssh']['host']
        self.username = settings['base-ssh']['username']
        self.password = settings['base-ssh'].get('password', '')
        self.port = settings['base-ssh'].get('port', 22)
        
        self.device = SSH(self.host, self.username, self.password, self.port)
        self.assertTrue(self.device.__netengine__)
        self.device.connect()
    
    def test_validate_negative_result(self):
        wrong = SSH('10.40.0.254', 'root', 'pwd')
        self.assertRaises(NetEngineError, wrong.validate)
    
    def test_validate_positive_result(self):
        self.device.disconnect()
        self.device.validate()
        
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
    
    def test_get_interface_mtu(self):
        interfaces = self.device.get_interfaces()
        # ensure MTU for first 2 interfaces is not empty
        self.assertNotEqual(interfaces[0]['mtu'], '')
        self.assertNotEqual(interfaces[1]['mtu'], '')

    def test_iwconfig(self):
        self.assertIs(type(self.device.iwconfig()), list)
