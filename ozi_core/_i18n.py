# ozi/_i18l.py
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
"""Internationalization utilities."""
from __future__ import annotations

import locale
from string import Template
from typing import TYPE_CHECKING
from typing import Any

from ozi_core._locales import data

if TYPE_CHECKING:  # pragma: no cover
    import sys

    if sys.version_info >= (3, 11):
        from typing import Self
    elif sys.version_info < (3, 11):
        from typing_extensions import Self

_LOCALE = locale.getlocale()[0]


class Translation:

    __slots__ = ('_locale', 'data')

    def __init__(self: Self) -> None:
        self.data = data
        self._locale = (
            _LOCALE[:2] if _LOCALE is not None and _LOCALE[:2] in self.data else 'en'
        )

    @property
    def locale(self: Self) -> str | Any:  # pragma: no cover
        return self._locale

    @locale.setter
    def locale(self: Self, loc: str) -> None:  # pragma: no cover
        if loc in self.data:
            self._locale = loc
        else:
            print('Invalid locale')

    def __call__(self: Self, _key: str, **kwargs: str) -> str:  # pragma: no cover
        if self.locale not in self.data:
            return _key
        text = self.data[self.locale].get(_key, _key)
        if text is None:
            return ''
        return Template(text).safe_substitute(**kwargs)


TRANSLATION = Translation()
