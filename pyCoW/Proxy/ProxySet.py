
class ProxySet(set):
    def __hash__(self):
        return hash(tuple(self))

    def __copy__(self):
        return ProxySet(self)
