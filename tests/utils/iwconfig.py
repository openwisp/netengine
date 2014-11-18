import unittest
import json
from collections import OrderedDict

from netengine.shortcuts import OrderedDict
from netengine.utils.iwconfig import IwConfig


__all__ = ['TestIwConfigParser']


class TestIwConfigParser(unittest.TestCase):
    def test_openwrt_backfire(self):
        output = """lo        no wireless extensions.

eth0      no wireless extensions.

br-lan    no wireless extensions.

wifi0     no wireless extensions.

v63t63    no wireless extensions.

br-example  no wireless extensions.

r11v16    IEEE 802.11g  ESSID:"ExampleWifi"
          Mode:Master  Frequency:2.417 GHz  Access Point: 00:12:0E:B8:92:AF
          Bit Rate:0 kb/s   Tx-Power=16 dBm
          RTS thr:off   Fragment thr:off
          Encryption key:off
          Power Management:off
          Link Quality=69/70  Signal level=-27 dBm  Noise level=-96 dBm
          Rx invalid nwid:630390  Rx invalid crypt:1  Rx invalid frag:2
          Tx excessive retries:3  Invalid misc:4   Missed beacon:5

setup00   no wireless extensions."""
        i = IwConfig(output).to_python()

        self.assertEqual(len(i), 1)
        self.assertEqual(len(i[0].keys()), 21)
        self.assertTrue(type(i[0]) is OrderedDict)
        self.assertEqual(i[0]['name'], 'r11v16')
        self.assertEqual(i[0]['ieee'], '802.11g')
        self.assertEqual(i[0]['essid'], 'ExampleWifi')
        self.assertEqual(i[0]['mode'], 'Master')
        self.assertEqual(i[0]['frequency'], '2.417 GHz')
        self.assertEqual(i[0]['access_point'], '00:12:0E:B8:92:AF')
        self.assertEqual(i[0]['bit_rate'], '0 kb/s')
        self.assertEqual(i[0]['tx_power'], '16 dBm')
        self.assertEqual(i[0]['rts_thr'], 'off')
        self.assertEqual(i[0]['fragment_thr'], 'off')
        self.assertEqual(i[0]['encryption_key'], 'off')
        self.assertEqual(i[0]['power_management'], 'off')
        self.assertEqual(i[0]['link_quality'], '69/70')
        self.assertEqual(i[0]['signal_level'], '-27 dBm')
        self.assertEqual(i[0]['noise_level'], '-96 dBm')
        self.assertEqual(i[0]['rx_invalid_nwid'], '630390')
        self.assertEqual(i[0]['rx_invalid_crypt'], '1')
        self.assertEqual(i[0]['rx_invalid_frag'], '2')
        self.assertEqual(i[0]['tx_excessive_retries'], '3')
        self.assertEqual(i[0]['invalid_misc'], '4')
        self.assertEqual(i[0]['missed_beacon'], '5')

    def test_to_json(self):
        output = """wlan0    IEEE 802.11g  ESSID:"ExampleWifi"
          Mode:Master  Frequency:2.417 GHz  Access Point: 00:12:0E:B8:92:AF
          Bit Rate:0 kb/s   Tx-Power=16 dBm
          RTS thr:off   Fragment thr:off
          Encryption key:off
          Power Management:off
          Link Quality=69/70  Signal level=-27 dBm  Noise level=-96 dBm
          Rx invalid nwid:630390  Rx invalid crypt:1  Rx invalid frag:2
          Tx excessive retries:3  Invalid misc:4   Missed beacon:5"""
        json_output = IwConfig(output).to_json()
        i = json.loads(json_output)
        self.assertEqual(len(i), 1)
        self.assertEqual(len(i[0].keys()), 21)

    def test_to_netjson(self):
        output = """wlan0    IEEE 802.11g  ESSID:"ExampleWifi"
          Mode:Master  Frequency:2.417 GHz  Access Point: 00:12:0E:B8:92:AF
          Bit Rate:0 kb/s   Tx-Power=16 dBm
          RTS thr:off   Fragment thr:off
          Encryption key:off
          Power Management:off
          Link Quality=69/70  Signal level=-27 dBm  Noise level=-96 dBm
          Rx invalid nwid:630390  Rx invalid crypt:1  Rx invalid frag:2
          Tx excessive retries:3  Invalid misc:4   Missed beacon:5"""

        i = IwConfig(output).to_netjson(python=True)
        self.assertEqual(len(i), 1)
        self.assertTrue(type(i[0]) is OrderedDict)
        self.assertEqual(len(i[0].keys()), 3)
        self.assertEqual(len(i[0]['wireless'].keys()), 7)

        json_output = IwConfig(output).to_netjson()
        i = json.loads(json_output)
        self.assertEqual(len(i), 1)
        self.assertEqual(len(i[0].keys()), 3)
        self.assertEqual(len(i[0]['wireless'].keys()), 7)
        self.assertEqual(i[0]['mac'], '00:12:0E:B8:92:AF')
        self.assertEqual(i[0]['name'], 'wlan0')
        self.assertEqual(i[0]['wireless'], {
            "bitrate": "0 kb/s",
            "encryption": False,
            "essid": "ExampleWifi",
            "frag_threshold": "off",
            "mode": "ap",
            "rts_threshold": "off",
            "standard": "802.11g"
        })

    def test_bug_1(self):
        output = """wlan0     IEEE 802.11abgn  ESSID:"eduroam"
          Mode:Managed  Frequency:2.442 GHz  Access Point: DE:9F:DB:27:77:93
          Bit Rate=1 Mb/s   Tx-Power=16 dBm
          Retry  long limit:7   RTS thr:off   Fragment thr:off
          Power Management:off
          Link Quality=48/70  Signal level=-62 dBm
          Rx invalid nwid:0  Rx invalid crypt:0  Rx invalid frag:0
          Tx excessive retries:0  Invalid misc:4459   Missed beacon:0"""

        i = IwConfig(output).to_python()
        self.assertEqual(i[0]['essid'], 'eduroam')
        self.assertEqual(i[0]['retry_long_limit'], '7')
