from .base import BaseBackend


class Dummy(BaseBackend):
    """
    Dummy backend
    """
    def __init__(self, host, port=0):
        """ dummy netengine backend for development or testing """
        self.host = host
        self.port = port
    
    def validate(self):
        """
        raises NetEngineError exception if anything is wrong with the connection
        for example: wrong host, invalid credentials
        """
        pass
    
    def __str__(self):
        """ print a human readable object description """
        return u"<Dummy NetEngine %s>" % self.host