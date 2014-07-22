from netengine.backends import BaseBackend
from netengine.exceptions import NetEngineError


__all__ = ['HTTP']


class HTTP(BaseBackend):
    """
    HTTP base backend
    """

    _authentication = None
    _status_cgi = None

    def __init__(self, host, username, password):
        """
        :host string: required
        :username string: required
        :username string: required
        """
        self.host = host
        self.username = username
        self.password = password
        self._authentication = {"username" : str(self.username) , "password" : str(self.password)}

    def __str__(self):
        """ prints a human readable object description """
        return "<HTTP: %s>" % self.host

    def __repr__(self):
        """ returns unicode string represantation """
        return self.__str__()
