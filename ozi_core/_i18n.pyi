"""
This type stub file was generated by pyright.
"""

from dataclasses import InitVar
from typing import TYPE_CHECKING
from typing import Any

"""Internationalization utilities."""
if TYPE_CHECKING:
    ...
_LOCALE = ...

class Translation:
    __slots__ = ('__logger', '_locale', '_mime_type', 'data')
    data: dict[str, str]
    def __init__(self) -> None: ...
    @property
    def mime_type(self: Translation) -> str | Any: ...
    @mime_type.setter
    def mime_type(self: Translation, mime: str) -> None: ...
    @property
    def locale(self) -> str | Any: ...
    @locale.setter
    def locale(self, loc: str) -> None: ...
    def postprocess(self: Translation, text: str) -> str: ...
    def __call__(self, _key: str, **kwargs: str) -> str: ...

TRANSLATION: Translation = ...
