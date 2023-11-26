import unittest

from netengine.backends.snmp import SNMP
from netengine.exceptions import NetEngineError

from ..settings import settings

__all__ = ['TestSNMP']


class TestSNMP(unittest.TestCase):
    def setUp(self):
        self.host = settings['base-snmp']['host']
        self.community = settings['base-snmp']['community']
        self.port = settings['base-snmp'].get('port', 161)
        self.device = SNMP(self.host, self.community, self.port)

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

    def test_octet_to_mac(self):
        self.assertEqual(
            self.device._octet_to_mac('\x04\x0e<\xcaU_'), '04:0e:3c:c3:8a:55'
        )

    def test_oid(self):
        self.assertEqual(self.device._oid('1,3,6,1,2,1,1,5,0'), '1.3.6.1.2.1.1.5.0')
        self.assertEqual(
            self.device._oid('1, 3, 6, 1, 2, 1, 1, 5, 0'), '1.3.6.1.2.1.1.5.0',
        )
        self.assertEqual(
            self.device._oid([1, 3, 6, 1, 2, 1, 1, 5, 0]), '1.3.6.1.2.1.1.5.0',
        )
