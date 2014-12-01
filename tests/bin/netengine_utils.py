import unittest
import json
import subprocess as sub

from netengine import get_version


__all__ = [
    'TestNetengineUtilsIfConfig',
    'TestNetengineUtilsIwConfig',
    'TestNetengineUtilsManufacturerLookup'
]


class TestNetengineUtilsIfConfig(unittest.TestCase):

    def test_version(self):
        p = sub.Popen(['netengine-utils', '--version'], stdout=sub.PIPE, stderr=sub.PIPE)
        self.assertIn(get_version(), p.communicate()[1])
        # ensure exit code is ok
        self.assertEqual(p.returncode, 0)

        p = sub.Popen(['netengine-utils', '-v'], stdout=sub.PIPE, stderr=sub.PIPE)
        self.assertIn(get_version(), p.communicate()[1])
        # ensure exit code is ok
        self.assertEqual(p.returncode, 0)

    def test_ifconfig(self):
        p = sub.Popen(['netengine-utils', 'ifconfig'], stdout=sub.PIPE, stderr=sub.PIPE)
        i = json.loads(p.communicate()[0])
        # ensure exit code is ok
        self.assertEqual(p.returncode, 0)
        self.assertEqual(type(i), list)
        self.assertEqual(type(i[0]), dict)
        self.assertIn('name', i[0])
        self.assertIn('link_encap', i[0])

    def test_ifconfig_netjson(self):
        p = sub.Popen(['netengine-utils', 'ifconfig', '--netjson'], stdout=sub.PIPE, stderr=sub.PIPE)
        i = json.loads(p.communicate()[0])
        # ensure exit code is ok
        self.assertEqual(p.returncode, 0)
        self.assertEqual(type(i), list)
        self.assertEqual(type(i[0]), dict)
        self.assertIn('name', i[0])
        self.assertIn('mac', i[0])

    def test_ifconfig_value(self):
        value = """eth0      Link encap:Ethernet  HWaddr 00:27:22:4D:7C:55
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:81885479 errors:0 dropped:0 overruns:0 frame:0
          TX packets:35544276 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000
          RX bytes:1559559756 (1.4 GiB)  TX bytes:2237569800 (2.0 GiB)
          Interrupt:4 Base address:0x1000

lo        Link encap:Local Loopback
          inet addr:127.0.0.1  Mask:255.0.0.0
          UP LOOPBACK RUNNING  MTU:16436  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:0 (0.0 B)  TX bytes:0 (0.0 B)"""

        p = sub.Popen(['netengine-utils', 'ifconfig', '--value', value], stdout=sub.PIPE, stderr=sub.PIPE)
        i = json.loads(p.communicate()[0])
        # ensure exit code is ok
        self.assertEqual(p.returncode, 0)
        self.assertEqual(len(i), 2)

        self.assertEqual(i[0]['name'], 'eth0')
        self.assertEqual(i[0]['link_encap'], 'Ethernet')
        self.assertEqual(i[0]['hardware_address'], '00:27:22:4D:7C:55')
        self.assertEqual(i[0]['mtu'], '1500')
        self.assertEqual(i[0]['metric'], '1')
        self.assertEqual(i[0]['rx_packets'], '81885479')
        self.assertEqual(i[0]['tx_packets'], '35544276')
        self.assertEqual(i[0]['collisions'], '0')
        self.assertEqual(i[0]['txqueuelen'], '1000')
        self.assertEqual(i[0]['rx_bytes'], '1559559756')
        self.assertEqual(i[0]['tx_bytes'], '2237569800')

        self.assertEqual(i[1]['name'], 'lo')
        self.assertEqual(i[1]['link_encap'], 'Local Loopback')
        self.assertEqual(i[1]['inet'], '127.0.0.1')
        self.assertEqual(i[1]['mask'], '255.0.0.0')
        self.assertEqual(i[1]['inet6'], '')
        self.assertEqual(i[1]['mtu'], '16436')
        self.assertEqual(i[1]['metric'], '1')
        self.assertEqual(i[1]['rx_packets'], '0')
        self.assertEqual(i[1]['tx_packets'], '0')
        self.assertEqual(i[1]['collisions'], '0')
        self.assertEqual(i[1]['txqueuelen'], '0')
        self.assertEqual(i[1]['rx_bytes'], '0')
        self.assertEqual(i[1]['tx_bytes'], '0')

    def test_ifconfig_value_netjson(self):
        value = """eth0      Link encap:Ethernet  HWaddr 00:26:b9:20:5f:09
          inet addr:193.206.99.183  Bcast:193.206.99.255  Mask:255.255.255.128
          inet6 addr: 2a01:4f8:150:8ffc::214/64 Scope:Global
          inet6 addr: fe80::226:b9ff:fe20:5f09/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:8350427 errors:0 dropped:0 overruns:0 frame:0
          TX packets:5746099 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000
          RX bytes:1025704661 (1.0 GB)  TX bytes:12316739027 (12.3 GB)

lo        Link encap:Local Loopback
          inet addr:127.0.0.1  Mask:255.0.0.0
          inet6 addr: ::1/128 Scope:Host
          UP LOOPBACK RUNNING  MTU:65536  Metric:1
          RX packets:10077 errors:0 dropped:0 overruns:0 frame:0
          TX packets:10077 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:2589263 (2.5 MB)  TX bytes:2589263 (2.5 MB)"""

        p = sub.Popen(['netengine-utils', 'ifconfig', '--netjson', '--value', value], stdout=sub.PIPE, stderr=sub.PIPE)
        i = json.loads(p.communicate()[0])
        # ensure exit code is ok
        self.assertEqual(p.returncode, 0)
        self.assertEqual(len(i), 2)

        self.assertEqual(i[0]['name'], 'eth0')
        self.assertEqual(i[0]['mac'], '00:26:b9:20:5f:09')
        self.assertEqual(i[0]['mtu'], '1500')
        self.assertEqual(i[0]['ip'][0]['address'], '193.206.99.183/25')
        self.assertEqual(i[0]['ip'][1]['address'], '2a01:4f8:150:8ffc::214/64')
        self.assertEqual(i[0]['ip'][2]['address'], 'fe80::226:b9ff:fe20:5f09/64')

        self.assertEqual(i[1]['name'], 'lo')
        self.assertNotIn('mac', i[1])
        self.assertEqual(i[1]['mtu'], '65536')
        self.assertEqual(i[1]['ip'][0]['address'], '127.0.0.1/8')
        self.assertEqual(i[1]['ip'][1]['address'], '::1/128')


class TestNetengineUtilsIwConfig(unittest.TestCase):

    def test_iwconfig(self):
        p = sub.Popen(['netengine-utils', 'iwconfig'], stdout=sub.PIPE, stderr=sub.PIPE)
        i = json.loads(p.communicate()[0])
        # ensure exit code is ok
        self.assertEqual(p.returncode, 0)
        self.assertEqual(type(i), list)

    def test_iwconfig_netjson(self):
        p = sub.Popen(['netengine-utils', 'iwconfig', '--netjson'], stdout=sub.PIPE, stderr=sub.PIPE)
        i = json.loads(p.communicate()[0])
        # ensure exit code is ok
        self.assertEqual(p.returncode, 0)
        self.assertEqual(type(i), list)

    def test_iwconfig_value(self):
        value = """wlan0     IEEE 802.11abgn  ESSID:"eduroam"
          Mode:Managed  Frequency:2.442 GHz  Access Point: DE:9F:DB:27:77:93
          Bit Rate=1 Mb/s   Tx-Power=16 dBm
          Retry  long limit:7   RTS thr:off   Fragment thr:off
          Power Management:off
          Link Quality=48/70  Signal level=-62 dBm
          Rx invalid nwid:0  Rx invalid crypt:0  Rx invalid frag:0
          Tx excessive retries:0  Invalid misc:4459   Missed beacon:0"""

        p = sub.Popen(['netengine-utils', 'iwconfig', '--value', value], stdout=sub.PIPE, stderr=sub.PIPE)
        i = json.loads(p.communicate()[0])
        # ensure exit code is ok
        self.assertEqual(p.returncode, 0)
        self.assertEqual(len(i), 1)

        self.assertEqual(i[0]['name'], 'wlan0')
        self.assertEqual(i[0]['ieee'], '802.11abgn')
        self.assertEqual(i[0]['essid'], 'eduroam')
        self.assertEqual(i[0]['mode'], 'Managed')
        self.assertEqual(i[0]['frequency'], '2.442 GHz')
        self.assertEqual(i[0]['access_point'], 'DE:9F:DB:27:77:93')

    def test_iwconfig_value_netjson(self):
        value = """wlan0     IEEE 802.11abgn  ESSID:"eduroam"
          Mode:Managed  Frequency:2.442 GHz  Access Point: DE:9F:DB:27:77:93
          Bit Rate=1 Mb/s   Tx-Power=16 dBm
          Retry  long limit:7   RTS thr:off   Fragment thr:off
          Power Management:off
          Link Quality=48/70  Signal level=-62 dBm
          Rx invalid nwid:0  Rx invalid crypt:0  Rx invalid frag:0
          Tx excessive retries:0  Invalid misc:4459   Missed beacon:0"""

        p = sub.Popen(['netengine-utils', 'iwconfig', '--netjson', '--value', value], stdout=sub.PIPE, stderr=sub.PIPE)
        i = json.loads(p.communicate()[0])
        # ensure exit code is ok
        self.assertEqual(p.returncode, 0)
        self.assertEqual(len(i), 1)
        self.assertEqual(i[0]['name'], 'wlan0')
        self.assertEqual(i[0]['mac'], 'DE:9F:DB:27:77:93')
        self.assertIn('wireless', i[0])


class TestNetengineUtilsManufacturerLookup(unittest.TestCase):

    def test_manufacturer_lookup(self):
        values = [
            '24:a4:3c:aa:bb:cc',
            '24-A4-3C-AA-BB-CC',
            '24A43CAABBCC',
            '24A43c'
        ]
        for value in values:
            p = sub.Popen(['netengine-utils', 'manufacturer_lookup', '--value', value], stdout=sub.PIPE, stderr=sub.PIPE)
            self.assertEqual(p.communicate()[0].strip(), 'Ubiquiti Networks, INC')
            # ensure exit code is ok
            self.assertEqual(p.returncode, 0)

    def test_manufacturer_lookup_missing_value(self):
        p = sub.Popen(['netengine-utils', 'manufacturer_lookup'], stdout=sub.PIPE, stderr=sub.PIPE)
        self.assertIn('you must supply', p.communicate()[0])
        # ensure exit code is not ok
        self.assertEqual(p.returncode, 1)

    def test_manufacturer_lookup_no_valid_manufacturer(self):
        p = sub.Popen(['netengine-utils', 'manufacturer_lookup', '--value', 'ab:ab:ab:ab:ab:ab'], stdout=sub.PIPE, stderr=sub.PIPE)
        self.assertIn('No valid manufacturer', p.communicate()[0])
        # ensure exit code is not ok
        self.assertEqual(p.returncode, 1)
