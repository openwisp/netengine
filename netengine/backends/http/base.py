from netengine.backends import BaseBackend
from netengine.exceptions import NetEngineError


try:
    import mechanize
except ImportError:
    "No mechanize installed on this host import json"
import json

__all__ = ['HTTP']


class HTTP(BaseBackend):
    """
    HTTP base backend
    """
    
    _authentication = None
    _host_json = None
    
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

    def get_json(self):
        if not self._host_json:
            browser = mechanize.Browser()
            browser.set_handle_robots(False)   # ignore robots
            browser.addheaders = [('User-agent', 'Firefox')]
            response = browser.open("https://10.40.0.130/login.cgi?uri=/status.cgi")
            browser.form = list(browser.forms())[0] 
            browser.select_form(nr = 0)
            browser.form['username'] = str(self._authentication['username'])
            browser.form['password'] = str(self._authentication['password'])
            request = browser.submit()
            result = json.loads(request.read())
            self._host_json = result
        return result
       
        
        
        