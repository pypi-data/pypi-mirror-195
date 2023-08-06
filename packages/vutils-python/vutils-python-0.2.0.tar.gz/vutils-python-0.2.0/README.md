[![Coverage Status](https://coveralls.io/repos/github/i386x/vutils-python/badge.svg?branch=main)](https://coveralls.io/github/i386x/vutils-python?branch=main)
![CodeQL](https://github.com/i386x/vutils-python/actions/workflows/codeql.yml/badge.svg)

# vutils-python: Python Language Tools

This package provides a set of tools to deal with tasks related to Python
language environment, like copying data to or from objects, importing, object
analysis etc.

## Installation

To get `vutils-python`, just type
```sh
$ pip install vutils-python
```

## How To Use

Functions and classes provided by `vutils-python` can be accessed by importing
following submodules:
* `vutils.python.objects`

Each of these submodules is described in the following subsections.

### Objects Manipulation

Functions and classes that deals with Python objects, defined in
`vutils.python.objects` submodule, are
* `merge_data(dest, src)` merges data from `src` to `dest`. `src` and `dest`
  must be of the same type. Examples:
  ```python
  src = [1, 2, 3]
  dest = [1, 2]
  merge_data(dest, src)
  # dest will be [1, 2, 1, 2, 3]

  src = {1, 2, 3}
  dest = {2, 4}
  merge_data(dest, src)
  # dest will be {1, 2, 3, 4}

  src = {"a": "bc", 1: 2}
  dest = {1: "a", "b": "c"}
  merge_data(dest, src)
  # dest will be {1: 2, "a": "bc", "b": "c"}

  merge_data({}, [1])  # TypeError
  ```
* `ensure_key(mapping, key, default)` ensures `mapping` has a `key` of the same
  type a `default`. If `key` is not in `mapping`, store `default` to `mapping`
  under it.
* `ensure_no_key(mapping, key)` ensures `key` is not present in `mapping`.
* `flatten(obj)` flattens `obj` recursively if it is `list` or `tuple`.
