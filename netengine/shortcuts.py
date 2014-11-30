try:
    from collections import OrderedDict
except ImportError:
    OrderedDict = dict  # python < 2.7
