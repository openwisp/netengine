import unittest
from netengine.backends.snmp import *

from .settings import settings


__all__ = [
    'TestSNMP',
    'TestAirOS',
    'TestOpenWRT'
]


class TestSNMP(unittest.TestCase):

    def setUp(self):
        self.host = settings['base-snmp']['host']
        self.community = settings['base-snmp']['community']
        
    def test_instantiation(self):
        device = SNMP(self.host, self.community)
        
        self.assertIn('SNMP', str(device))
    
    def test_not_implemented_methods(self):
        device = SNMP(self.host, self.community)
        
        with self.assertRaises(NotImplementedError):
            device.olsr
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


class TestAirOS(unittest.TestCase):
    
    def setUp(self):
        self.host = settings['airos-snmp']['host']
        self.community = settings['airos-snmp']['community']
        
        self.device = AirOS(self.host, self.community)
    
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
        self.host = settings['openwrt-snmp']['host']
        self.community = settings['openwrt-snmp']['community']
        
        self.device = OpenWRT(self.host, self.community)
    
    def test_properties(self):
        device = self.device
        
        device.olsr
        device.os
        device.name


if __name__ == '__main__':
    unittest.main()