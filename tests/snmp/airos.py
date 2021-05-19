import unittest
from mock import patch
from netengine.backends.snmp import AirOS
from netengine.exceptions import NetEngineError

from ..settings import settings
from ..static import MockOutputMixin


__all__ = ['TestSNMPAirOS']


class TestSNMPAirOS(unittest.TestCase, MockOutputMixin):
    
    def setUp(self):
        self.host = settings['airos-snmp']['host']
        self.community = settings['airos-snmp']['community']
        self.port = settings['airos-snmp'].get('port', 161)
        
        self.device = AirOS(self.host, self.community, port=self.port)
        self.oid_mock_data = self._load_mock_json('/test-airos-snmp.json')
        self.interfaces_patcher = patch(
            'netengine.backends.snmp.openwrt.SNMP._value_to_retrieve',
            return_value=[1, 2, 3, 4, 5]
        )
        self.nextcmd_patcher = patch(
            'netengine.backends.snmp.openwrt.SNMP.next',
            return_value=[0, 0, 0, [[[0, 0,]]] * 5]
        )
        self.get_value_patcher = patch(
            'netengine.backends.snmp.airos.AirOS.get',
            side_effect=lambda x: self._get_mocked_getcmd(
                oid=x, data=self.oid_mock_data
            ),
        )
        self.get_value_patcher.start()
    
    def test_get_value_error(self):
        with self.get_value_patcher as p:
            p.side_effect = lambda x: self.device._oid(x)
            with self.assertRaises(NetEngineError):
                self.device.get_value('.')
    
    def test_validate_negative_result(self):
        with self.get_value_patcher as p:
            p.side_effect = lambda x: self.device._oid(x)
            wrong = AirOS('10.40.0.254', 'wrong', 'wrong')
            self.assertRaises(NetEngineError, wrong.validate)
    
    def test_validate_positive_result(self):
        self.device.validate()
    
    def test_get(self):
        with self.get_value_patcher as p:
            p.side_effect = lambda x: self.device._oid(x)
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
        with self.interfaces_patcher:
            self.assertTrue(type(self.device.get_interfaces()) == list)

    def test_get_interfaces_mtu(self):
        with self.interfaces_patcher:
            self.assertTrue(type(self.device.interfaces_mtu) == list)
    
    def test_interfaces_state(self):
        with self.interfaces_patcher:
            self.assertTrue(type(self.device.interfaces_state) == list)
    
    def test_interfaces_speed(self):
        with self.interfaces_patcher:
            self.assertTrue(type(self.device.interfaces_speed) == list)
        
    def test_interfaces_bytes(self):
        with self.interfaces_patcher:
            self.assertTrue(type(self.device.interfaces_bytes) == list)
    
    def test_interfaces_MAC(self):
        with self.interfaces_patcher:
            self.assertTrue(type(self.device.interfaces_MAC) == list)
    
    def test_interfaces_type(self):
        with self.interfaces_patcher:
            self.assertTrue(type(self.device.interfaces_type) == list)
    
    def test_interfaces_to_dict(self):
        with self.interfaces_patcher:
            self.assertTrue(type(self.device.interfaces_to_dict) == list)

    def test_wireless_dbm(self):
        with self.nextcmd_patcher:
            self.assertTrue(type(self.device.wireless_dbm) == list)
    
    def test_interfaces_number(self):
        self.assertTrue(type(self.device.interfaces_number) == int)
    
    def test_wireless_to_dict(self):
        with self.interfaces_patcher, self.nextcmd_patcher as np:
            np.side_effect = lambda x: self._get_mocked_wireless_links(oid=x)
            self.assertTrue(type(self.device.wireless_links) == list)

    def test_RAM_free(self):
        self.assertTrue(type(self.device.RAM_free) == int)
        
    def test_RAM_total(self):
        self.assertTrue(type(self.device.RAM_total) == int)

    def test_to_dict(self):
        with self.interfaces_patcher, self.nextcmd_patcher as np:
            np.side_effect = lambda x: self._get_mocked_wireless_links(oid=x)
            self.assertTrue(isinstance(self.device.to_dict(), dict))
    
    def test_manufacturer_to_dict(self):
        with self.interfaces_patcher, self.nextcmd_patcher as np:
            np.side_effect = lambda x: self._get_mocked_wireless_links(oid=x)
            self.assertIsNotNone(self.device.to_dict()['manufacturer'])
    
    def test_manufacturer(self):
        with self.interfaces_patcher:
            self.assertIsNotNone(self.device.manufacturer)
    
    def test_model(self):
        self.assertTrue(type(self.device.model) == str)
    
    def test_firmware(self):
        self.assertTrue(type(self.device.firmware) == str)
        
    def test_uptime(self):
        self.assertTrue(type(self.device.uptime) == int)
    
    def test_uptime_tuple(self):
        self.assertTrue(type(self.device.uptime_tuple) == tuple)

    def tearDown(self):
        self.get_value_patcher.stop()
