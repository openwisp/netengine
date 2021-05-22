import unittest

from netengine.backends.http import HTTP
from netengine.exceptions import NetEngineError


__all__ = ['TestHTTP']


class TestHTTP(unittest.TestCase):

    def setUp(self):
        self.device = HTTP('test-host.com', 'test-user', 'test-password')
        self.assertTrue(self.device.__netengine__)
