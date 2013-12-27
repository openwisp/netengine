from .base import BaseBackend


class Dummy(BaseBackend):
    """
    Dummy backend
    """
    def __init__(self, host, port=0):
        """ dummy netengine backend for development or testing """
        self.host = host
        self.port = port
    
    def __str__(self):
        """ print a human readable object description """
        return u"<Dummy NetEngine %s>" % self.host