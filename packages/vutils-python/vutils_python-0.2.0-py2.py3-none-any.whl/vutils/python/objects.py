#
# File:    ./src/vutils/python/objects.py
# Author:  Jiří Kučera <sanczes AT gmail.com>
# Date:    2022-06-24 14:07:30 +0200
# Project: vutils-python: Python language tools
#
# SPDX-License-Identifier: MIT
#
"""Python objects utilities."""

from typing import TYPE_CHECKING, cast

if TYPE_CHECKING:
    from collections.abc import Callable, Generator, MutableMapping

    from vutils.python import _KT, _VT


def merge_data(dest: object, src: object) -> None:
    """
    Merge data from the source object to the destination object.

    :param dest: The destination object
    :param src: The source object
    :raises TypeError: when destination and source have different types
    """
    if not isinstance(dest, type(src)):
        raise TypeError("src and dest should have same types!")

    if isinstance(src, list):
        cast("list[object]", dest).extend(src)
    elif isinstance(src, set):
        cast("set[object]", dest).update(src)
    elif isinstance(src, dict):
        cast("dict[object, object]", dest).update(src)
    else:
        cast("dict[str, object]", dest.__dict__).update(
            cast("dict[str, object]", src.__dict__)
        )


def ensure_key(
    mapping: "MutableMapping[_KT, _VT]", key: "_KT", default: "_VT"
) -> None:
    """
    Ensure <mapping> has a <key> of the same type as <default>.

    :param mapping: The mapping
    :param key: The key
    :param default: The default value if <key> is not set
    :raises TypeError: when the value under the <key> cannot be converted to
        the type that has <default>

    If <key> is present in <mapping>, ensure the value is of a same type as
    <default>. Otherwise, store <default> to <mapping> under <key>.
    """
    typecls: "type[_VT]" = type(default)
    if key in mapping and not isinstance(mapping[key], typecls):
        # Raises TypeError if conversion fails
        mapping[key] = cast("Callable[[_VT], _VT]", typecls)(mapping[key])
    if key not in mapping:
        mapping[key] = default


def ensure_no_key(mapping: "MutableMapping[_KT, _VT]", key: "_KT") -> None:
    """
    Ensure <key> is not present in <mapping>.

    :param mapping: The mapping
    :param key: The key
    """
    if key in mapping:
        del mapping[key]


def flatten(obj: object) -> "Generator[object, None, None]":
    """
    Flatten <obj> recursively.

    :param obj: The object to be flattened
    :return: the generator that yields items from flattened <obj>

    If <obj> is :class:`list` or :class:`tuple`, yield items from <obj>'s
    flattened element. Otherwise, yield <obj>.
    """
    if isinstance(obj, (tuple, list)):
        for elem in obj:
            yield from flatten(elem)
    else:
        yield obj
