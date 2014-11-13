

def manufacturer_lookup(mac_address):
    """ Lookup to the manufacturers' dictionary """
    mac_address = str(mac_address.replace(':', '').replace('-', '').upper())
    mac_address = mac_address[0:6]
    return dictionary[mac_address]
    
