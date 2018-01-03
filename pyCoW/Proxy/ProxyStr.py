
from ..CoW import CoW

class ProxyStr(str, CoW):
    def __init__(self, *args, **kwargs):
        # str keeps it's setup all in __new__
        CoW.__init__(self, *args, **kwargs)
        self.__hash_cache = None

    def __hash__(self):
        if self.__hash_cache is None:
            self.__hash_cache = super().__hash__()
        return self.__hash_cache

    def __copy__(self):
        return ProxyStr(self)
