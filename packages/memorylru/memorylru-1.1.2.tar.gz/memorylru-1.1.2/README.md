# Introduction

Fork of https://github.com/plone/guillotina/tree/master/guillotina/contrib/cache into
its own package.

This package provides an LRU cache that is constrained by the size, in-memory of the
objects in the cache.

```python
from memorylru import LRU

lru = LRU(1024 * 1024 * 50)

lru['foo'] = 'bar'
```