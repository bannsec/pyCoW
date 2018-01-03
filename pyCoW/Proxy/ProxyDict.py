
from collections import OrderedDict
from operator import itemgetter

# Things list class does in-place that we need to watch out for
proxy_list_inplace = ['clear', 'pop', 'popitem']

class in_init:
    """Silly class to handle setting and unsetting self.__in_init bool."""
    def __init__(self, obj):
        self.obj = obj
    def __enter__(self):
        self.obj._in_init = True
    def __exit__(self, type, value, traceback):
        self.obj._in_init = False

class ProxyDict(OrderedDict):
    def __init__(self, d):
        with in_init(self):
            # If we're already a Proxy Dict, just pass through
            if type(d) in [ProxyDict, OrderedDict]:
                return OrderedDict.__init__(self, d)

            # Sorting this by default to reduce burden on hash
            super().__init__(sorted(d.items(), key=itemgetter(1)))

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
        return hash(tuple(self.items()))

    def __setitem__(self, *args, **kwargs):
        super().__setitem__(*args, **kwargs)
        if not self._in_init:
            self._flyweight_cb_func(self)

    def __getattribute__(self, key):
        # If we don't need to proxy this call, just do it.
        if key not in proxy_list_inplace or key in vars(self).keys():
            return super().__getattribute__(key)

        # Proxy this call
        return lambda *args, **kwargs: list_do_generic_call(self, key, *args, **kwargs)

from . import list_do_generic_call
