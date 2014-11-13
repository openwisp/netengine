from netengine.resources.manufacturers import dictionary


def manufacturer_lookup(mac_address):
    """ Lookup to the manufacturers' dictionary """
    # strip : or -
    mac_address = str(mac_address.replace(':', '').replace('-', '').upper())
    # us prefix only
    mac_address = mac_address[0:6]
    # return manufacturer
    return dictionary[mac_address]
