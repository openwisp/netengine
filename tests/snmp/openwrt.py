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
    
    def test_interfaces_MAC(self):
        self.assertTrue(type(self.device.interfaces_MAC) == list)
    
    def test_RAM_total(self):
        self.assertTrue(type(self.device.RAM_total) == int)
        
    def test_to_dict(self):
        self.assertTrue(isinstance(self.device.to_dict(), dict))
