import re
import json
from collections import OrderedDict


class IwConfig(object):
    """ iwconfig parser class """

    MODE_MAP = {
        'Master': 'ap',
        'Managed': 'sta',
        'Ad-Hoc': 'adhoc',
        'Repeater': 'wds',
        'Secondary': 'wds',
        'Monitor': 'mon',
        'Auto': 'auto'
    }

    def __init__(self, output):
        """
        :param output: iwconfig text output
        """
        self.interfaces = []
        # loop over blocks
        for block in output.split('\n\n'):
            if 'no wireless extension' not in block.strip():
                self.interfaces.append(self._parse_block(block))

    def _parse_block(self, output):
        result = OrderedDict()
        lines = output.split('\n')
        # first line is special, split it in parts,
        # use double whitespace as delimeter
        # strip extra whitespace at beginning and end, discard empty strings
        first_line_parts = [part.strip() for part in lines[0].split('  ') if part.strip()]
        result['name'] = first_line_parts[0]
        result['ieee'] = first_line_parts[1].replace('IEEE ', '')
        result['essid'] = first_line_parts[2].replace('ESSID:', '').replace('"', '')
        # treat subsequent lines consistently
        for line in lines[1:]:
            # split groups divided by spaces
            groups = [part.strip() for part in line.split('  ') if part.strip()]
            # loop over groups
            for group in groups:
                # split keys & values (use = or : as delimeter)
                key, value = re.split('=|:', group, 1)
                # lowercase keys with underscore in place of spaces or dashes
                key = key.lower().replace(' ', '_').replace('-', '_')
                result[key] = value.strip()
        return result

    def to_python(self):
        """ returns python dictionary representation of iwconfig output """
        return self.interfaces

    def to_json(self, **kwargs):
        """ returns json representation of ifconfig output """
        return json.dumps(self.interfaces, **kwargs)

    def to_netjson(self, python=False, **kwargs):
        """ convert to netjson format """
        result = []
        for i in self.interfaces:
            wireless = OrderedDict((
                ('bitrate', i.get('bit_rate')),
                ('standard', i.get('ieee')),
                ('essid', i.get('essid')),
                ('mode', self.MODE_MAP.get(i['mode'])),
                ('rts_threshold', i.get('rts_thr')),
                ('frag_threshold', i.get('fragment_thr'))
            ))
            if 'encryption_key' in i:
                wireless['encryption'] = i['encryption_key'] != 'off'

            result.append(OrderedDict((
                ('name', i['name']),
                ('mac', i['access_point']),
                ('wireless', wireless)
            )))
        # can return both python and json
        if python:
            return result
        else:
            return json.dumps(result, **kwargs)
