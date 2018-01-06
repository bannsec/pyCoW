from pyCoW import CoW, ProxyList
from copy import copy

class MyClass(CoW):
    pass

"""
)

In [18]: t.l
Out[18]: [<pyCoW.CoW.Test at 0x7fe2e9868748>]

In [19]: t3 = copy(t)

In [20]: t3
Out[20]: <pyCoW.CoW.Test at 0x7fe2e9844cf8>

In [21]: t
Out[21]: <pyCoW.CoW.Test at 0x7fe2e98de5f8>

In [22]: t3.l
Out[22]: [<pyCoW.CoW.Test at 0x7fe2e9868748>]

In [23]: t3.l[0]
Out[23]: <pyCoW.CoW.Test at 0x7fe2e9868748>

In [24]: t3.l[0].l
---------------------------------------------------------------------------
AttributeError                            Traceback (most recent call last)
<ipython-input-24-73783679de36> in <module>()
----> 1 t3.l[0].l

~/opt/pyCoW/pyCoW/CoW.py in __getattribute__(self, key)
     92     def __getattribute__(self, key):
     93         # Grab the value
---> 94         value = super().__getattribute__(key)
     95
     96         # Don't proxy our own stuff

AttributeError: 'Test' object has no attribute 'l'

In [25]: t3.l[0].l = [1,2,3]

In [26]: t3.l[0].l
Out[26]: [1, 2, 3]

In [27]: t.l[0].l
Out[27]: [1, 2, 3]

"""

def test_list_subupdate():
    t = MyClass()

    t.l = [1,2,3]
    assert t.l == [1,2,3]
    assert len(t._flyweight_cache[ProxyList]) == 1
    t2 = copy(t)

    t.l.append(t2)
    
    # Make sure we're copying correctly
    assert t.l[-1] == t.l[-1]
    assert t.l[-1] == t2

    # Try appending to it, make sure it gets back up
    t.l[-1].l.append(4)
    assert t.l[-1].l == [1,2,3,4]
    assert t.l[:-1] == [1,2,3]
    assert len(t.l) == 4

    # Setitem
    t.l[-1].l[2] = 5
    assert t.l[:-1] == [1,2,3]
    assert len(t.l) == 4
    assert t.l[-1].l == [1, 2, 5, 4]

    # Update higher in list
    t.l.append(5)
    assert t.l[:3] == [1,2,3]
    assert len(t.l) == 5
    assert t.l[-1] == 5
    assert t.l[-2].l == [1, 2, 5, 4]

def test_list_subcow():
    """Adding a CoW inside the CoW"""
    t = MyClass()

    t.l = [1,2,3,4]
    assert t.l == [1,2,3,4]
    assert len(t._flyweight_cache[ProxyList]) == 1
    t2 = MyClass()
    t2.l = [5,6,7,8]

    t.l.append(t2)
    
    # Make sure we're copying correctly
    assert t.l[-1] == t.l[-1]
    assert t.l[-1] == t2

    # Try appending to it, make sure it gets back up
    t.l[-1].l.append(9)
    assert t.l[-1].l == [5,6,7,8,9]

def test_list_setitem_hash():
    t = MyClass()

    t.l = [1,2,3,4]
    assert t.l == [1,2,3,4]
    assert len(t._flyweight_cache[ProxyList]) == 1

    old_hash = hash(t.l)
    t.l[1] = 5
    new_hash = hash(t.l)

    assert old_hash != new_hash
    assert len(t._flyweight_cache[ProxyList]) == 1
    assert new_hash in t._flyweight_cache[ProxyList]

def test_list_append_hash():
    t = MyClass()

    t.l = [1,2,3,4]
    assert t.l == [1,2,3,4]
    assert len(t._flyweight_cache[ProxyList]) == 1

    old_hash = hash(t.l)
    t.l.append(5)
    new_hash = hash(t.l)

    assert old_hash != new_hash
    assert len(t._flyweight_cache[ProxyList]) == 1
    assert new_hash in t._flyweight_cache[ProxyList]

def test_list_setitem():
    t = MyClass()

    t.l = [1,2,3,4]
    assert t.l == [1,2,3,4]
    assert len(t._flyweight_cache[ProxyList]) == 1

    t2 = copy(t)

    assert t2.l == t.l

    t.l[2] = 10
    assert t.l == [1,2,10,4]
    assert t2.l == [1,2,3,4]

def test_list_sort():
    t = MyClass()

    t.l = [4,2,3,1]
    assert t.l == [4,2,3,1]
    assert len(t._flyweight_cache[ProxyList]) == 1

    t2 = copy(t)

    assert t2.l == t.l

    t.l.sort()
    assert t.l == [1,2,3,4]
    assert t2.l == [4,2,3,1]

def test_list_reverse():
    t = MyClass()

    t.l = [1,2,3,4]
    assert t.l == [1,2,3,4]
    assert len(t._flyweight_cache[ProxyList]) == 1

    t2 = copy(t)

    assert t2.l == t.l

    t.l.reverse()
    assert t.l == [4,3,2,1]
    assert t2.l == [1,2,3,4]

def test_list_remove():
    t = MyClass()

    t.l = [1,2,3,4]
    assert t.l == [1,2,3,4]
    assert len(t._flyweight_cache[ProxyList]) == 1

    t2 = copy(t)

    assert t2.l == t.l

    t.l.remove(4)
    assert t.l == [1,2,3]
    assert t2.l == [1,2,3,4]

def test_list_pop():
    t = MyClass()

    t.l = [1,2,3,4]
    assert t.l == [1,2,3,4]
    assert len(t._flyweight_cache[ProxyList]) == 1

    t2 = copy(t)

    assert t2.l == t.l

    assert t.l.pop(2) == 3
    assert t.l == [1,2,4]
    assert t2.l == [1,2,3,4]


def test_list_insert():
    t = MyClass()

    t.l = [1,2,3,4]
    assert t.l == [1,2,3,4]
    assert len(t._flyweight_cache[ProxyList]) == 1

    t2 = copy(t)

    assert t2.l == t.l

    t.l.insert(1,5)
    assert t.l == [1, 5, 2, 3, 4]
    assert t2.l == [1,2,3,4]

def test_list_extend():
    t = MyClass()

    t.l = [1,2,3,4]
    assert t.l == [1,2,3,4]
    assert len(t._flyweight_cache[ProxyList]) == 1

    t2 = copy(t)

    assert t2.l == t.l

    t.l.extend([5,6,7])
    assert t.l == [1,2,3,4,5,6,7]
    assert t2.l == [1,2,3,4]

def test_list_clear():
    t = MyClass()

    t.l = [1,2,3,4]
    assert t.l == [1,2,3,4]
    assert len(t._flyweight_cache[ProxyList]) == 1

    t2 = copy(t)

    assert t2.l == t.l

    t.l.clear()
    assert t.l == []
    assert t2.l == [1,2,3,4]

    t = copy(t2)
    assert t2.l == t.l

    t2.l.clear()
    assert t2.l == []
    assert t.l == [1,2,3,4]


def test_list_append():
    t = MyClass()

    t.l = [1,2,3,4]
    assert t.l == [1,2,3,4]
    assert len(t._flyweight_cache[ProxyList]) == 1

    t2 = copy(t)

    assert t2.l == t.l

    t.l.append(5)
    assert t.l == [1,2,3,4,5]
    assert t2.l == [1,2,3,4]

def test_list_basic():
    t = MyClass()

    t.l = [1,2,3,4]
    assert t.l == [1,2,3,4]

    assert len(t._flyweight_cache[ProxyList]) == 1

    t2 = copy(t)
    assert t2.l == t.l

    t.l += [5]
    assert t.l == [1,2,3,4,5]
    assert t2.l == [1,2,3,4]
    assert len(t._flyweight_cache[ProxyList]) == 2

