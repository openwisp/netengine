"""
SSH base class
"""

__all__ = ['SSH']


import paramiko

from netengine.exceptions import NetEngineError


class SNMP(object):
    """
    SNMP base backend
    """
    
    def __init__(self, host, community='public'):
        """
        :host string: required
        :community string: defaults to public
        """
        self.host = host
        self.community = community
    
    def __str__(self):
        """ print a human readable object description """
        return "<SNMP: %s-%s>" % (self.host, self.community)
    
    def __repr__(self):
        """ return unicode string represantation """
        return self.__str__()
    
    def __unicode__(self):
        """ unicode __str__() for python2.7 """
        return unicode(self.__str__())
    
    #def connect(self):
    #    """
    #    Initialize SSH session
    #    
    #    will raise exception if anything goes wrong
    #    """
    #    shell = paramiko.SSHClient()
    #    shell.load_system_host_keys()
    #    shell.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #    
    #    shell.connect(
    #        self.host,
    #        username=self.username,
    #        password=self.password,
    #        port=self.port
    #    )
    #    self.shell = shell
    #
    #def disconnect(self):
    #    """ closes SSH connection """
    #    self.shell.close()
    #
    #def exec_command(self, command, **kwargs):
    #    """ alias to paramiko.SSHClient.exec_command """
    #    # init connection if necessary
    #    if self.shell is None:
    #        self.connect()
    #    
    #    return self.shell.exec_command(command, **kwargs)
    #
    #def run(self, command, **kwargs):
    #    """
    #    executes command and returns stdout if success or stderr if error
    #    """
    #    stdin, stdout, stderr = self.exec_command(command, **kwargs)
    #    
    #    output = stdout.read().strip()
    #    error = stderr.read().strip()
    #    
    #    # if error return error msg
    #    if error != '':
    #        return error
    #    # otherwise return output
    #    else:
    #        return output
    #
    #def get_interfaces(self):
    #    """ get device interfaces """
    #    return ifconfig_to_dict(self.run('ifconfig'))
    #
    #def get_ipv6_of_interface(self, interface_name):
    #    """ return ipv6 address for specified interface """
    #    command = "ip -6 addr show %s" % interface_name
    #    
    #    output = self.run(command)
    #    
    #    for line in output.split('\n'):
    #        line = line.strip()
    #        
    #        if 'global' in line:
    #            parts = line.split(' ')
    #            ipv6 = parts[1]
    #            break
    #    
    #    return ipv6
    
    @property
    def olsr(self):
        """
        should return tuple with version and url if OLSR is installed
        should return None if not installed
        """
        raise NotImplementedError('Not implemented')
    
    @property
    def os(self):
        """
        Not Implemented
        
        should return a tuple in which
        the first element is the OS name and
        the second element is the OS version
        """
        raise NotImplementedError('Not implemented')
    
    @property
    def name(self):
        """
        Not Implemented
        
        should return a string containing the device name
        """
        raise NotImplementedError('Not implemented')
    
    @property
    def model(self):
        """
        Not Implemented
        
        should return a string containing the device model
        """
        raise NotImplementedError('Not implemented')
    
    @property
    def RAM_total(self):
        """
        Not Implemented
        
        should return a string containing the device RAM in bytes
        """
        raise NotImplementedError('Not implemented')
    
    @property
    def ethernet_standard(self):
        """
        Not Implemented
        """
        raise NotImplementedError('Not implemented')
    
    @property
    def ethernet_duplex(self):
        """
        Not Implemented
        """
        raise NotImplementedError('Not implemented')
    
    @property
    def wireless_channel_width(self):
        """
        Not Implemented
        """
        raise NotImplementedError('Not implemented')
    
    @property
    def wireless_mode(self):
        """
        Not Implemented
        """
        raise NotImplementedError('Not implemented')
    
    @property
    def wireless_channel(self):
        """
        Not Implemented
        """
        raise NotImplementedError('Not implemented')
    
    @property
    def wireless_output_power(self):
        """
        Not Implemented
        """
        raise NotImplementedError('Not implemented')
    
    @property
    def wireless_dbm(self):
        """
        Not Implemented
        """
        raise NotImplementedError('Not implemented')
    
    @property
    def wireless_noise(self):
        """
        Not Implemented
        """
        raise NotImplementedError('Not implemented')