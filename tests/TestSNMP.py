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
        self.port = settings['base-snmp'].get('port', 161)
        
    def test_instantiation(self):
        device = SNMP(self.host, self.community, self.port)
        
        self.assertIn('SNMP', str(device))
    
    def test_not_implemented_methods(self):
        device = SNMP(self.host, self.community)
        
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
        self.port = settings['airos-snmp'].get('port', 161)
        
        self.device = AirOS(self.host, self.community, port=self.port)
    
    def test_get(self):
        with self.assertRaises(AttributeError):
            self.device.get({})
        
        with self.assertRaises(AttributeError):
            self.device.get(object)
        
        self.device.get('1,3,6,1,2,1,1,5,0')
        self.device.get(u'1,3,6,1,2,1,1,5,0')
        self.device.get((1,3,6,1,2,1,1,5,0))
        self.device.get([1,3,6,1,2,1,1,5,0])
    
    def test_properties(self):
        device = self.device
        
        device.os
        device.name
        device.model
        device.os
        device.uptime
        device.uptime_tuple


class TestOpenWRT(unittest.TestCase):
    
    def setUp(self):
        self.host = settings['openwrt-snmp']['host']
        self.community = settings['openwrt-snmp']['community']
        self.port = settings['openwrt-snmp'].get('port', 161)
        
        self.device = OpenWRT(self.host, self.community, self.port)


if __name__ == '__main__':
    unittest.main()