import unittest
from netengine.ssh.ssh import SSH

from .settings import settings

class TestSSH(unittest.TestCase):

    def setUp(self):
        self.host = settings['base-ssh']['host']
        self.username = settings['base-ssh']['username']
        self.password = settings['base-ssh']['password']
        
        self.device = SSH(self.host, self.username, self.password)
        self.device.connect()
    
    def test_wrong_connection(self):
        wrong = SSH('10.40.0.254', 'root', 'pwd')
        self.assertRaises(Exception, wrong.connect)
        
    def test_olsr_installed(self):
        self.device.olsr_installed()


if __name__ == '__main__':
    unittest.main()