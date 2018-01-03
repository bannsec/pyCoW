
from ..CoW import CoW

class ProxyStr(str, CoW):
    def __init__(self, *args, **kwargs):
        # str keeps it's setup all in __new__
        CoW.__init__(self, *args, **kwargs)

    def __copy__(self):
        return ProxyStr(self)
