import unittest
from unittest.mock import patch

from netengine.backends.snmp import AirOS
from netengine.exceptions import NetEngineError


class TestSNMP(unittest.TestCase):
    def setUp(self):
        self.device = AirOS("192.0.2.1")

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
