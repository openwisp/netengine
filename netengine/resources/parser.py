import os
import json


def parse_manufacturer():
    dictionary = {}
    manufacturer_file = open("manufacturers.txt")
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
    parse_manufacturer()