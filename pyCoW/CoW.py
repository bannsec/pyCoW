
#
# Base concept taken from Yannick Loiseau
# http://yloiseau.net/articles/DesignPatterns/flyweight/
#

"""
This class was created as a base class, or "Mixin"/PureAbstract. Conceptually,
I needed a way to transparently minimize memory footprint, and more importantly
reduce the cost for creating a copy of any given object. That's what the
purpose of this class is.

Traditional FlyWeight pattern is useful for ensuring you do not duplicate
memory. However, given I require to state split, I also wanted to utilize
Copy-On-Write principles for performance. Thus, I take the concept of
FlyWeight pattern, and extend it by instrumenting getattr and setattr. The net
result is that, transparent to the underlying python class object, every
attribute is actually a pointer and memory is reduced in that manner. Also, I
override the __copy__ method to copy the pointers into a new object instead of
fully traversing get/set. This allows me to not have to implement custom copy
methods per each class, and instead utilize the duck typing of python to make
this all transparent.
"""

import weakref
from copy import copy
import types

# Import our proxies
from .Proxy import ProxyStr, ProxyList, ProxyTuple, ProxySet, ProxyDict

# Implementing __copy__ on each Proxy as it's faster than the normal copy method.

def proxify(value):
    """Wrap the value in a proxy shell if need be. Returns the object or the proxy object."""

    if type(value) is str:
        value = ProxyStr(value)

    elif type(value) is list:
        value = ProxyList(value)

    elif type(value) is tuple:
        value = ProxyTuple(value)

    elif type(value) is set:
        value = ProxySet(value)

    elif type(value) is dict:
        value = ProxyDict(value)

    return value

# Thing to explicitly not try to flyweight
flyweight_ignored_keys = ["_flyweight_cache","_flyweight_cb_func"]
flyweight_ignored_types = [int, float, type(None), bool]

class CoW(object):

    # Using weakref to allow garbage collection
    # dict[<var_type>][__hash__]
    # TODO: pypy doesn't delete right away... might be an issue
    _flyweight_cache = {}

    def __setattr__(self, key, value):

        # Standardize the value up front
        value = proxify(value)

        # Non-flyweight classes
        if type(value) in flyweight_ignored_types or value in flyweight_ignored_keys:
            return super().__setattr__(key, value)

        # Make sure the type is in our cache
        if type(value) not in self._flyweight_cache.keys():
            self._flyweight_cache[type(value)] = weakref.WeakValueDictionary()

        # If an equivalent object exists, use that
        value_hash = hash(value)
        if value_hash in self._flyweight_cache[type(value)].keys():
            return super().__setattr__(key, self._flyweight_cache[type(value)][value_hash])

        # No matching object exists, save off this one
        self._flyweight_cache[type(value)][value_hash] = value

        # Set the attr
        return super().__setattr__(key, value)

    def __getattribute__(self, key):
        # Grab the value
        value = super().__getattribute__(key)

        # Don't proxy our own stuff
        # If this is a function, don't try to copy it
        if key in flyweight_ignored_keys or type(value) in [types.BuiltinFunctionType, types.MethodType, types.FunctionType]:
            return value

        # Returning copies so we can Copy on Write.
        value = copy(value)

        # Writing callback value so we can be notified if this object updates in place.
        if type(value) in [ProxyList, ProxySet, ProxyDict]:
            value._flyweight_cb_func = lambda value: self.__setattr__(key, value)

        return value

    def __copy__(self):
        """Perform fast copy of attribute pointers in self. Note: This assumes that you are not doing anything aside from copying variables in your __init__. Meaning, if you end up creating new custom objects, connecting to databases, etc, this will not work for you. You can override this with your own copy however."""

        # Create blank object
        obj = self.__new__(type(self))

        # Copy over our refs, recursively calling copy
        for key, value in vars(self).items():
            # Since we're coming from CoW object, copy directly instead of doing CoW get/set lookups.
            super(type(obj),obj).__setattr__(key, value)

        return obj

    def __hash__(self):
        """Overriding hash function for CoW object. Feel free to do your own if
        this doesn't work for you."""

        # Hashing on the slots
        if hasattr(self,"__slots__"):
            return hash(tuple(self.__slots__))

        # If no slots, use vars
        return hash(tuple(vars(self).values()))

class Test(CoW):
    pass
