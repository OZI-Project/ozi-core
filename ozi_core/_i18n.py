# ozi/_i18l.py
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
"""Internationalization utilities."""
from __future__ import annotations

import html
import locale
from logging import getLogger
from string import Template
from typing import Any

from ozi_core._locales import data
from ozi_core._logging import PytestFilter
from ozi_core._logging import config_logger

config_logger()
_LOCALE = locale.getlocale()[0]


class Translation:
    """Translation API for use inside OZI tools.

    Try to get the system locale and load translations.
    """

    __slots__ = ('__logger', '_locale', '_mime_type', 'data')

    def __init__(self: Translation) -> None:
        self.data = data
        self._mime_type = 'text/plain;charset=UTF-8'
        self._locale = (
            _LOCALE[:2] if _LOCALE is not None and _LOCALE[:2] in self.data else 'en'
        )
        self.__logger = getLogger(f'ozi_core.{__name__}.{self.__class__.__name__}')
        self.__logger.addFilter(PytestFilter())

    @property
    def mime_type(self: Translation) -> str | Any:  # pragma: no cover
        """Get the current MIME type setting."""
        return self._mime_type

    @mime_type.setter
    def mime_type(self: Translation, mime: str) -> None:  # pragma: no cover
        """Set the MIME type for string translation."""
        if mime in {'text/plain;charset=UTF-8', 'text/html;charset=UTF-8'}:
            self._mime_type = mime
        else:
            self.__logger.debug(f'Invalid MIME type: {mime}')

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
            self.__logger.debug(f'Invalid locale: {loc}')

    def postprocess(self: Translation, text: str) -> str:
        """Final function called on a translation before return."""
        if self.mime_type == 'text/plain;charset=UTF-8':
            pass
        elif self.mime_type == 'text/html;charset=UTF-8':  # pragma: defer to E2E
            text = html.escape(text)
            for i in '（(『/.':
                text = text.replace(i, f'<wbr>{i}')
            for i in '』）)　：－-:':
                text = text.replace(i, f'{i}<wbr>')
        return text

    def __call__(self: Translation, _key: str, **kwargs: str) -> str:  # pragma: no cover
        """Get translation text by key and pass optional substitions as keyword arguments."""
        if self.locale not in self.data:
            return _key
        text = self.data[self.locale].get(_key, _key)
        if text is None:
            return ''
        elif text is _key:
            self.__logger.debug(f'no translation for "{_key}" in locale "{self.locale}"')
            return Template(text).safe_substitute(**kwargs)
        return self.postprocess(Template(text).safe_substitute(**kwargs))


TRANSLATION = Translation()
