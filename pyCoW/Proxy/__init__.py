import logging
logger = logging.getLogger("CoW:Proxy")

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
    copy_required = False if get_true_reference_count(self) <= 1 else True

    logger.debug("list_do_generic_call({},{},{},{})".format(self, method_name, args, kwargs))
    logger.debug("copy_required = {}".format(copy_required))

    if copy_required:
        # Just-in-time copy
        my_copy = copy(self)
        my_type = type(my_copy)

        # Invalidate hash cache if one exists
        if hasattr(my_copy, "_hash_cache"):
            my_copy._hash_cache = None
    else:
        my_copy = self
        my_type = type(self)
        my_old_hash = hash(self)

    # HACK: I need to figure out a proper sloution for this... Tuple __iadd__ (and likely others) causes infinite recursion.
    if my_type is ProxyTuple:
        my_type = ProxyList

    # Proxify the args if we need to
    args = [proxify(arg) for arg in args]
    kwargs = {key: proxify(val) for key,val in kwargs.items()}

    # Run this call in-place
    ret = getattr(super(my_type, my_copy), method_name)(*args, **kwargs)

    # Only bother calling update if we had to copy
    if copy_required:
        # Call our cb function
        #for func in self._flyweight_cb_func.values():
        for func in self._flyweight_cb_func:
            func(my_copy)
    else:
        # Update the cache with our new value

        # Remove ref to this object since hash changed
        try:
            del CoW._flyweight_cache[type(my_copy)][my_old_hash]
        except:
            pass

        # Invalidate hash cache if one exists
        if hasattr(my_copy, "_hash_cache"):
            my_copy._hash_cache = None
        # Add new ref
        CoW._flyweight_cache[type(my_copy)][hash(my_copy)] = my_copy

    # Return any value that might be returned
    return ret

from copy import copy
import gc
from .ProxyStr import ProxyStr
from .ProxyList import ProxyList
from .ProxyTuple import ProxyTuple
from .ProxySet import ProxySet
from .ProxyDict import ProxyDict
from ..CoW import CoW, proxify
