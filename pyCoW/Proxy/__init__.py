
def get_true_reference_count(obj):
    """Returns the true refernce count (that we're interested in) for the object. Useful in decision making of mod in place or not."""

    count = 0
    for ref in gc.get_referrers(obj):
        if type(ref) is dict and "_my_flyweight_cb_func" in ref:
            count += 1

    return count

def list_do_generic_call(self, method_name, *args, **kwargs):
    """Runs a call that we know ahead of time will modify the state of this object. I.e.: list.clear()"""

    # If only one thing is watching, we don't need to copy
    copy_required = False if get_true_reference_count(self) == 1 else True

    if copy_required:
        # Just-in-time copy
        my_copy = copy(self)
        my_type = type(my_copy)
    else:
        my_copy = self
        my_type = type(self)

    # HACK: I need to figure out a proper sloution for this... Tuple __iadd__ (and likely others) causes infinite recursion.
    if my_type is ProxyTuple:
        my_type = ProxyList

    # Run this call in-place
    ret = getattr(super(my_type, my_copy), method_name)(*args, **kwargs)

    # Only bother calling update if we had to copy
    if copy_required:
        # Call our cb function
        for func in self._flyweight_cb_func.values():
            func(my_copy)

    # Return any value that might be returned
    return ret

from copy import copy
import gc
from .ProxyStr import ProxyStr
from .ProxyList import ProxyList
from .ProxyTuple import ProxyTuple
from .ProxySet import ProxySet
from .ProxyDict import ProxyDict
