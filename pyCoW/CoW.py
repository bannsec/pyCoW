
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

NOTE: Due to how I'm type changing under the covers, calling "vars" will lie to
you sometimes. To get the real value of that variable, you will need to get it
via the attribute.
"""

import weakref
from copy import copy

#
# Some basic proxying
#

class ProxyStr(str):
    pass

class ProxyList(list):
    def __hash__(self):
        return hash(tuple(self))

# Tuple cannot directly be weak referenced... Need some magic.
class ProxyTuple(ProxyList):
    def __init__(self, tup):
        # Turning into a list so we can weakref
        return super().__init__(tup)

    def __eq__(self, obj):
        """Pretending to be a tuple..."""
        return tuple(self) == obj

    def __hash__(self):
        return hash(tuple(self))

class ProxySet(set):
    def __hash__(self):
        return hash(tuple(self))

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

    return value

def unproxify(value):
    """Remove the proxy layer. Returns the object."""
    if type(value) is ProxyStr:
        value = str(value)

    elif type(value) is ProxyList:
        value = list(value)

    elif type(value) is ProxyTuple:
        value = tuple(value)

    elif type(value) is ProxySet:
        value = set(value)

    return value


class CoW(object):
    # Using weakref to allow garbage collection
    # dict[<var_type>][__hash__]
    # TODO: pypy doesn't delete right away... might be an issue
    _flyweight_cache = {}

    # Types we don't want to cache
    _flyweight_ignored_types = [int, float, type(None), bool]

    def __setattr__(self, key, value):

        # Standardize the value up front
        value = proxify(value)

        # Save off the type of this attr
        #super().__setattr__("__{key:s}_type".format(key=key), type(value))

        # Non-flyweight classes
        if type(value) in self._flyweight_ignored_types:
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
        # Don't proxy our own stuff
        if key in ["_flyweight_ignored_types","_flyweight_cache"]:
            return super().__getattribute__(key)

        return copy(super().__getattribute__(key))
        #value = super().__getattribute__(key)
        #return unproxify(value)

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
