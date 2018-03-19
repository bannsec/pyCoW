
from collections import OrderedDict
from operator import itemgetter
import weakref
from ..CoW import CoW, proxify

# Things list class does in-place that we need to watch out for
proxy_list_inplace = ['clear', 'pop', 'popitem']

class in_init:
    " ""Silly class to handle setting and unsetting self.__in_init bool."" "
    def __init__(self, obj):
        self.obj = obj
    def __enter__(self):
        self.obj._in_init = True
    def __exit__(self, type, value, traceback):
        self.obj._in_init = False

class ProxyDict(OrderedDict, CoW):
    def __init__(self, d):
        # Recursively proxify first
        d = {item: proxify(d[item]) for item in d}

        CoW.__init__(self)

        with in_init(self):
            
            self._hash_cache = None

            # If we're already a Proxy Dict, just pass through
            if type(d) in [ProxyDict, OrderedDict]:
                return OrderedDict.__init__(self, d)

            # Sorting this by default to reduce burden on hash
            #super().__init__(sorted(d.items(), key=itemgetter(1)))
            super().__init__(d)

        self._flyweight_register_self()

    def copy(self):
        """Weirdness in OrderedDict copy... Using mine instead."""
        return self.__copy__()

    def fromkeys(self, *args, **kwargs):
        """Need to figure out how to implement this. Getting strange errors."""
        raise NotImplementedError("I have not implemented this yet.")

    def __copy__(self):
        return ProxyDict(self)

    def __hash__(self):
        # TODO: Verify this actually produces a good hash...
        if self._hash_cache is None:
            self._hash_cache = hash(tuple(self.items()))
        return self._hash_cache

    def __setitem__(self, *args, **kwargs):
        if not self._in_init:
            # Letting CoW get first shot at this
            return CoW.__setitem__(self, *args, **kwargs)
        else:
            return super().__setitem__(*args, **kwargs)
    
    def __getattribute__(self, key):
        # If we don't need to proxy this call, just do it.
        if key not in proxy_list_inplace or key in vars(self).keys():
            return super().__getattribute__(key)

        # Proxy this call
        return lambda *args, **kwargs: list_do_generic_call(self, key, *args, **kwargs)

    def __getitem__(self, key):
        # Proxy to call first, which will come back to our first subclass of list.
        return CoW.__getitem__(self, key)

from . import list_do_generic_call
