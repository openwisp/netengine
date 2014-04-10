import unittest
from netengine.backends.snmp import *
from netengine.exceptions import NetEngineError

from .settings import settings


__all__ = [
    'TestSNMP',
    'TestSNMPAirOS',
    'TestSNMPOpenWRT'
]


class TestSNMP(unittest.TestCase):

    def setUp(self):
        self.host = settings['base-snmp']['host']
        self.community = settings['base-snmp']['community']
        self.port = settings['base-snmp'].get('port', 161)
        
    def test_instantiation(self):
        device = SNMP(self.host, self.community, self.port)
        self.assertTrue(device.__netengine__)
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


class TestSNMPAirOS(unittest.TestCase):
    
    def setUp(self):
        self.host = settings['airos-snmp']['host']
        self.community = settings['airos-snmp']['community']
        self.port = settings['airos-snmp'].get('port', 161)
        
        self.device = AirOS(self.host, self.community, port=self.port)
    
    def test_get_value_error(self):
        with self.assertRaises(NetEngineError):
            self.device.get_value('.')
    
    def test_validate_negative_result(self):
        wrong = AirOS('10.40.0.254', 'wrong', 'wrong')
        self.assertRaises(NetEngineError, wrong.validate)
    
    def test_validate_positive_result(self):
        self.device.validate()
    
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
    
    def test_os(self):
        self.assertTrue(type(self.device.os) == tuple)
        
    def test_get_interfaces(self):
        self.assertTrue(type(self.device.get_interfaces) == list)
        

class TestSNMPOpenWRT(unittest.TestCase):
    
    def setUp(self):
        self.host = settings['openwrt-snmp']['host']
        self.community = settings['openwrt-snmp']['community']
        self.port = settings['openwrt-snmp'].get('port', 161)
        
        self.device = OpenWRT(self.host, self.community, self.port)
        
    def test_os(self):
        self.assertTrue(type(self.device.os) == tuple)

    def test_name(self):
        self.assertTrue(type(self.device.name) == str)
    
    def test_uptime(self):
        self.assertTrue(type(self.device.uptime) == int)

    def test_uptime_tuple(self):
        self.assertTrue(type(self.device.uptime_tuple) == tuple)
    
    def test_get_interfaces(self):
        self.assertTrue(type(self.device.get_interfaces) == list)
    
    def test_RAM_total(self):
        self.assertTrue(type(self.device.RAM_total) == int)
        
    def test_to_dict(self):
        self.assertTrue(isinstance(self.device.to_dict(), dict))
