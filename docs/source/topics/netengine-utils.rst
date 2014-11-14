************************************
netengine-utils command line utility
************************************

**netengine-utils** is a shell utility that provides bindings to some features of
``netengine.utils``:

 * ``netengine.utils.ifconfig``
 * ``netengine.utils.iwfconfig``
 * ``netengine.utils.manufacturer_lookup``

This utility can be called from the interactive linux shell, bash scripts or from
software written in a different language than python.

Convert local ifconfig output to JSON
=====================================

Convert the **ifconfig** output of the local machine to JSON format::

    netengine-utils ifconfig

Example output::

    [
        {
            "name": "eth0",
            "link_encap": "Ethernet",
            "hardware_address": "00:26:b9:20:5f:09",
            "inet": "193.206.99.183",
            "broadcast": "193.206.99.255",
            "mask": "255.255.255.128",
            "inet6": "",
            "inet6_local": "fe80::226:b9ff:fe20:5f09/64",
            "mtu": "1500",
            "metric": "1",
            "rx_packets": "18237538",
            "tx_packets": "12674692",
            "collisions": "0",
            "txqueuelen": "1000",
            "rx_bytes": "2297452870",
            "tx_bytes": "27474972424"
        },
        {
            "name": "lo",
            "link_encap": "Local Loopback",
            "hardware_address": "",
            "inet": "127.0.0.1",
            "broadcast": "",
            "mask": "255.0.0.0",
            "inet6": "::1/128",
            "inet6_local": "",
            "mtu": "65536",
            "metric": "1",
            "rx_packets": "12025",
            "tx_packets": "12025",
            "collisions": "0",
            "txqueuelen": "0",
            "rx_bytes": "2165364",
            "tx_bytes": "2165364"
        },
        {
            "name": "lxcbr0",
            "link_encap": "Ethernet",
            "hardware_address": "c2:b3:22:60:4d:e4",
            "inet": "10.0.3.1",
            "broadcast": "10.0.3.255",
            "mask": "255.255.255.0",
            "inet6": "",
            "inet6_local": "fe80::c0b3:22ff:fe60:4de4/64",
            "mtu": "1500",
            "metric": "1",
            "rx_packets": "0",
            "tx_packets": "229",
            "collisions": "0",
            "txqueuelen": "0",
            "rx_bytes": "0",
            "tx_bytes": "45639"
        }
    ]

Convert specified ifconfig output to JSON
=========================================

Convert the **ifconfig** output specified with the ``--value`` option to JSON format::

    netengine-utils ifconfig --value "$OUTPUT"

In which ``$OUTPUT`` is a variable containing the ifconfig output you obtained from some remote device.

Ifconfig "netjson" option
=========================

Pass the ``--netjson`` option::

    netengine-utils ifconfig --netjson

And you will get a format similar to the following one::

    [
        {
            "name": "eth0",
            "mac": "00:26:b9:20:5f:09",
            "mtu": "1500",
            "ip": [
                {
                    "address": "193.206.99.183/25"
                },
                {
                    "address": "fe80::226:b9ff:fe20:5f09/64"
                }
            ]
        },
        {
            "name": "lo",
            "mtu": "65536",
            "ip": [
                {
                    "address": "127.0.0.1/8"
                },
                {
                    "address": "::1/128"
                }
            ]
        },
        {
            "name": "lxcbr0",
            "mac": "c2:b3:22:60:4d:e4",
            "mtu": "1500",
            "ip": [
                {
                    "address": "10.0.3.1/24"
                },
                {
                    "address": "fe80::c0b3:22ff:fe60:4de4/64"
                }
            ]
        }
    ]

Convert local iwconfig output to JSON
=====================================

Convert the **iwconfig** output of the local machine to JSON format::

    netengine-utils iwconfig

Example output::

    [
        {
            "name": "wlan0",
            "ieee": "802.11abgn",
            "essid": "off/any",
            "mode": "Managed",
            "access_point": "Not-Associated",
            "tx_power": "off",
            "retry_long_limit": "7",
            "rts_thr": "off",
            "fragment_thr": "off",
            "power_management": "off"
        }
    ]

Convert specified iwconfig output to JSON
=========================================

Convert the **iwconfig** output specified with the ``--value`` option to JSON format::

    netengine-utils iwconfig --value "$OUTPUT"

In which ``$OUTPUT`` is a variable containing the iwconfig output you obtained from some remote device.

Iwconfig "netjson" option
=========================

Pass the ``--netjson`` option::

    netengine-utils iwconfig --netjson

And you will get a format similar to the following one::

    [
        {
            "name": "wlan0",
            "mac": "DC:9F:DB:27:77:80",
            "wireless": {
                "bitrate": "9 Mb/s",
                "standard": "802.11abgn",
                "essid": "provinciawifi",
                "mode": "sta",
                "rts_threshold": "off",
                "frag_threshold": "off"
            }
        }
    ]

Manufacturer Lookup
===================

Use this command to retrieve the manufacturer from a mac address or prefix::

    netengine-utils manufacturer_lookup --value 24:a4:3c:00:11:22

    Ubiquiti Networks, INC

Different formats are allowed::

    netengine-utils manufacturer_lookup --value 24-A4-3C-00-11-22
    netengine-utils manufacturer_lookup --value 24A43C001122
    netengine-utils manufacturer_lookup --value 24-A4-3C
