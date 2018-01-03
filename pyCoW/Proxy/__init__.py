

def list_do_generic_call(self, method_name, *args, **kwargs):
    """Runs a call that we know ahead of time will modify the state of this object. I.e.: list.clear()"""

    # Just-in-time copy
    my_copy = copy(self)
    my_type = type(my_copy)

    # HACK: I need to figure out a proper sloution for this... Tuple __iadd__ (and likely others) causes infinite recursion.
    if my_type is ProxyTuple:
        my_type = ProxyList

    # Run this call in-place
    ret = getattr(super(my_type, my_copy), method_name)(*args, **kwargs)

    # Call our cb function
    for func in self._flyweight_cb_func.values():
        func(my_copy)

    # Return any value that might be returned
    return ret

from copy import copy
from .ProxyStr import ProxyStr
from .ProxyList import ProxyList
from .ProxyTuple import ProxyTuple
from .ProxySet import ProxySet
from .ProxyDict import ProxyDict
