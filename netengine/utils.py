import sys
import re
import json

# ------- IFCONFIG TO JSON CONVERSION ------- #
# credits:
# https://gist.github.com/snbartell/1586034

def _extract(ifconfig_output):
    mo = re.search(r'^(?P<interface>\w+|\w+:\d+)\s+' +
                   r'Link encap:(?P<link_encap>\S+)\s+' +
                   r'(HWaddr\s+(?P<hardware_address>\S+))?' +
                   r'(\s+inet addr:(?P<ip_address>\S+))?' +
                   r'(\s+inet6 addr: (?P<ipv6_address_global>\S+)\s+Scope:Global)?' +
                   r'(\s+Bcast:(?P<broadcast_address>\S+)\s+)?' +
                   r'(Mask:(?P<net_mask>\S+)\s+)?'+
                   r'(inet6 addr: (?P<ipv6_address_link>\S+)\s+Scope:Link)?' +
                   r'((\s|\w)+MTU:(?P<mtu>\S+)\s+)?'+
                   r'(Metric:(?P<metric>\S+)\s+)?'+
                   r'(RX packets:(?P<rx_packets>\S+)\s+errors:\d+ dropped:\d+ overruns:\d+ frame:\d+\s+)?'+
                   r'(TX packets:(?P<tx_packets>\S+)\s+errors:\d+ dropped:\d+ overruns:\d+ carrier:\d+\s+)?'+
                   r'(collisions:(?P<collisions>\S+)\s+)?'+
                   r'(txqueuelen:(?P<txqueuelen>\S+)\s+)?'+
                   r'(RX bytes:(?P<rx_bytes>\S+)\s+\((\d|\s|\.|\w)+\)\s+)?'+
                   r'(TX bytes:(?P<tx_bytes>\S+)\s+\((\d|\s|\.|\w)+\)?)?',
                   
                     ifconfig_output, re.MULTILINE|re.IGNORECASE )
    if mo:
        return mo.groupdict('')
    return {}
 

def ifconfig_to_python(ifconfig):
    interfaces = [ _extract(interface) for interface in ifconfig.split('\n\n') if interface.strip() ]
    return interfaces

def ifconfig_to_json(ifconfig, indent=4):
    interfaces = ifconfig_to_dict(ifconfig)
    return json.dumps(interfaces, indent=indent)
