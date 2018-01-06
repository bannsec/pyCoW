
from ..CoW import CoW, proxify

# Things list class does in-place that we need to watch out for
proxy_list_inplace = ["append", "clear", "extend", "insert", "pop", "remove", "reverse", "sort"]

class ProxyList(list, CoW):

    def __init__(self, iterable):

        # Recursively transform into CoW objects
        proxified = [proxify(item) for item in iterable]
        CoW.__init__(self, proxified)
        list.__init__(self, proxified)
        self._hash_cache = None

    def __hash__(self):
        if self._hash_cache is None:
            self._hash_cache = hash(tuple(self))
        return self._hash_cache

    def __copy__(self):
        return ProxyList(self)
    
    def __getattribute__(self, key):
        # If we don't need to proxy this call, just do it.
        if key not in proxy_list_inplace:
            return super().__getattribute__(key)

        # Proxy this call -- invalidate cache as we will be changing
        return lambda *args, **kwargs: list_do_generic_call(self, key, *args, **kwargs)

    def __setitem__(self, *args, **kwargs):
        # Invalidate our cache
        self._hash_cache = None
        # Letting CoW get first shot at this
        return CoW.__setitem__(self, *args, **kwargs)

    def __iadd__(self, *args, **kwargs):
        # Invalidate our cache
        self._hash_cache = None
        # Can't overload special methods through getattribute, so just proxying here.
        return list_do_generic_call(self, "__iadd__", *args, **kwargs)


from . import list_do_generic_call
