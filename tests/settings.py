import json
import os

settings_file = os.getenv('TEST_SETTINGS_FILE', './test-settings.example.json')
settings = json.loads(open(settings_file).read())
settings['disable_mocks'] = os.getenv('DISABLE_MOCKS', '0') == '1'
