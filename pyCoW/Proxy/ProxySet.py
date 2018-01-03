
from ..CoW import CoW

# Things set class does in-place that we need to watch out for
proxy_list_inplace = ["add", "clear", "difference_update", "discard", "intersection_update", "pop", "remove", "symmetric_difference_update", "update"]

class ProxySet(set, CoW):
    def __init__(self, *args, **kwargs):
        set.__init__(self, *args, **kwargs)
        CoW.__init__(self, *args, **kwargs)
        self.__hash_cache = None

    def __hash__(self):
        if self.__hash_cache is None:
            self.__hash_cache = hash(tuple(self))
        return self.__hash_cache

    def __copy__(self):
        return ProxySet(self)

    def __getattribute__(self, key):
        # If we don't need to proxy this call, just do it.
        if key not in proxy_list_inplace:
            return super().__getattribute__(key)

        # Proxy this call
        return lambda *args, **kwargs: list_do_generic_call(self, key, *args, **kwargs)

from . import list_do_generic_call
