from netengine.backends import BaseBackend
from netengine.exceptions import NetEngineError

import requests

__all__ = ['HTTP']


class HTTP(BaseBackend):
    """
    HTTP base backend
    """
    
    _cookie = None
    
    def __init__(self, host, username, password):
        """
        :host string: required
        :username string: required
        :username string: required
        """
        self.host = host
        self.username = username
        self.password = password
        
    def __str__(self):
        """ prints a human readable object description """
        return "<HTTP: %s>" % self.host
    
    def __repr__(self):
        """ returns unicode string represantation """
        return self.__str__()

    def __unicode__(self):
        """ unicode __str__() for python2.7 """
        return unicode(self.__str__())
    
    @property
    def cookie(self):
        cookies = {}
        authentication = {"Username" : str(self.username) , "Password" : str(self.password)}
        cookies['AIROS_SESSIONID'] = requests.post("http://" + self.host + "/login.cgi?uri=/", data = authentication, verify = False).cookies.get('AIROS_SESSIONID')
        cookies['ui_language'] = requests.post("http://" + self.host + "/login.cgi?uri=/", data = authentication, verify = False).cookies.get('ui_language')
        self._cookie = cookies
        
    def get_json(self):
        json = requests.get("http://" + self.host + "/status.cgi", cookies = self._cookie, verify = False)
        return json
    
    
    