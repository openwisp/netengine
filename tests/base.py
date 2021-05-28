import unittest

from netengine import get_version, __version__
from netengine.backends import BaseBackend
from netaddr import AddrFormatError


__all__ = ['TestBaseBackend']


class TestBaseBackend(unittest.TestCase):
    
    def test_version(self):
        get_version()
        __version__
    
    def test_dict(self):
        device = BaseBackend()
        dictionary = device._dict({})
        self.assertTrue(isinstance(dictionary, dict))
    
    def test_base_backend(self):
        device = BaseBackend()
        
        self.assertTrue(device.__netengine__)
        
        with self.assertRaises(NotImplementedError):
            device.validate()
        
        with self.assertRaises(NotImplementedError):
            device.to_dict()
        
        with self.assertRaises(NotImplementedError):
            device.to_json()
        
        with self.assertRaises(NotImplementedError):
            str(device)
        
        with self.assertRaises(NotImplementedError):
            device.__repr__()
        
        with self.assertRaises(NotImplementedError):
            device.__unicode__()
        
        with self.assertRaises(NotImplementedError):
            device.os
        
        with self.assertRaises(NotImplementedError):
            device.name
        
        with self.assertRaises(NotImplementedError):
            device.model
        
        with self.assertRaises(NotImplementedError):
            device.RAM_total
        
        with self.assertRaises(NotImplementedError):
            device.uptime
        
        with self.assertRaises(NotImplementedError):
            device.uptime_tuple
        
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
        
        with self.assertRaises(NotImplementedError):
            device.olsr
        
    def test_get_manufacturer_unicode(self):
        device = BaseBackend()
        with self.assertRaises(AddrFormatError):
            device.get_manufacturer(u"wrong MAC")
