from netengine.resources.manufacturers import dictionary
from netengine.exceptions import NetEngineError


def manufacturer_lookup(mac_address):
    """ Lookup to the manufacturers' dictionary """
    key = str(mac_address)
    # strip : or -
    key = key.replace(':', '').replace('-', '').upper()
    # us prefix only
    key = key[0:6]
    # return manufacturer
    try:
        return dictionary[key]
    except KeyError:
        raise NetEngineError("No valid manufacturer found for mac address: %s" % mac_address)
