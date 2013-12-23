import unittest
from netengine.backends.ssh import *

from .settings import settings


__all__ = [
    'TestSSH',
    'TestUbiquitiAirOS',
    'TestOpenWRT'
]


class TestSSH(unittest.TestCase):

    def setUp(self):
        self.host = settings['base-ssh']['host']
        self.username = settings['base-ssh']['username']
        self.password = settings['base-ssh']['password']
        
        self.device = SSH(self.host, self.username, self.password)
        self.device.connect()
    
    def test_wrong_connection(self):
        wrong = SSH('10.40.0.254', 'root', 'pwd')
        self.assertRaises(Exception, wrong.connect)
        
    def test_olsr(self):
        print self.device.olsr
    
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


class TestUbiquitiAirOS(unittest.TestCase):
    
    def setUp(self):
        self.host = settings['ubiquiti']['host']
        self.username = settings['ubiquiti']['username']
        self.password = settings['ubiquiti']['password']
        
        self.device = UbiquitiAirOS(self.host, self.username, self.password)
        self.device.connect()
    
    def test_properties(self):
        device = self.device
        
        device.olsr
        device.ubntbox
        device.systemcfg
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


class TestOpenWRT(unittest.TestCase):
    
    def setUp(self):
        self.host = settings['openwrt']['host']
        self.username = settings['openwrt']['username']
        self.password = settings['openwrt']['password']
        
        self.device = OpenWRT(self.host, self.username, self.password)
        self.device.connect()
    
    def test_properties(self):
        device = self.device
        
        device.olsr
        device.os
        device.name


if __name__ == '__main__':
    unittest.main()