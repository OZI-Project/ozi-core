"""
This type stub file was generated by pyright.
"""

from dataclasses import dataclass
from functools import lru_cache
from typing import TYPE_CHECKING

"""Trove packaging classifiers interface."""
if TYPE_CHECKING:
    ...
@lru_cache
def get_trove_prefix(text: str) -> str | None:
    """Get a trove classifier prefix from a classifier string.

    :param text: full classifier text
    :type text: str
    :return: the prefix if the classifier text is valid otherwise None
    :rtype: str | None
    """
    ...

valid_trove_prefixes = ...
@dataclass(frozen=True, slots=True, eq=True)
class Prefix:
    """Trove :term:`classifier` prefix literals for :term:`PyPI`"""
    audience: str = ...
    environment: str = ...
    framework: str = ...
    language: str = ...
    license: str = ...
    status: str = ...
    topic: str = ...
    def __post_init__(self: Self) -> None:
        """Check if any of the default attributes are deprecated upstream."""
        ...
    


@lru_cache
def from_prefix(prefix: str) -> tuple[str, ...]:
    """Return all matching classifiers for a prefix string."""
    ...
