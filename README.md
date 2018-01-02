[![Build Status](https://travis-ci.org/bannsec/pyCoW.svg?branch=master)](https://travis-ci.org/bannsec/pyCoW)
[![Coverage Status](https://coveralls.io/repos/github/bannsec/pyCoW/badge.svg?branch=master)](https://coveralls.io/github/bannsec/pyCoW?branch=master)

# Overview
This is an attempt at implementing a generic Copy-on-Write base class for python.

# Gotchas
## Variable Types
Variable types have to be changed for this to work. The change is done automatically for you, and for the most part should be in the background. However, you will notice that the variable type you put in (such as `list`) comes back as a different type (such as `ProxyList`). The type should behave the same as you would expect, but if you use `type(x) == ` checks in your code, you will need to adjust for the proxy versions of those types.
