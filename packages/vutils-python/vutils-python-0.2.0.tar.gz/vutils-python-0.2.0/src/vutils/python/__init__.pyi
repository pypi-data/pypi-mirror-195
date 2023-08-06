#
# File:    ./src/vutils/python/__init__.pyi
# Author:  Jiří Kučera <sanczes AT gmail.com>
# Date:    2022-06-24 14:03:43 +0200
# Project: vutils-python: Python language tools
#
# SPDX-License-Identifier: MIT
#

from collections.abc import Generator, MutableMapping
from typing import TypeVar

_KT = TypeVar("_KT")
_VT = TypeVar("_VT")

def merge_data(dest: object, src: object) -> None: ...
def ensure_key(
    mapping: MutableMapping[_KT, _VT], key: _KT, default: _VT
) -> None: ...
def ensure_no_key(mapping: MutableMapping[_KT, _VT], key: _KT) -> None: ...
def flatten(obj: object) -> Generator[object, None, None]: ...
