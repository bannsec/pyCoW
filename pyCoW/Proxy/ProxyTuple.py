from .ProxyList import ProxyList

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

    def __copy__(self):
        return ProxyTuple(self)

    def __setitem__(self, *args, **kwargs):
        raise TypeError("'tuple' object does not support item assignment")

