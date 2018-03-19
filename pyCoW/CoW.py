
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

import logging
logger = logging.getLogger("CoW")

import weakref
from copy import copy
import types

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
flyweight_ignored_keys = ["_flyweight_cache","_flyweight_cb_func","_my_flyweight_cb_func"]
flyweight_ignored_types = (int, float, type(None), bool) + weakref.ProxyTypes

class CoW(object):

    # Using weakref to allow garbage collection
    # dict[<var_type>][__hash__]
    # TODO: pypy doesn't delete right away... might be an issue
    _flyweight_cache = {}
    
    def __init__(self, *args, **kwargs):
        # Jenky.. But i need to keep a hard ref until this object is removed.
        #self._my_flyweight_cb_func = {} # Contains hard ref for my lambda functions I'm setting in other objects
        #self._my_flyweight_cb_func = weakref.WeakValueDictionary() # Contains hard ref for my lambda functions I'm setting in other objects
        self._my_flyweight_cb_func = None # Contains hard ref for my lambda functions I'm setting in other objects
        #self._flyweight_cb_func = weakref.WeakValueDictionary()
        self._flyweight_cb_func = weakref.WeakSet() # Contains refs to those functions I should notify when I copy update
        super().__init__()

        # If we're initing from ourselves, copy over
        if len(args) >= 1 and type(args[0]) == type(self):
            obj = args[0]

            # Basic variables
            if hasattr(obj, "__dict__"):
                # Using setters here so we auto register callbacks with things relevant
                for key, value in vars(obj).items():
                    if key in flyweight_ignored_keys:
                        continue

                    # Standardize private vars
                    if key.startswith("__") and not key.endswith("__"):
                        key = key.replace("__","_{}__".format(self.__class__.__name__),1)

                    # If value is not CoW subclass, it likely won't handle CoW correctly. Strait up copy it
                    if not issubclass(type(value), CoW):
                        value = copy(value)

                    object.__setattr__(self, key, value)

            # Slot variables
            if hasattr(obj, "__slots__"):
                # Using setters here so we auto register callbacks with things relevant
                for key in obj.__slots__:
                    if key in flyweight_ignored_keys:
                        continue

                    # Standardize private vars
                    if key.startswith("__") and not key.endswith("__"):
                        key = key.replace("__","_{}__".format(self.__class__.__name__),1)

                    value = getattr(obj, key)
                    # If value is not CoW subclass, it likely won't handle CoW correctly. Strait up copy it
                    if not issubclass(type(value), CoW):
                        value = copy(value)

                    object.__setattr__(self, key, value)

    def __getitem__(self, key):
        #print("__getitem__", self, key)

        #value = super(type(self), self).__getitem__(key)
        # TODO: There's probably a better way to handle this...
        # Check if we're the top level. If we are, raise exception
        getitem = super(type(self), self).__getitem__
        if getitem == self.__getitem__:
            raise TypeError("'{}' object does not support indexing".format(self.__class__.__name__))

        value = getitem(key)
        
        # If this was a single value, add a cb func
        if type(key) is not slice and issubclass(type(value), CoW):
            self.__cow_add_cb_pointer(value, key=key, key_type='item')

        #print("__getitem__ returning ", value)
        return value

    def __setattr__(self, key, value):
        logger.debug("CoW:setattr({},{},{})".format(self, key, value))

        # Don't proxify our ignored keys
        if key not in flyweight_ignored_keys:
            value = proxify(value)

        # Non-flyweight classes
        if type(value) in flyweight_ignored_types or key in flyweight_ignored_keys:
            return super().__setattr__(key, value)

        # If this is a private attribute, adjust
        if key.startswith("__") and not key.endswith("__"):
            key = key.replace("__","_{}__".format(self.__class__.__name__),1)

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
        # If this is a private attribute, adjust
        if key.startswith("__") and not key.endswith("__"):
            key = key.replace("__","_{}__".format(self.__class__.__name__),1)

        # Grab the value
        value = super().__getattribute__(key)

        # Don't proxy our own stuff
        # If this is a function, don't try to copy it
        if key in flyweight_ignored_keys or type(value) in [types.BuiltinFunctionType, types.MethodType, types.FunctionType]:
            return value

        # Writing callback value so we can be notified if this object updates in place.
        if issubclass(type(value), CoW):
            self.__cow_add_cb_pointer(value, key=key, key_type='attribute')

        return value

    def __cow_add_cb_pointer(self, obj, key, key_type):
        """Register a cb with the object to let us know if it has updated."""

        # Check if I have already registered with this object
        #if not any(f for f in obj._flyweight_cb_func if any(f2.cell_contents is self for f2 in f.__closure__)):
        #print("setting cb", self, id(self), id(obj), obj)
        """
        if id(obj) not in self._my_flyweight_cb_func:

            # Record it so we have a hard pointer
            self._my_flyweight_cb_func[id(obj)] = lambda new_value: self.__cow_update_object(obj, new_value)
        """

        # Record it so it doesn't disappear
        self._my_flyweight_cb_func = lambda new_value: self.__cow_update_object(old=obj, new=new_value, key=key, key_type=key_type)

        # Tell the object we're interested in it
        #obj._flyweight_cb_func.add(self._my_flyweight_cb_func[id(obj)])
        # Deciding to only use one cb function at a time. Always set it at get time so we know which obj we're talking about
        obj._flyweight_cb_func.clear()
        #obj._flyweight_cb_func.add(self._my_flyweight_cb_func[id(obj)])
        obj._flyweight_cb_func.add(self._my_flyweight_cb_func)

    def __copy__(self):
        """Perform fast copy of attribute pointers in self. Note: This assumes that you are not doing anything aside from copying variables in your __init__. Meaning, if you end up creating new custom objects, connecting to databases, etc, this will not work for you. You can override this with your own copy however."""

        """
        # Create blank object
        obj = self.__new__(type(self))

        # Copy over our refs, recursively calling copy
        for key, value in vars(self).items():
            # Since we're coming from CoW object, copy directly instead of doing CoW get/set lookups.
            #super(type(obj),obj).__setattr__(key, value)
            object.__setattr__(obj, key, value)
        """
        #obj = type(self)(self)

        obj = type(self).__new__(type(self))
        CoW.__init__(obj, self)

        return obj

    def __hash__(self):
        """Overriding hash function for CoW object. Feel free to do your own if
        this doesn't work for you."""

        # Hashing on the slots
        if hasattr(self,"__slots__"):
            return hash(tuple(self.__slots__))

        # If no slots, use vars
        return hash(tuple((x,y) for x,y in vars(self).items() if x not in flyweight_ignored_keys))

    # Extending this for the sake of inheriting CoW
    def __setitem__(self, key, item):
        # Proxy types that we have autoproxy for
        if type(item) in [list, dict, set, tuple]:
            item = proxify(item)

        # Just-in-time copy
        my_copy = copy(self)

        # Set it
        super(type(my_copy), my_copy).__setitem__(key, item)

        # Notify anyone who cares
        #for func in self._flyweight_cb_func.values():
        for func in self._flyweight_cb_func:
            func(my_copy)

    def __cow_update_object(self, old, new, key, key_type):
        """Iterates through all attributes and items in current object, replacing any that have the id of the old object with the id of the new object.
        
        Args:
            old: The old obj to replace
            new: The new object to replace it with
            key: The name of the attribute or item (or None if this is a Set)
            key_type: The type (i.e.: "attribute", "item")
        """
        logging.debug('CoW.__cow_update_object({},{},{},{},{})'.format(self, old, new, key, key_type))

        key_type = key_type.lower()
        assert key_type in ["attribute", "item"]

        if key_type == "attribute":

            if hasattr(self, key):
                #assert getattr(self, key) is old
                setattr(self, key, new)

            """
            # TODO: Optimize this so i'm not scanning every time
            # Not using __slots__
            if hasattr(self, "__dict__"):
                for new_key, new_value in vars(self).items():
                    if new_key != key:
                        continue

                    assert new_value is old:
                    setattr(self, new_key, new)
            
            # Using __slots__
            if hasattr(self, "__slots__"):
                for key in self.__slots__:
                    if getattr(self, key) is old:
                        setattr(self, key, new)
            """

        else:
            # If we expose items, update those too
            #try:

            # Iterate over list
            if issubclass(type(self), (list, dict)):
                value = self[key]
                #assert value is old
                self[key] = new
                """
                for i, key in enumerate(self):
                    if key is old:
                        self[i] = new
                """

            # Iterate over set
            elif issubclass(type(self), set):
                #assert old in self
                self.remove(old)
                self.add(new)

            """
            # Iterate over dict
            elif issubclass(type(self), dict):
                for key in self:
                    if self[key] is old:
                        self[key] = new
            """

            #except Exception as e:
            #    pass
        
        """
        # Remove any local cb reference we have so gc will get it
        keys_to_delete = []
        for key, val in self._my_flyweight_cb_func.items():
            for cell in val.__closure__:
                if cell.cell_contents is old:
                    keys_to_delete.append(key)
                    break

        # Can't remove during iteration. Do it now.
        for key in keys_to_delete:
            del self._my_flyweight_cb_func[key]
        """
        #print("__cow_update_object outcome: ", self)

    def _flyweight_register_self(self):
        """Makes sure our object is registered in the cache."""

        # Make sure the type is in our cache
        if type(self) not in self._flyweight_cache.keys():
            self._flyweight_cache[type(self)] = weakref.WeakValueDictionary()

        my_hash = hash(self)

        if my_hash not in self._flyweight_cache[type(self)].keys():
            self._flyweight_cache[type(self)][my_hash] = self


class Test(CoW):
    pass

# Import our proxies
# Implementing __copy__ on each Proxy as it's faster than the normal copy method.
from .Proxy import ProxyStr, ProxyList, ProxyTuple, ProxySet, ProxyDict
