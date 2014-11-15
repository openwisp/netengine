import json
import unittest

from netengine.backends.ssh import AirOS

from ..settings import settings


__all__ = ['TestSSHAirOS']


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
        self.assertTrue(type(device.get_ipv6_of_interface('eth0')) in [str, type(None)])
        self.assertTrue(type(device.get_ipv6_of_interface('wrong')) is type(None))
        device.disconnect()
