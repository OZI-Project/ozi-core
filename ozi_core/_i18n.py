# ozi/_i18l.py
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
"""Internationalization utilities."""
from __future__ import annotations

import glob
import os
from locale import getlocale
from pathlib import Path
from string import Template
from typing import Self

import yaml

_LOCALE = getlocale()[0]


class Translation:

    def __init__(self: Self) -> None:
        self.data = {}
        self._locale: str = _LOCALE[:2] if _LOCALE else 'en'

        files = glob.glob(os.path.join(Path(__file__).parent / 'data', '*.yml'))
        for f in files:
            loc = os.path.splitext(os.path.basename(f))[0]
            with open(f, 'r', encoding='utf8') as fh:
                self.data[loc] = yaml.safe_load(fh)

    @property
    def locale(self: Self) -> str:  # pragma: no cover
        return self._locale

    @locale.setter
    def locale(self: Self, loc: str) -> None:  # pragma: no cover
        if loc in self.data:
            self._locale = loc
        else:
            print('Invalid locale')

    def __call__(self: Self, key: str, **kwargs: str) -> str:  # pragma: no cover
        if self.locale not in self.data:
            return key
        text = self.data[self.locale].get(key, key)
        return Template(text).safe_substitute(**kwargs)


TRANSLATION = Translation()
