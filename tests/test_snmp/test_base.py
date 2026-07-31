import unittest
from unittest.mock import patch

from netengine.backends.snmp import SNMP, AirOS
from netengine.exceptions import NetEngineError

__all__ = ["TestSNMP"]


class TestSNMP(unittest.TestCase):
    def setUp(self):
        self.device = AirOS("192.0.2.1")

    def test_instantiation(self):
        device = SNMP("192.0.2.1")
        self.assertTrue(device.__netengine__)
        self.assertIn("SNMP", str(device))

    def test_get_value_error_response(self):
        with patch.object(
            self.device,
            "get",
            return_value=(Exception("request timed out"), 0, 0, ()),
        ):
            with self.assertRaisesRegex(NetEngineError, "request timed out"):
                self.device.get_value("1.3.6.1.2.1.1.5.0")

    def test_walk_error_response(self):
        with patch.object(
            self.device,
            "next",
            return_value=(Exception("request timed out"), 0, 0, ()),
        ):
            self.assertEqual(self.device._value_to_retrieve(), [])

    def test_next_collects_walk_responses(self):
        async def walk_response(*args):
            yield None, 0, 0, ((0, 1),)
            yield None, 0, 0, ((0, 2),)

        with patch("netengine.backends.snmp.base.walk_cmd", side_effect=walk_response):
            self.assertEqual(
                self.device.next("1.3.6.1.2.1.1.5.0"),
                (None, 0, 0, [((0, 1),), ((0, 2),)]),
            )

    def test_raised_exception(self):
        class WrongSNMPBackend(SNMP):
            pass

        with self.assertRaises(NetEngineError):
            WrongSNMPBackend("192.0.2.1")._value_to_retrieve()

    def test_oid(self):
        self.assertEqual(self.device._oid("1,3,6,1,2,1,1,5,0"), "1.3.6.1.2.1.1.5.0")
        self.assertEqual(
            self.device._oid([1, 3, 6, 1, 2, 1, 1, 5, 0]), "1.3.6.1.2.1.1.5.0"
        )

    def test_mac_bytes(self):
        """MAC octets must be encoded one byte at a time."""
        self.assertEqual(
            self.device._octet_to_mac("\x08\x00\x27\x27\x80\x10"),
            "08:00:27:27:80:10",
            "SNMP octets must not be expanded by UTF-8 encoding",
        )
