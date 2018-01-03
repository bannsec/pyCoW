
def list_do_generic_call(self, method_name, *args, **kwargs):
    # Run this call in-place
    ret = getattr(super(type(self), self), method_name)(*args, **kwargs)

    # Call our cb function
    for func in self._flyweight_cb_func:
        func(self)

    # Return any value that might be returned
    return ret

from .ProxyStr import ProxyStr
from .ProxyList import ProxyList
from .ProxyTuple import ProxyTuple
from .ProxySet import ProxySet
from .ProxyDict import ProxyDict
