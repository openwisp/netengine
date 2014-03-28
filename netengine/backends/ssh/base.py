import paramiko
from netengine.backends import BaseBackend
from netengine.exceptions import NetEngineError
from netengine.utils import ifconfig_to_python


__all__ = ['SSH']


class SSH(BaseBackend):
    """
    SSH base backend
    """
    
    def __init__(self, host, username, password, port=22):
        """
        :host string: required
        :username string: required
        :password string: required
        :port integer: defaults to 22
        """
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.shell = None
    
    def __str__(self):
        """ print a human readable object description """
        return "<SSH: %s@%s>" % (self.username, self.host)
    
    def __del__(self):
        """
        when the instance is garbage collected
        ensure SSH connection is closed
        """
        try:
            self.disconnect()
        except AttributeError:
            pass
    
    def validate(self):
        """
        raises NetEngineError exception if anything is wrong with the connection
        for example: wrong host, invalid credentials
        """
        try:
            self.connect()
            self.disconnect()
        except Exception as e:
            raise NetEngineError(e)
    
    def connect(self):
        """
        Initialize SSH session
        
        will raise exception if anything goes wrong
        """
        shell = paramiko.SSHClient()
        shell.load_system_host_keys()
        shell.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        shell.connect(
            self.host,
            username=self.username,
            password=self.password,
            port=self.port
        )
        self.shell = shell
    
    def disconnect(self):
        """ closes SSH connection """
        self.shell.close()
    
    def exec_command(self, command, **kwargs):
        """ alias to paramiko.SSHClient.exec_command """
        # init connection if necessary
        if self.shell is None or self.shell.get_transport() is None:
            self.connect()
        
        return self.shell.exec_command(command, **kwargs)
    
    def run(self, command, **kwargs):
        """
        executes command and returns stdout if success or stderr if error
        """
        stdin, stdout, stderr = self.exec_command(command, **kwargs)
        
        output = stdout.read().strip()
        error = stderr.read().strip()
        
        # if error return error msg
        if error != '':
            return error
        # otherwise return output
        else:
            return output
    
    def get_interfaces(self):
        """ get device interfaces """
        return ifconfig_to_python(self.run('ifconfig'))
    
    def get_ipv6_of_interface(self, interface_name):
        """ return ipv6 address for specified interface """
        command = "ip -6 addr show %s" % interface_name
        
        output = self.run(command)
        
        ipv6 = None
        
        for line in output.split('\n'):
            line = line.strip()
            
            if 'global' in line:
                parts = line.split(' ')
                ipv6 = parts[1]
                break
        
        return ipv6
    
    # TODO: this sucks
    @property
    def olsr(self):
        """
        returns tuple with version and url if OLSR is installed
        returns None if not installed
        """
        version_string = self.run('olsrd -v')
        
        if 'not found' in version_string:
            return False
        
        # extract olsr version and url
        lines = version_string.split('\n')
        version = lines[0].split(' - ')[1].strip()
        url = lines[2].strip()
        
        return (version, url)
