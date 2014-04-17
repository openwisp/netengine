import unittest

from netengine.backends.snmp import SNMP

from ..settings import settings


__all__ = ['TestSNMP']


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
