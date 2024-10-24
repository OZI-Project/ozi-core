# ozi/_i18l.py
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
"""Internationalization utilities."""
from __future__ import annotations

import locale
from string import Template
from typing import Any

from ozi_core._locales import data

_LOCALE = locale.getlocale()[0]


class Translation:
    """Translation API for use inside OZI tools."""

    __slots__ = ('_locale', 'data')

    def __init__(self: Translation) -> None:
        """Try to get the system locale and load translations."""
        self.data = data
        self._locale = (
            _LOCALE[:2] if _LOCALE is not None and _LOCALE[:2] in self.data else 'en'
        )

    @property
    def locale(self: Translation) -> str | Any:  # pragma: no cover
        """Get the current locale setting."""
        return self._locale

    @locale.setter
    def locale(self: Translation, loc: str) -> None:  # pragma: no cover
        """Set the locale for string translation."""
        if loc in self.data:
            self._locale = loc
        else:
            print('Invalid locale')

    def __call__(self: Translation, _key: str, **kwargs: str) -> str:  # pragma: no cover
        """Get translation text by key and pass optional substitions as keyword arguments."""
        if self.locale not in self.data:
            return _key
        text = self.data[self.locale].get(_key, _key)
        if text is None:
            return ''
        return Template(text).safe_substitute(**kwargs)


TRANSLATION = Translation()
