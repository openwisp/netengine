import codecs
import json
import os
from unittest import mock

from .settings import settings


class SpyMock:
    @staticmethod
    def _patch(*args, **kwargs):
        if not settings['disable_mocks']:
            return mock.patch.object(*args, **kwargs)
        wraps = getattr(kwargs['wrap_obj'], kwargs['attribute'])
        return mock.patch.object(kwargs['target'], kwargs['attribute'], wraps=wraps)

    @staticmethod
    def _update_patch(mock_obj, *args, **kwargs):
        if settings['disable_mocks']:
            return
        mock_obj.__dict__.update(*args, **kwargs)


class MockOutputMixin(object):
    @staticmethod
    def _load_mock_json(file):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        with open(base_dir + file) as f:
            data = json.load(f)
        return data

    @staticmethod
    def _get_mocked_getcmd(data, input):
        oid = input[2]
        result = data[oid]
        if type(result) == dict:
            _type = result['type']
            _value = result['value']
            if _type == 'bytes':
                result = codecs.escape_decode(_value)[0]
        elif type(result) == list:
            result = '\n'.join(result[0:])
        return [0, 0, 0, [[0, result]]]

    @staticmethod
    def _get_mocked_wireless_links(data):
        oid = data[2]
        return_data = {
            '1.3.6.1.4.1.14988.1.1.1.2.1': [0, 0, 0, [[[0, 0], 0]] * 28],
            '1.3.6.1.4.1.14988.1.1.1.2.1.3': [0, 0, 0, [0, 0]],
            '1.3.6.1.4.1.14988.1.1.1.2.1.3.0': [None, 0, 0, []],
            '1.3.6.1.2.1.1.9.1.1': [
                0,
                0,
                0,
                [[[0, 1]], [[0, 2]], [[0, 3]], [[0, 4]], [[0, 5]]],
            ],
        }
        return return_data[oid]
