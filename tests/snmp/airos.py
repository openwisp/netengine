import unittest
from netengine.backends.snmp import AirOS
from netengine.exceptions import NetEngineError

from ..settings import settings


__all__ = ['TestSNMPAirOS']


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
    
    def test_name(self):
        self.assertTrue(type(self.device.name) == str)
    
    def test_os(self):
        self.assertTrue(type(self.device.os) == tuple)
        
    def test_get_interfaces(self):
        self.assertTrue(type(self.device.get_interfaces()) == list)

    def test_get_interfaces_mtu(self):
        self.assertTrue(type(self.device.interfaces_mtu) == list)
    
    def test_interfaces_state(self):
        self.assertTrue(type(self.device.interfaces_state) == list)
    
    def test_interfaces_speed(self):
        self.assertTrue(type(self.device.interfaces_speed) == list)
        
    def test_interfaces_bytes(self):
        self.assertTrue(type(self.device.interfaces_bytes) == list)
    
    def test_interfaces_MAC(self):
        self.assertTrue(type(self.device.interfaces_MAC) == list)
    
    def test_interfaces_type(self):
        self.assertTrue(type(self.device.interfaces_type) == list)
    
    def test_interfaces_to_dict(self):
        self.assertTrue(type(self.device.interfaces_to_dict) == list)
        
    def test_wireless_dbm(self):
        self.assertTrue(type(self.device.wireless_dbm) == list)
    
    def test_interfaces_number(self):
        self.assertTrue(type(self.device.interfaces_number) == int)
    
    def test_wireless_to_dict(self):
        self.assertTrue(type(self.device.wireless_links) == list)

    def test_RAM_free(self):
        self.assertTrue(type(self.device.RAM_free) == int)
        
    def test_RAM_total(self):
        self.assertTrue(type(self.device.RAM_total) == int)

    def test_to_dict(self):
        self.assertTrue(isinstance(self.device.to_dict(), dict))
    
    def test_manufacturer_to_dict(self):
        self.assertIsNotNone(self.device.to_dict()['manufacturer'])
    
    def test_manufacturer(self):
        self.assertIsNotNone(self.device.manufacturer)
    
    def test_model(self):
        self.assertTrue(type(self.device.model) == str)
    
    def test_firmware(self):
        self.assertTrue(type(self.device.firmware) == str)
        
    def test_uptime(self):
        self.assertTrue(type(self.device.uptime) == int)
    
    def test_uptime_tuple(self):
        self.assertTrue(type(self.device.uptime_tuple) == tuple)