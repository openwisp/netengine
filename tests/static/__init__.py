import json
import mock
import os

from ..settings import settings


class MockOutputMixin(object):

    class DisableMockMixin(object):
        """
        Disables the mock object in context managers restoring the mocked
        function to its original state
        """
        def assert_called(self, *args, **kwargs):
            pass

        def assert_not_called(self, *args, **kwargs):
            pass

        def assert_called_once(self, *args, **kwargs):
            pass

        def assert_called_with(self, *args, **kwargs):
            pass

        def assert_called_once_with(self, *args, **kwargs):
            pass

        def assert_has_calls(self, *args, **kwargs):
            pass

        def assert_any_call(self, *args, **kwargs):
            pass

        def start(self):
            pass

        def stop(self):
            pass

        def __enter__(self, *args, **kwargs):
            return self

        def __exit__(self, *args, **kwargs):
            return True


    def _patch(self, *args, **kwargs):
        if settings['disable_mocks']:
            return self.DisableMockMixin()
        else:
            return mock.patch(*args, **kwargs)

    @staticmethod
    def _load_mock_json(file):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        with open(base_dir + file) as f:
            data = json.load(f)
        return data

    @staticmethod
    def _get_mocked_value(oid, data, *args, **kwargs):
        result = data[oid]
        if type(result) == list:
            result = "\n".join(result[0:])
        return result

    @staticmethod
    def _get_encoded_mocked_value(oid, data, *args, **kwargs):
        result = data[oid]
        if type(result) == list:
            result = "\n".join(result[0:])
        return [0, 0, 0, [[0, result.encode('ascii', 'ignore')], 0]]

    @staticmethod
    def _get_mocked_wireless_links(oid):
        return_data = {
            '1.3.6.1.4.1.14988.1.1.1.2.1': [0, 0, 0, [[[0, 0], 0]] * 28],
            '1.3.6.1.4.1.14988.1.1.1.2.1.3': [0, 0, 0, [0, 0]],
            '1.3.6.1.4.1.14988.1.1.1.2.1.3.0': [None, 0, 0, []],
        }
        return return_data[oid]
