import unittest
import json
from netengine.backends import Dummy


__all__ = ['TestDummyBackend']


class TestDummyBackend(unittest.TestCase):
    
    def setUp(self):
        self.dummy = Dummy('10.40.0.1')
    
    def test_str(self):
        self.assertIn('Dummy NetEngine', str(self.dummy))
    
    def test_validate(self):
        self.dummy.validate()
    
    def test_to_dict(self):
        self.assertTrue(isinstance(self.dummy.to_dict(), dict))
    
    def test_to_json(self):
        json_string = self.dummy.to_json()
        
        self.assertTrue(isinstance(json_string, basestring))
        
        dictionary = json.loads(json_string)