import json
import unittest

from netengine.backends.ssh import *
from netengine.exceptions import NetEngineError

from .settings import settings


__all__ = [
    'TestSSH',
    'TestSSHAirOS',
    'TestSSHOpenWRT'
]


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
        
        device.disconnect()
    
    def test_get_interface_mtu(self):
        interfaces = self.device.get_interfaces()
        
        # ensure MTU for first 2 interfaces is not empty
        self.assertNotEqual(interfaces[0]['mtu'], '')
        self.assertNotEqual(interfaces[1]['mtu'], '')


class TestSSHAirOS(unittest.TestCase):
    
    def setUp(self):
        self.host = settings['airos-ssh']['host']
        self.username = settings['airos-ssh']['username']
        self.password = settings['airos-ssh']['password']
        self.port = settings['airos-ssh'].get('port', 22)
        
        self.device = AirOS(self.host, self.username, self.password, self.port)
        self.device.connect()
    
    def test_to_dict(self):
        self.assertTrue(isinstance(self.device.to_dict(), dict))
    
    def test_to_json(self):
        json_string = self.device.to_json()
        self.assertTrue(isinstance(json_string, basestring))
        dictionary = json.loads(json_string)
        self.device.disconnect()
    
    def test_properties(self):
        device = self.device
        
        device._ubntbox
        device._systemcfg
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
        device.olsr
        device.disconnect()
    
    def test_run(self):
        self.device.run('ls -l')
        self.device.disconnect()
    
    def test_temp_methods(self):
        device = self.device
        self.assertTrue(type(device.get_interfaces()) is list)
        self.assertTrue(type(device.get_ipv6_of_interface('eth0')) is str)
        self.assertTrue(type(device.get_ipv6_of_interface('wrong')) is type(None))
        device.disconnect()


class TestSSHOpenWRT(unittest.TestCase):
    
    def setUp(self):
        self.host = settings['openwrt-ssh']['host']
        self.username = settings['openwrt-ssh']['username']
        self.password = settings['openwrt-ssh']['password']
        self.port = settings['openwrt-ssh'].get('port', 22)
        
        self.device = OpenWRT(self.host, self.username, self.password, self.port)
        self.device.connect()
    
    def test_properties(self):
        device = self.device
        
        device.os
        device.name
        device.olsr
        device.disconnect()
    
    def test_wireless_mode(self):
        self.assertTrue(self.device.wireless_mode in ['ap', 'sta'])

    def test_RAM_total(self):
        self.assertTrue(type(self.device.RAM_total) == int)

    def test_uptime(self):
        self.assertTrue(type(self.device.uptime) == int)

    def test_to_dict(self):
        self.assertTrue(isinstance(self.device.to_dict(), dict))

