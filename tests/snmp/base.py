import unittest

from netengine.backends.snmp import SNMP
from netengine.exceptions import NetEngineError



__all__ = ['TestSNMP']


class TestSNMP(unittest.TestCase):

    def setUp(self):
        self.host = '0.0.0.0'
        self.community = 'public'
        self.port = 161
        
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
    
    def test_raised_exception(self):
        class WrongSNMPBackend(SNMP):
            pass
        
        device = WrongSNMPBackend(self.host, self.community)
        
        with self.assertRaises(NetEngineError):
            device._value_to_retrieve()
        
        # this time define the _oid_to_retrieve attribute
        class RightSNMPBackend(SNMP):
            _oid_to_retrieve = ''
        
        device = RightSNMPBackend(self.host, self.community)
        
        # now we expect a different kind of error
        with self.assertRaises(IndexError):
            device._value_to_retrieve()
