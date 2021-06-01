#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

try:
    import nose2
except ImportError:
    message = """nose package not installed, install test requirements with:
    pip install -r requirements-test.txt
    """
    raise ImportError(message)

if __name__ == '__main__':
    file_path = os.path.abspath(__file__)
    tests_path = os.path.join(os.path.abspath(os.path.dirname(file_path)), 'tests',)
    nose2.discover()
    result = nose2.main()
