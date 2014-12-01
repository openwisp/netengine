import os
import json
import urllib2


def parse_manufacturers():
    """
    Downloads the latest MAC Address Block Large table
    and converts it to a python dictionary
    """
    dictionary = {}
    manufacturer_file = urllib2.urlopen("https://standards.ieee.org/develop/regauth/oui/oui.txt")
    for line in manufacturer_file.readlines():
        if "(hex)" in line:
            pairs = []
            pairs = line.split("(hex)")
            key = pairs[0].replace(' ', '').replace('-', '').upper()
            value = pairs[1].strip('\t\r\n')
            dictionary[key] = value
    json_file = json.dumps(dictionary, indent=4, sort_keys=True)
    out_file = open("manufacturers.py", "w")
    out_file.write("dictionary = " + json_file)
    out_file.close()


if __name__ == '__main__':
    parse_manufacturers()
