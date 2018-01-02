
# Things list class does in-place that we need to watch out for
proxy_list_inplace = ["append", "clear", "extend", "insert", "pop", "remove", "reverse", "sort"]

def list_do_generic_call(self, *args, **kwargs):
    # Run this call in-place
    method_name = kwargs.pop('CoWProxMethodName')
    ret = getattr(super(type(self), self), method_name)(*args, **kwargs)

    # Call our cb function
    self._flyweight_cb_func(self)

    # Return any value that might be returned
    return ret

class ProxyList(list):
    def __hash__(self):
        return hash(tuple(self))

    def __copy__(self):
        return ProxyList(self)
    
    def __getattribute__(self, key):
        # If we don't need to proxy this call, just do it.
        if key not in proxy_list_inplace:
            return super().__getattribute__(key)

        # Proxy this call
        return lambda *args, **kwargs: list_do_generic_call(self, *args, **kwargs, CoWProxMethodName=key)
