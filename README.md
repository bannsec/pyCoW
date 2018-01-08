[![Build Status](https://travis-ci.org/bannsec/pyCoW.svg?branch=master)](https://travis-ci.org/bannsec/pyCoW)
[![Coverage Status](https://coveralls.io/repos/github/bannsec/pyCoW/badge.svg?branch=master)](https://coveralls.io/github/bannsec/pyCoW?branch=master)

# Overview
This is an attempt at implementing a generic Copy-on-Write base class for python.

# How To Use
Feel free to give it a shot. I doubt that it is bug-free, but it may be minimal enough bugs to be helpful to your project.

## Setup

The basic way to integrate Copy-on-Write in the form of `pyCoW` into your project is to extend your classes with it. First step is to install pyCoW as you would a normal lib:

```bash
$ pip install pyCoW
```

Next, extend your class objects inheritance with it, as follows:

```python
from pyCoW import CoW

class MyClass(CoW):
    pass
```

Note, if you already have class inheritance on your object, you need to be careful. `pyCoW` assumes that it will be the secondary class, so that any `super()` calls will resolve to the intended class. Thus, if your object extended `int`, the following would be the correct order:

```python
class MyClass(int, CoW):
    pass
```

Also, note that it is important in the later case to override some magic methods with a simple stub. This allows `pyCoW` to manage those calls and work some copy-on-write magic in the middle. For instance, if you extended a dictionary, you would want `pyCoW` to handle managing your items. This could be done as follows:

```python
class MyClass(dict, CoW):
    def __setitem__(self, *args, **kwargs):
        return CoW.__setitem__(self, *args, **kwargs)

    def __getitem__(self, key):
        return CoW.__getitem__(self, key)
```

What is happening there is that you are explicitly choosing to use `pyCoW`'s get and set item calls. `pyCoW` will do it's own checks and work under the covers, then call your primary handler which in this case is the dict object. The result is that it should be mostly transparent that you are using this.

## Use
This library has a few main effects. First off, it attempts to be aggressive about not duplicating any of your items in memory. For instance, if you were to make two of the same attributes in different objects, you would only be making one actual object.

```python
from pyCoW import CoW

class MyClass(CoW):
    pass

obj = MyClass()
obj2 = MyClass()

obj.l = [1,2,3]
obj2.l = [1,2,3]

assert obj.l is obj2.l
```

In this case i'm asserting not only that they are equal, but that they are the same object entirely. However, if i were to continue and update one of them, now i have two separate objects.

```python
obj.l.append(4)
assert obj.l == [1,2,3,4]
assert obj2.l == [1,2,3]
```

One other key thing you can do on `CoW` objects is `copy`. In this case, you can think of `copy` as the python built-in `deepcopy` in that the object you get back should be a complete copy of the object in. The difference is that, since `CoW`'s version of `copy` utilizes aggressive caching and just-in-time copy, it will be substantially faster than `deepcopy` and will also take up much less memory on large objects. Example:

```python
from copy import copy

obj = MyClass()
# Do a bunch of things with obj
obj2 = copy(obj)
```

In this case, I'm using the `copy` method simply as a convenience wrapper to call `__copy__`. You could call that directly if you wished.

# Gotchas
## Variable Types
Variable types have to be changed for this to work. The change is done automatically for you, and for the most part should be in the background. However, you will notice that the variable type you put in (such as `list`) comes back as a different type (such as `ProxyList`). The type should behave the same as you would expect, but if you use `type(x) == ` checks in your code, you will need to adjust for the proxy versions of those types.

# Python Versions
This is being tested against 3.5+. There are known issues at the moment for 3.4, and anything below is untested.
