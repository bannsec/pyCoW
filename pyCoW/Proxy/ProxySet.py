
# Things set class does in-place that we need to watch out for
proxy_list_inplace = ["add", "clear", "difference_update", "discard", "intersection_update", "pop", "remove", "symmetric_difference_update", "update"]

class ProxySet(set):
    def __hash__(self):
        return hash(tuple(self))

    def __copy__(self):
        return ProxySet(self)

    def __getattribute__(self, key):
        # If we don't need to proxy this call, just do it.
        if key not in proxy_list_inplace:
            return super().__getattribute__(key)

        # Proxy this call
        return lambda *args, **kwargs: list_do_generic_call(self, key, *args, **kwargs)

from . import list_do_generic_call
