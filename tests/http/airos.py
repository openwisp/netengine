import unittest
from netengine.backends.http import AirOS

from ..settings import settings


__all__ = ['TestHTTP']


class TestHTTP(unittest.TestCase):

    def setUp(self):
        self.host = settings['base-http']['host']
        self.username = settings['base-http']['username']
        self.password = settings['base-http']['password']
        self.device = AirOS(self.host, self.username, self.password)
        self.assertTrue(self.device.__netengine__)

    def test_info(self):
        self.assertTrue(type(self.device.info) == dict)

    def test_iflist(self):
        self.assertTrue(type(self.device.iflist) == dict)

    def test_name(self):
        self.assertTrue(type(self.device.name) == str)

    def test_firewall(self):
        self.assertTrue(type(self.device.firewall) == dict)

    def test_host_info(self):
        self.assertTrue(type(self.device.host_info) == dict)

    def test_uptime(self):
        self.assertTrue(type(self.device.uptime) == str)

    def test_airview(self):
        self.assertTrue(type(self.device.airview) == dict)

    def test_services(self):
        self.assertTrue(type(self.device.services) == dict)

    def test_interfaces(self):
        self.assertTrue(type(self.device.interfaces) == list)

    def test_interfaces_properties(self):
        self.assertTrue(type(self.device.interfaces_properties) == dict)

    def test_wireless(self):
        self.assertTrue(type(self.device.services) == dict)

    def test_wireless_stats(self):
        self.assertTrue(type(self.device.services) == dict)

    def test_wireless_polling(self):
        self.assertTrue(type(self.device.wireless_polling) == dict)

    def test_ssid(self):
        self.assertTrue(type(self.device.ssid) == str)

    def test_frequency(self):
        self.assertTrue(type(self.device.frequency) == str)

    def test_rates(self):
        self.assertTrue(type(self.device.rates) == list)

    def test_ap_addr(self):
        self.assertTrue(type(self.device.ap_addr) == str)

    def test_noisefloor(self):
        self.assertTrue(type(self.device.noisefloor) == int)

    def test_mode(self):
        self.assertTrue(type(self.device.mode) == str)

    def test_uptime_tuple(self):
        self.assertTrue(type(self.device.uptime_tuple) == tuple)

    def test_connected_stations(self):
        self.assertTrue(type(self.device.uptime_tuple) == tuple)

    def test_to_dict(self):
        self.assertTrue(isinstance(self.device.to_dict(), dict))
