import unittest

from netengine.backends.http import HTTP
from netengine.exceptions import NetEngineError

from ..settings import settings


__all__ = ['TestHTTP']


class TestHTTP(unittest.TestCase):

    def setUp(self):
        self.host = settings['base-http']['host']
        self.username = settings['base-http']['username']
        self.password = settings['base-http']['password']
        self.device = HTTP(self.host, self.username, self.password)
        self.assertTrue(self.device.__netengine__)
