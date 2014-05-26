import unittest
from netengine.backends.snmp import OpenWRT

from ..settings import settings


__all__ = ['TestSNMPOpenWRT']


class TestSNMPOpenWRT(unittest.TestCase):
    
    def setUp(self):
        self.host = settings['openwrt-snmp']['host']
        self.community = settings['openwrt-snmp']['community']
        self.port = settings['openwrt-snmp'].get('port', 161)
        
        self.device = OpenWRT(self.host, self.community, self.port)
        
    def test_os(self):
        self.assertTrue(type(self.device.os) == tuple)
    
    def test_manufacturer(self):
        self.assertIsNotNone(self.device.manufactuer)

    def test_name(self):
        self.assertTrue(type(self.device.name) == str)
    
    def test_uptime(self):
        self.assertTrue(type(self.device.uptime) == int)

    def test_uptime_tuple(self):
        self.assertTrue(type(self.device.uptime_tuple) == tuple)
    
    def test_get_interfaces(self):
        self.assertTrue(type(self.device.get_interfaces()) == list)
    
    def test_interfaces_speed(self):
        self.assertTrue(type(self.device.interfaces_speed) == list)
    
    def test_interfaces_bytes(self):
        self.assertTrue(type(self.device.interfaces_bytes) == list)
    
    def test_interfaces_MAC(self):
        self.assertTrue(type(self.device.interfaces_MAC) == list)
        
    def test_interfaces_type(self):
        self.assertTrue(type(self.device.interfaces_type) == list)
    
    def test_interfaces_mtu(self):
        self.assertTrue(type(self.device.interfaces_mtu) == list)

    def test_interfaces_state(self):
        self.assertTrue(type(self.device.interfaces_state) == list)
    
    def test_interfaces_to_dict(self):
        self.assertTrue(type(self.device.interfaces_to_dict) == list)
    
    def test_interface_addr_and_mask(self):
        self.assertTrue(type(self.interface_addr_and_mask) == list)
    
    def test_RAM_total(self):
        self.assertTrue(type(self.device.RAM_total) == int)
        
    def test_to_dict(self):
        self.assertTrue(isinstance(self.device.to_dict(), dict))
    
    def test_manufacturer_to_dict(self):
        self.assertIsNotNone(self.device.to_dict()['manufacturer'])
