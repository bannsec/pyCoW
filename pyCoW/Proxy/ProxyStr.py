
class ProxyStr(str):
    def __copy__(self):
        return ProxyStr(self)
