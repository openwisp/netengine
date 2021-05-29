import json
from collections import OrderedDict

from netaddr import EUI, NotRegisteredError

__all__ = ['BaseBackend']


class BaseBackend(object):
    """
    Base NetEngine Backend
    """

    __netengine__ = True
    _dict = OrderedDict

    def __str__(self):
        raise NotImplementedError('Not implemented, must be extended')

    def __repr__(self):
        """returns unicode string represantation"""
        return self.__str__()

    def validate(self):
        raise NotImplementedError('Not implemented')

    def to_dict(self):
        raise NotImplementedError('Not implemented')

    def to_json(self, **kwargs):
        dictionary = self.to_dict()
        return json.dumps(dictionary, **kwargs)

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
    def uptime(self):
        """
        Not Implemented

        should return an integer representing the number of seconds of uptime
        """
        raise NotImplementedError('Not implemented')

    @property
    def uptime_tuple(self):
        """
        Not Implemented

        should return tuple (days, hours, minutes)
        """
        raise NotImplementedError('Not implemented')

    @property
    def ethernet_standard(self):
        raise NotImplementedError('Not implemented')

    @property
    def ethernet_duplex(self):
        raise NotImplementedError('Not implemented')

    @property
    def wireless_channel_width(self):
        raise NotImplementedError('Not implemented')

    @property
    def wireless_mode(self):
        raise NotImplementedError('Not implemented')

    @property
    def wireless_channel(self):
        raise NotImplementedError('Not implemented')

    @property
    def wireless_output_power(self):
        raise NotImplementedError('Not implemented')

    @property
    def wireless_dbm(self):
        raise NotImplementedError('Not implemented')

    @property
    def wireless_noise(self):
        raise NotImplementedError('Not implemented')

    # TODO: this sucks
    @property
    def olsr(self):
        raise NotImplementedError('Not implemented')

    def get_interfaces(self):
        raise NotImplementedError('Not implemented')

    def get_manufacturer(self, mac_address):
        """returns the manufacturer of the network interface"""
        if not mac_address:
            return ''
        try:
            return EUI(mac_address).oui.registration().org
        except NotRegisteredError:
            return ''
