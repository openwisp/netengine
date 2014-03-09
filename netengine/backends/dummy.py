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
        
        '''	Validation of self.port '''
	 	try:
			if self.port<0 or self.port>65535:
				''' If self.port is not valid, raise NetEngineError '''
				raise Exception("NetEngineError")
		except:
			raise Exception("NetEngineError")
			

		''' validation of self.host '''
		try:
			validate_host_list = self.host.split(".")
			if len(validate_host_list)!=4:
				raise Exception("NetEngineError")
			for validate_host_var in validate_host_list:
				if int(validate_host_var)<0 or int(validate_host_var)>255:
					''' If self.host is not valid, raise NetEngineError '''
					raise Exception("NetEngineError")
		except:
			raise Exception("NetEngineError")

    
    def __str__(self):
        """ print a human readable object description """
        return u"<Dummy NetEngine %s>" % self.host
    
    def to_dict(self):
        return self._dict({
            "name": "dummy",
            "type": "radio",
            "os": "dummyOS",
            "os_version": "0.1",
            "manufacturer": "dummy inc.",
            "model": "dummy model",
            "RAM_total": 65536,
            "uptime": 0,
            "uptime_tuple": (0, 0, 0),
            "interfaces": [
                {
                    "type": "wireless",
                    "name": "wifi0",
                    "mac_address": "de:9f:db:30:c9:c5",
                    "mtu": 1500,
                    "standard": "802.11n",
                    "channel": 5745,
                    "channel_width": 20,
                    "mode": "ap",
                    "output_power": 18,
                    "tx_rate": None,
                    "rx_rate": None,
                    "dbm": -27,
                    "noise": -97,
                    "ip": [
                        {
                            "version": 4,
                            "address": '192.168.1.1'
                        },
                        {
                            "version": 6,
                            "address": '2001:4c00:893b:fede::1'
                        }
                    ],
                    "vap": [
                        {
                            "essid": "dummyssid",
                            "bssid": "",
                            "encryption": ""
                        }
                    ]
                },
                {
                    "type": "ethernet",
                    "name": "eth0",
                    "mac_address": "de:9f:db:30:c9:c4",
                    "mtu": 1500,
                    "standard": "fast",
                    "duplex": "full",
                    "tx_rate": None,
                    "rx_rate": None,
                    "ip": [
                        {
                            "version": 4,
                            "address": '192.168.1.2'
                        },
                        {
                            "version": 6,
                            "address": '2001:4c00:893b:fede::2'
                        }
                    ]
                }
            ],
            "antennas": [],
            "routing_protocols": [
                {
                    "name": "olsr",
                    "version": "dummy version"
                }
            ]
        })
