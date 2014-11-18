import unittest
import json

from netengine.utils import manufacturer_lookup
from netengine.exceptions import NetEngineError


__all__ = ['TestManufacturerLookup']


class TestManufacturerLookup(unittest.TestCase):
    def test_multiple_mac(self):
        all_capitalized_mac = "3C0E23DB1D1E"
        all_lowered_mac = "3C0E23db1d1e"
        mixed_dashed_mac = "3C-0E-23-DB-1D-1E"
        mixed_mac = "3c:0e-23:Db-1D-1e"

        self.assertEqual(manufacturer_lookup(all_capitalized_mac), "Cisco")
        self.assertEqual(manufacturer_lookup(all_lowered_mac), "Cisco")
        self.assertEqual(manufacturer_lookup(mixed_dashed_mac), "Cisco")
        self.assertEqual(manufacturer_lookup(mixed_mac), "Cisco")

    def test_error(self):
        with self.assertRaises(NetEngineError):
            manufacturer_lookup('ab:ab:ab:ab:ab:ab')
