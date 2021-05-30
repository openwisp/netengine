try:
    from pysnmp.entity.rfc3413.oneliner import cmdgen
except ImportError:
    raise ImportError('pysnmp library is not installed, install it with "pip install pysnmp"')

from netengine.backends import BaseBackend
from netengine.exceptions import NetEngineError
from netengine.resources.interfaces import interfaces

__all__ = ['SNMP']


class SNMP(BaseBackend):
    """
    SNMP base backend
    """

    _oid_to_retrieve = None

    def __init__(self, host, community='public', agent='my-agent', port=161):
        """
        :host string: required
        :community string: defaults to public
        :agent string: defaults to my-agent
        :port integer: defaults to 161
        """
        self.host = host
        self.community = cmdgen.CommunityData(agent, community, 0)
        self.transport = cmdgen.UdpTransportTarget((host, port))
        self.port = port

    def __str__(self):
        """ prints a human readable object description """
        return "<SNMP: %s>" % self.host

    def __repr__(self):
        """ returns unicode string represantation """
        return self.__str__()

    def __unicode__(self):
        """ unicode __str__() for python2.7 """
        return unicode(self.__str__())

    @property
    def _command(self):
        """
        alias to cmdgen.CommandGenerator()
        """
        return cmdgen.CommandGenerator()

    def _oid(self, oid):
        """
        returns valid oid value to be passed to getCmd() or nextCmd()
        """
        if type(oid) not in (str, unicode, tuple, list):
            raise AttributeError('get accepts only strings, tuples or lists')
        # allow string representations of oids with commas ,
        elif isinstance(oid, basestring):
            # ignore spaces
            oid = oid.replace(' ', '').replace(',', '.')
        # convert lists and tuples into strings
        else:
            # convert each list item to string
            oid = [str(element) for element in oid]
            oid = '.'.join(oid)

        # ensure is string (could be unicode)
        return str(oid)

    def get(self, oid):
        """
        alias to cmdgen.CommandGenerator().getCmd
        :oid string|tuple|list: string,
        tuple or list representing the OID to get

        example of valid oid parameters:
            * "1,3,6,1,2,1,1,5,0"
            * "1, 3, 6, 1, 2, 1, 1, 5, 0"
            * "1.3.6.1.2.1.1.5.0"
            * [1, 3, 6, 1, 2, 1, 1, 5, 0]
            * (1, 3, 6, 1, 2, 1, 1, 5, 0)
        """
        print 'DEBUG: SNMP GET %s' % self._oid(oid)
        return self._command.getCmd(self.community, self.transport, self._oid(oid))

    def next(self, oid):
        """
        alias to cmdgen.CommandGenerator().nextCmd
        :oid string|tuple|list:
        string, tuple or list representing the OID to get

        example of valid oid parameters:
            * "1,3,6,1,2,1,1,5,0"
            * "1, 3, 6, 1, 2, 1, 1, 5, 0"
            * "1.3.6.1.2.1.1.5.0"
            * [1, 3, 6, 1, 2, 1, 1, 5, 0]
            * (1, 3, 6, 1, 2, 1, 1, 5, 0)
        """
        print 'DEBUG: SNMP NEXT %s' % self._oid(oid)
        return self._command.nextCmd(self.community, self.transport, self._oid(oid))

    def get_value(self, oid):
        """
        returns value of oid,
        or raises NetEngineError Exception is anything wrong
        :oid string|tuple|list:
        string, tuple or list representing the OID to get
        """
        result = self.get(oid)
        try:
            return str(result[3][0][1])  # snmp stores results in several arrays
        except IndexError:
            raise NetEngineError(str(result[0]))

    def _value_to_retrieve(self):
        """
        return the final SNMP indexes for the
        interfaces to be used in the other methods and properties
        """
        value_to_retr = []

        if (self._oid_to_retrieve is None):
            raise NetEngineError('Please fix properly the _oid_to_retrieve string in OpenWRT or AirOS SNMP backend')

        indexes = self.next(self._oid_to_retrieve)[3]

        for i in range(len(indexes)):
            value_to_retr.append(int(indexes[i][0][1]))

        return value_to_retr

    def interfaces(self, key):
        """
        Lookup to the interfaces' dictionary
        """
        try:
            return interfaces[key]
        except KeyError:
            raise NetEngineError("No valid interfaces found for key: %s" % key)
