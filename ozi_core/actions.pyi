"""
This type stub file was generated by pyright.
"""

from argparse import Action
from argparse import ArgumentParser
from argparse import Namespace
from collections.abc import Sequence
from dataclasses import dataclass
from typing import TYPE_CHECKING
from typing import Any
from typing import Collection
from typing import NoReturn

from packaging.version import Version

"""Parsing actions for the OZI commandline interface."""
if TYPE_CHECKING:
    ...
_prefix = ...
@dataclass
class ExactMatch:
    """Exact matches data for packaging core metadata."""
    audience: tuple[str, ...] = ...
    language: tuple[str, ...] = ...
    framework: tuple[str, ...] = ...
    environment: tuple[str, ...] = ...
    license: tuple[str, ...] = ...
    license_id: tuple[str, ...] = ...
    license_exception_id: tuple[str, ...] = ...
    status: tuple[str, ...] = ...
    topic: tuple[str, ...] = ...


class CloseMatch(Action):
    """Special argparse choices action. Warn the user if a close match could not be found."""
    exact_match = ...
    def __init__(self: Self, option_strings: list[str], dest: str, nargs: int | str | None = ..., **kwargs: Any) -> None:
        """Argparse init"""
        ...
    
    def close_matches(self: Self, key: str, value: str) -> Sequence[str]:
        """Get a close matches for a Python project packaging core metadata key.

        :param key: Python project packaging core metadata key name (normalized)
        :type key: str
        :param value: the value to query a close match for
        :type value: Sequence[str]
        :return: sequence with the best match or an empty sequence
        :rtype: Sequence[str]
        """
        ...
    
    def __call__(self: Self, parser: ArgumentParser, namespace: Namespace, values: str | Sequence[str] | None, option_string: str | None = ...) -> None:
        """Find closest matching class attribute."""
        ...
    


def check_for_update(current_version: Version, releases: Collection[Version]) -> None:
    """Issue a warning if installed version of OZI is not up to date."""
    ...

def check_version(version: str) -> NoReturn:
    """Check for a newer version of OZI and exit."""
    ...

def info(version: str) -> NoReturn:
    """Print all metadata as JSON and exit."""
    ...

def list_available(key: str) -> NoReturn:
    """Print a list of valid values for a key and exit."""
    ...

def license_expression(expr: str) -> NoReturn:
    """Validate a SPDX license expression."""
    ...
