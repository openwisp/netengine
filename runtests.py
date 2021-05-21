#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
try:
    import nose
except:
    message = """nose package not installed, install test requirements with:
    pip install -r requirements-test.txt
    """
    raise ImportError(message)

if __name__ == "__main__":
    file_path = os.path.abspath(__file__)
    tests_path = os.path.join(os.path.abspath(os.path.dirname(file_path)), "tests")
    parser = argparse.ArgumentParser()
    parser.add_argument('--disable-mocks', default='1')
    parser.add_argument('--test-settings', default='test-settings.example.json')
    args = parser.parse_args(args=None)
    os.environ["DISABLE_MOCKS"] = args.disable_mocks
    os.environ["TEST_SETTINGS_FILE"] = os.path.join(
        os.path.dirname(file_path), args.test_settings
    )
    result = nose.run(
        argv=[
            os.path.abspath(__file__),
            "--with-cov",
            "--cover-package=netengine",
            tests_path
        ]
    )
