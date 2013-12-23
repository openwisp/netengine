import json

try:
    settings = json.loads(open('../test-settings.json').read())
except IOError:
    settings = json.loads(open('./test-settings.json').read())