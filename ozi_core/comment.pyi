"""
This type stub file was generated by pyright.
"""

import re
from collections import Counter
from enum import IntFlag
from functools import lru_cache
from pathlib import Path
from typing import TYPE_CHECKING
from typing import Generator
from typing import Sequence

"""Linter comment check utilities."""
if TYPE_CHECKING:
    ...
TIER3_COMMENTS = ...
TIER2_COMMENTS = ...
TIER1_COMMENTS = ...

class CommentQuality(IntFlag):
    """Comment tiers for scoring project quality."""

    TIER1 = ...
    TIER2 = ...
    TIER3 = ...

def calculate_score(lines: int, t1: int, t2: int, t3: int) -> float:
    """Calculate a quality score out of five.
    Comments have more impact on the score when lines is higher.

    :param lines: total line count
    :type lines: int
    :param t1: low-impact comments
    :type t1: int
    :param t2: intermediate-impact comments
    :type t2: int
    :param t3: high-impact comments
    :type t3: int
    :return: comment quality score out of 5.0
    :rtype: float
    """

@lru_cache
def pattern_cache(key: str) -> re.Pattern[str]:
    """Cached OZI specification linter comment pattern lookup.

    :param key: key in :py:class:`ozi_spec.CommentPatterns`
    :type key: str
    :return: compiled regular expression pattern
    :rtype: re.Pattern[str]
    """

def pattern_search(line: str) -> Generator[tuple[str, str], None, None]:
    """Search for OZI specification comment patterns.

    :param line: line text verbatim
    :type line: str
    :yield: key, match for key in :py:class:`ozi_spec.CommentPatterns` excluding ``help``
    :rtype: Generator[tuple[str, str], None, None]
    """

def diagnose(
    line: str, rel_path: Path, line_no: int
) -> Generator[tuple[str, str], None, None]:
    """Diagnose OZI comment pattern for a single line.

    :param line: line text verbatim
    :type line: str
    :param rel_path: file relative to OZI project root
    :type rel_path: Path
    :param line_no: current line number
    :type line_no: int
    """

def diagnostic(
    lines: Sequence[str], rel_path: Path, start: int = ...
) -> tuple[Counter[str], dict[str, str]]:
    """Diagnose OZI comment pattern for a sequence of lines (usually a single file).

    :param lines: lines to check
    :type lines: list[str]
    :param rel_path: file relative to OZI project root
    :type rel_path: Path
    :param start: starting line number for asynchronous chunking, defaults to 1
    :type start: int, optional
    :rtype: tuple[Counter[str], dict[str, str]]
    :return: count of lines and comment pattern matches as a dict
    """

def score_file(count: Counter[str]) -> float:
    """Score a single file comment diagnostic.

    .. deprecated:: 1.11.2

        Use :py:func:`ozi.comment.score` instead.
    """

def score(count: Counter[str]) -> float:
    """Score a single comment diagnostic.

    :param count: count of lines and comments
    :type count: Counter[str]
    :return: span comment score out of 5.0
    :rtype: float
    """

def comment_diagnostic(target: Path, rel_path: Path, file: str) -> None:
    """Run a scored comment diagnostic on a python file."""