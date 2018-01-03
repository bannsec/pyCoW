
from ..CoW import CoW

# Things list class does in-place that we need to watch out for
proxy_list_inplace = ["append", "clear", "extend", "insert", "pop", "remove", "reverse", "sort"]

class ProxyList(list, CoW):

    def __init__(self, *args, **kwargs):
        CoW.__init__(self, *args, **kwargs)
        list.__init__(self, *args, **kwargs)

    def __hash__(self):
        return hash(tuple(self))

    def __copy__(self):
        return ProxyList(self)
    
    def __getattribute__(self, key):
        # If we don't need to proxy this call, just do it.
        if key not in proxy_list_inplace:
            return super().__getattribute__(key)

        # Proxy this call
        return lambda *args, **kwargs: list_do_generic_call(self, key, *args, **kwargs)

    def __setitem__(self, *args, **kwargs):
        # Letting CoW get first shot at this
        return CoW.__setitem__(self, *args, **kwargs)

    def __iadd__(self, *args, **kwargs):
        # Can't overload special methods through getattribute, so just proxying here.
        return list_do_generic_call(self, "__iadd__", *args, **kwargs)


from . import list_do_generic_call
