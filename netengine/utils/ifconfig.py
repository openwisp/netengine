import re
import json
import ipaddress
from collections import OrderedDict


class IfConfig(object):
    """ ifconfig parser class """

    def __init__(self, output):
        """
        :param output: ifconfig text output
        """
        self.interfaces = []
        # loop over blocks
        for block in output.split('\n\n'):
            if block.strip():
                self.interfaces.append(self._parse_block(block))

    def _parse_block(self, output):
        """
        Parses an ifconfig block
        """
        mo = re.search(
            r'^(?P<name>\S+)\s+' +
            r'Link encap:(?P<link_encap>\S+(\s\S+)?)' +
            r'(\s+HWaddr\s+(?P<hardware_address>\S+))?' +
            r'(\s+inet addr:(?P<inet>\S+))?' +
            r'(\s+Bcast:(?P<broadcast>\S+))?' +
            r'(\s+Mask:(?P<mask>\S+))?'+
            r'(\s+inet6 addr: (?P<inet6>\S+)\s+Scope:(Global|Host))?' +
            r'(\s+inet6 addr: (?P<inet6_local>\S+)\s+Scope:Link)?' +
            r'((\s|\w)+MTU:(?P<mtu>\S+))?'+
            r'(\s+Metric:(?P<metric>\S+))?'+
            r'(\s+RX packets:(?P<rx_packets>\S+)\s+errors:\d+ dropped:\d+ overruns:\d+ frame:\d+)?'+
            r'(\s+TX packets:(?P<tx_packets>\S+)\s+errors:\d+ dropped:\d+ overruns:\d+ carrier:\d+)?'+
            r'(\s+collisions:(?P<collisions>\S+))?'+
            r'(\s+txqueuelen:(?P<txqueuelen>\S+))?'+
            r'(\s+RX bytes:(?P<rx_bytes>\S+)\s+\((\d|\s|\.|\w)+\))?'+
            r'(\s+TX bytes:(?P<tx_bytes>\S+)\s+\((\d|\s|\.|\w)+\)?)?',
            output, re.MULTILINE|re.IGNORECASE
        )
        if mo:
            d = mo.groupdict('')
            result = OrderedDict()
            for key in ['name',
                        'link_encap',
                        'hardware_address',
                        'inet',
                        'broadcast',
                        'mask',
                        'inet6',
                        'inet6_local',
                        'mtu',
                        'metric',
                        'rx_packets',
                        'tx_packets',
                        'collisions',
                        'txqueuelen',
                        'rx_bytes',
                        'tx_bytes']:
                if key in d:
                    result[key] = d[key]
            return result
        else:
            return {}

    def to_python(self):
        """ returns python dictionary representation of ifconfig output """
        return self.interfaces

    def to_json(self, **kwargs):
        """ returns json representation of ifconfig output """
        return json.dumps(self.interfaces, **kwargs)

    def to_netjson(self, python=False, **kwargs):
        """ convert to netjson format """
        result = []
        for i in self.interfaces:
            netjson = OrderedDict((
                ('name', i['name']),
                ('mac', i['hardware_address']),
                ('mtu', i['mtu']),
                ('ip', [])
            ))
            if not netjson['mac']:
                del netjson['mac']
            # add ipv4
            if i['inet'] and i['mask']:
                netjson['ip'].append({
                    # creates an ipv4_interface object correctly
                    'address': str(ipaddress.ip_interface(u'%(inet)s/%(mask)s' % i))
                })
            # add ipv6
            for ip in [i['inet6'], i['inet6_local']]:
                if ip:
                    netjson['ip'].append({
                        'address': ip
                    })
            result.append(netjson)
        # can return both python and json
        if python:
            return result
        else:
            return json.dumps(result, **kwargs)
