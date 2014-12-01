import unittest
import json

from netengine.shortcuts import OrderedDict
from netengine.utils.ifconfig import IfConfig


__all__ = ['TestIfConfigParser']


class TestIfConfigParser(unittest.TestCase):
    def test_ubuntu_13_simple(self):
        output = """eth0      Link encap:Ethernet  HWaddr 00:26:b9:20:5f:09
          inet addr:193.206.99.183  Bcast:193.206.99.255  Mask:255.255.255.128
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
          RX bytes:2589263 (2.5 MB)  TX bytes:2589263 (2.5 MB)

wlan0     Link encap:Ethernet  HWaddr 00:16:44:60:32:d2
          inet addr:172.19.184.164  Bcast:172.19.255.255  Mask:255.255.0.0
          inet6 addr: fe80::216:44ff:fe60:32d2/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:148496 errors:0 dropped:0 overruns:0 frame:0
          TX packets:972 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000
          RX bytes:18964958 (18.9 MB)  TX bytes:147671 (147.6 KB)"""

        i = IfConfig(output).to_python()
        eth = i[0]
        lo = i[1]
        wlan = i[2]

        self.assertTrue(type(eth) is OrderedDict)
        self.assertEqual(eth['name'], 'eth0')
        self.assertEqual(eth['link_encap'], 'Ethernet')
        self.assertEqual(eth['hardware_address'], '00:26:b9:20:5f:09')
        self.assertEqual(eth['inet'], '193.206.99.183')
        self.assertEqual(eth['broadcast'], '193.206.99.255')
        self.assertEqual(eth['mask'], '255.255.255.128')
        self.assertEqual(eth['inet6'], '')
        self.assertEqual(eth['inet6_local'], 'fe80::226:b9ff:fe20:5f09/64')
        self.assertEqual(eth['mtu'], '1500')
        self.assertEqual(eth['metric'], '1')
        self.assertEqual(eth['rx_packets'], '8350427')
        self.assertEqual(eth['tx_packets'], '5746099')
        self.assertEqual(eth['collisions'], '0')
        self.assertEqual(eth['txqueuelen'], '1000')
        self.assertEqual(eth['rx_bytes'], '1025704661')
        self.assertEqual(eth['tx_bytes'], '12316739027')

        self.assertTrue(type(lo) is OrderedDict)
        self.assertEqual(lo['name'], 'lo')
        self.assertEqual(lo['link_encap'], 'Local Loopback')
        self.assertEqual(lo['inet'], '127.0.0.1')
        self.assertEqual(lo['mask'], '255.0.0.0')
        self.assertEqual(lo['inet6'], '::1/128')
        self.assertEqual(lo['mtu'], '65536')
        self.assertEqual(lo['metric'], '1')
        self.assertEqual(lo['rx_packets'], '10077')
        self.assertEqual(lo['tx_packets'], '10077')
        self.assertEqual(lo['collisions'], '0')
        self.assertEqual(lo['txqueuelen'], '0')
        self.assertEqual(lo['rx_bytes'], '2589263')
        self.assertEqual(lo['tx_bytes'], '2589263')

        self.assertTrue(type(wlan) is OrderedDict)
        self.assertEqual(wlan['name'], 'wlan0')
        self.assertEqual(wlan['link_encap'], 'Ethernet')
        self.assertEqual(wlan['hardware_address'], '00:16:44:60:32:d2')
        self.assertEqual(wlan['inet'], '172.19.184.164')
        self.assertEqual(wlan['broadcast'], '172.19.255.255')
        self.assertEqual(wlan['mask'], '255.255.0.0')
        self.assertEqual(wlan['inet6'], '')
        self.assertEqual(wlan['inet6_local'], 'fe80::216:44ff:fe60:32d2/64')
        self.assertEqual(wlan['mtu'], '1500')
        self.assertEqual(wlan['metric'], '1')
        self.assertEqual(wlan['rx_packets'], '148496')
        self.assertEqual(wlan['tx_packets'], '972')
        self.assertEqual(wlan['collisions'], '0')
        self.assertEqual(wlan['txqueuelen'], '1000')
        self.assertEqual(wlan['rx_bytes'], '18964958')
        self.assertEqual(wlan['tx_bytes'], '147671')

    def test_to_json(self):
        output = """eth0      Link encap:Ethernet  HWaddr 00:26:b9:20:5f:09
          inet addr:193.206.99.183  Bcast:193.206.99.255  Mask:255.255.255.128
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
          RX bytes:2589263 (2.5 MB)  TX bytes:2589263 (2.5 MB)

wlan0     Link encap:Ethernet  HWaddr 00:16:44:60:32:d2
          inet addr:172.19.184.164  Bcast:172.19.255.255  Mask:255.255.0.0
          inet6 addr: fe80::216:44ff:fe60:32d2/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:148496 errors:0 dropped:0 overruns:0 frame:0
          TX packets:972 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000
          RX bytes:18964958 (18.9 MB)  TX bytes:147671 (147.6 KB)"""

        json_output = IfConfig(output).to_json()
        i = json.loads(json_output)
        self.assertEqual(len(i), 3)
        eth = i[0]
        lo = i[1]
        wlan = i[2]

        self.assertEqual(eth['name'], 'eth0')
        self.assertEqual(eth['link_encap'], 'Ethernet')
        self.assertEqual(eth['hardware_address'], '00:26:b9:20:5f:09')
        self.assertEqual(eth['inet'], '193.206.99.183')
        self.assertEqual(eth['broadcast'], '193.206.99.255')
        self.assertEqual(eth['mask'], '255.255.255.128')
        self.assertEqual(eth['inet6'], '')
        self.assertEqual(eth['inet6_local'], 'fe80::226:b9ff:fe20:5f09/64')
        self.assertEqual(eth['mtu'], '1500')
        self.assertEqual(eth['metric'], '1')
        self.assertEqual(eth['rx_packets'], '8350427')
        self.assertEqual(eth['tx_packets'], '5746099')
        self.assertEqual(eth['collisions'], '0')
        self.assertEqual(eth['txqueuelen'], '1000')
        self.assertEqual(eth['rx_bytes'], '1025704661')
        self.assertEqual(eth['tx_bytes'], '12316739027')

        self.assertEqual(lo['name'], 'lo')
        self.assertEqual(lo['link_encap'], 'Local Loopback')
        self.assertEqual(lo['inet'], '127.0.0.1')
        self.assertEqual(lo['mask'], '255.0.0.0')
        self.assertEqual(lo['inet6'], '::1/128')
        self.assertEqual(lo['mtu'], '65536')
        self.assertEqual(lo['metric'], '1')
        self.assertEqual(lo['rx_packets'], '10077')
        self.assertEqual(lo['tx_packets'], '10077')
        self.assertEqual(lo['collisions'], '0')
        self.assertEqual(lo['txqueuelen'], '0')
        self.assertEqual(lo['rx_bytes'], '2589263')
        self.assertEqual(lo['tx_bytes'], '2589263')

        self.assertEqual(wlan['name'], 'wlan0')
        self.assertEqual(wlan['link_encap'], 'Ethernet')
        self.assertEqual(wlan['hardware_address'], '00:16:44:60:32:d2')
        self.assertEqual(wlan['inet'], '172.19.184.164')
        self.assertEqual(wlan['broadcast'], '172.19.255.255')
        self.assertEqual(wlan['mask'], '255.255.0.0')
        self.assertEqual(wlan['inet6'], '')
        self.assertEqual(wlan['inet6_local'], 'fe80::216:44ff:fe60:32d2/64')
        self.assertEqual(wlan['mtu'], '1500')
        self.assertEqual(wlan['metric'], '1')
        self.assertEqual(wlan['rx_packets'], '148496')
        self.assertEqual(wlan['tx_packets'], '972')
        self.assertEqual(wlan['collisions'], '0')
        self.assertEqual(wlan['txqueuelen'], '1000')
        self.assertEqual(wlan['rx_bytes'], '18964958')
        self.assertEqual(wlan['tx_bytes'], '147671')

    def test_simple_output_linux_openwrt_backfire(self):
        output = """eth0      Link encap:Ethernet  HWaddr 00:27:22:4D:7C:55
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

        i = IfConfig(output).to_python()
        eth = i[0]
        lo = i[1]

        self.assertEqual(eth['name'], 'eth0')
        self.assertEqual(eth['link_encap'], 'Ethernet')
        self.assertEqual(eth['hardware_address'], '00:27:22:4D:7C:55')
        self.assertEqual(eth['mtu'], '1500')
        self.assertEqual(eth['metric'], '1')
        self.assertEqual(eth['rx_packets'], '81885479')
        self.assertEqual(eth['tx_packets'], '35544276')
        self.assertEqual(eth['collisions'], '0')
        self.assertEqual(eth['txqueuelen'], '1000')
        self.assertEqual(eth['rx_bytes'], '1559559756')
        self.assertEqual(eth['tx_bytes'], '2237569800')

        self.assertEqual(lo['name'], 'lo')
        self.assertEqual(lo['link_encap'], 'Local Loopback')
        self.assertEqual(lo['inet'], '127.0.0.1')
        self.assertEqual(lo['mask'], '255.0.0.0')
        self.assertEqual(lo['inet6'], '')
        self.assertEqual(lo['mtu'], '16436')
        self.assertEqual(lo['metric'], '1')
        self.assertEqual(lo['rx_packets'], '0')
        self.assertEqual(lo['tx_packets'], '0')
        self.assertEqual(lo['collisions'], '0')
        self.assertEqual(lo['txqueuelen'], '0')
        self.assertEqual(lo['rx_bytes'], '0')
        self.assertEqual(lo['tx_bytes'], '0')

    def test_ipv6_global(self):
        output = """eth0      Link encap:Ethernet  HWaddr 52:54:00:56:46:d0
          inet addr:176.9.211.214  Bcast:10.177.8.255  Mask:255.255.255.240
          inet6 addr: 2a01:4f8:150:8ffc::214/64 Scope:Global
          inet6 addr: fe80::5054:ff:fe56:46d0/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:1320428 errors:0 dropped:0 overruns:0 frame:0
          TX packets:1170003 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000
          RX bytes:137665653 (137.6 MB)  TX bytes:2092947843 (2.0 GB)"""

        i = IfConfig(output).to_python()
        eth = i[0]

        self.assertEqual(eth['name'], 'eth0')
        self.assertEqual(eth['link_encap'], 'Ethernet')
        self.assertEqual(eth['hardware_address'], '52:54:00:56:46:d0')
        self.assertEqual(eth['inet'], '176.9.211.214')
        self.assertEqual(eth['broadcast'], '10.177.8.255')
        self.assertEqual(eth['mask'], '255.255.255.240')
        self.assertEqual(eth['inet6'], '2a01:4f8:150:8ffc::214/64')
        self.assertEqual(eth['inet6_local'], 'fe80::5054:ff:fe56:46d0/64')
        self.assertEqual(eth['mtu'], '1500')
        self.assertEqual(eth['metric'], '1')
        self.assertEqual(eth['rx_packets'], '1320428')
        self.assertEqual(eth['tx_packets'], '1170003')
        self.assertEqual(eth['collisions'], '0')
        self.assertEqual(eth['txqueuelen'], '1000')
        self.assertEqual(eth['rx_bytes'], '137665653')
        self.assertEqual(eth['tx_bytes'], '2092947843')

    def test_netjson(self):
        output = """eth0      Link encap:Ethernet  HWaddr 00:26:b9:20:5f:09
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

        i = IfConfig(output).to_netjson(python=True)
        eth = i[0]
        lo = i[1]

        self.assertEqual(eth['name'], 'eth0')
        self.assertEqual(eth['mac'], '00:26:b9:20:5f:09')
        self.assertEqual(eth['mtu'], '1500')
        self.assertEqual(eth['ip'][0]['address'], '193.206.99.183/25')
        self.assertEqual(eth['ip'][1]['address'], '2a01:4f8:150:8ffc::214/64')
        self.assertEqual(eth['ip'][2]['address'], 'fe80::226:b9ff:fe20:5f09/64')

        self.assertEqual(lo['name'], 'lo')
        self.assertNotIn('mac', lo)
        self.assertEqual(lo['mtu'], '65536')
        self.assertEqual(lo['ip'][0]['address'], '127.0.0.1/8')
        self.assertEqual(lo['ip'][1]['address'], '::1/128')

        string = IfConfig(output).to_netjson(sort_keys=True)
        i = json.loads(string)

        eth = i[0]
        lo = i[1]

        self.assertEqual(eth['name'], 'eth0')
        self.assertEqual(lo['name'], 'lo')

    def test_netjson_airos_output(self):
        output = """ath0      Link encap:Ethernet  HWaddr 00:27:22:16:8B:12
          inet6 addr: fe80::227:22ff:fe16:8b12/64 Scope:Link
          UP BROADCAST RUNNING PROMISC ALLMULTI MULTICAST  MTU:1500  Metric:1
          RX packets:453289433 errors:6 dropped:0 overruns:0 frame:0
          TX packets:425102013 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:3089770133 (2.8 GiB)  TX bytes:1082993376 (1.0 GiB)

br0       Link encap:Ethernet  HWaddr 00:27:22:16:8B:12
          inet6 addr: fe80::227:22ff:fe16:8b12/64 Scope:Link
          UP BROADCAST RUNNING ALLMULTI MULTICAST  MTU:1500  Metric:1
          RX packets:166848958 errors:0 dropped:0 overruns:0 frame:0
          TX packets:6 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:4287619683 (3.9 GiB)  TX bytes:468 (468.0 B)

eth0      Link encap:Ethernet  HWaddr 00:27:22:17:8B:12
          inet addr:10.40.0.130  Bcast:10.40.0.255  Mask:255.255.255.128
          inet6 addr: fe80::227:22ff:fe17:8b12/64 Scope:Link
          UP BROADCAST RUNNING ALLMULTI MULTICAST  MTU:1500  Metric:1
          RX packets:572607903 errors:0 dropped:0 overruns:0 frame:0
          TX packets:478274409 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000
          RX bytes:1313195648 (1.2 GiB)  TX bytes:940262910 (896.7 MiB)

eth0.24   Link encap:Ethernet  HWaddr 00:27:22:17:8B:12
          inet6 addr: fe80::227:22ff:fe17:8b12/64 Scope:Link
          UP BROADCAST RUNNING PROMISC ALLMULTI MULTICAST  MTU:1500  Metric:1
          RX packets:425090150 errors:0 dropped:0 overruns:0 frame:0
          TX packets:453289608 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:1126617830 (1.0 GiB)  TX bytes:607963875 (579.7 MiB)

lo        Link encap:Local Loopback
          inet addr:127.0.0.1  Mask:255.0.0.0
          UP LOOPBACK RUNNING  MTU:16436  Metric:1
          RX packets:26 errors:0 dropped:0 overruns:0 frame:0
          TX packets:26 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:2276 (2.2 KiB)  TX bytes:2276 (2.2 KiB)

wifi0     Link encap:Ethernet  HWaddr 00:27:22:16:8B:12
          UP BROADCAST RUNNING PROMISC ALLMULTI MULTICAST  MTU:2286  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:0 errors:23129 dropped:299 overruns:0 carrier:0
          collisions:0 txqueuelen:2000
          RX bytes:0 (0.0 B)  TX bytes:0 (0.0 B)
          Interrupt:48 Memory:b0000000-b0010000"""

        i = IfConfig(output).to_netjson(python=True)
        self.assertTrue(type(i[0]) is OrderedDict)
        self.assertEqual(len(i), 6)
        eth24 = i[3]
        self.assertEqual(eth24['name'], 'eth0.24')

        i = json.loads(IfConfig(output).to_netjson())
        self.assertEqual(len(i), 6)
        eth24 = i[3]
        self.assertEqual(eth24['name'], 'eth0.24')
