# ozi/_i18l.py
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
"""Internationalization utilities."""
from __future__ import annotations

import gettext
import html
import locale
import os
import site
import sys
from logging import getLogger
from pathlib import Path
from string import Template
from typing import Any
from typing import Callable

from ozi_core._logging import PytestFilter
from ozi_core._logging import config_logger

config_logger()
_LOCALE = locale.getlocale()[0]
mo_path = Path(site.getuserbase()) / 'share' / 'locale'
if 'PYTEST_VERSION' in os.environ or 'pytest' in sys.modules:
    mo_path = Path(__file__).parent.parent / 'po'
try:
    T = gettext.translation('ozi-core', localedir=mo_path)  # pragma: no cover
except FileNotFoundError as e:
    raise RuntimeError(os.listdir(mo_path)) from e
gettext.bindtextdomain('ozi-core', mo_path)


class Translation:
    """Translation API for use inside OZI tools.

    Wraps gettext.gettext with mimetype-specific postprocessing.
    """

    __slots__ = ('__logger', '_locale', '_mime_type', 'data')

    def __init__(self: Translation) -> None:
        self.data = {
            'en_US': gettext.translation('ozi-core', localedir=mo_path, languages=['en_US']),
            'en': gettext.translation('ozi-core', localedir=mo_path, languages=['en']),
            'zh_CN': gettext.translation('ozi-core', localedir=mo_path, languages=['zh_CN']),
            'zh': gettext.translation('ozi-core', localedir=mo_path, languages=['zh']),
        }
        self._mime_type = 'text/plain;charset=UTF-8'
        self._locale = _LOCALE if _LOCALE is not None and _LOCALE in self.data else 'en_US'
        self.__logger = getLogger(f'ozi_core.{__name__}.{self.__class__.__name__}')
        self.__logger.addFilter(PytestFilter())
        gettext.textdomain('ozi-core')

    @property
    def mime_type(self: Translation) -> str | Any:
        """Get the current MIME type setting."""
        return self._mime_type

    @mime_type.setter
    def mime_type(self: Translation, mime: str) -> None:
        """Set the MIME type for string translation."""
        if mime in {'text/plain;charset=UTF-8', 'text/html;charset=UTF-8'}:
            self._mime_type = mime
        else:
            self.__logger.debug(f'Invalid MIME type: {mime}')  # pragma: no cover

    @property
    def locale(self: Translation) -> str | Any:
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

    @property
    def gettext(self: Translation) -> Callable[[str], str]:
        t = TRANSLATION.data[TRANSLATION.locale]
        t.install()
        return t.gettext

    def __call__(self: Translation, _key: str, **kwargs: str) -> str:
        """Get translation text by key and pass optional substitutions as keyword arguments."""
        text = self.gettext(_key)
        if text is None:
            return ''  # pragma: no cover
        elif text is _key:
            self.__logger.debug(f'no translation for "{_key}" in locale "{self.locale}"')
            return Template(text).safe_substitute(**kwargs)
        return self.postprocess(Template(text).safe_substitute(**kwargs))


TRANSLATION = Translation()
