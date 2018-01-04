from pyCoW import CoW, ProxyList
from copy import copy

class MyClass(CoW):
    pass

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

