"""
This type stub file was generated by pyright.
"""

from pathlib import Path
from typing import Generator

"""Build definition check utilities."""
IGNORE_MISSING = ...
def inspect_files(target: Path, rel_path: Path, found_files: list[str], extra_files: list[str]) -> list[str]:
    ...

def process(target: Path, rel_path: Path, found_files: list[str] | None = ...) -> list[str]:
    """Process an OZI project build definition's files."""
    ...

def validate(target: Path, rel_path: Path, subdirs: list[str], children: set[str] | None) -> Generator[Path, None, None]:
    """Validate an OZI standard build definition's directories."""
    ...

def walk(target: Path, rel_path: Path, found_files: list[str] | None = ..., project_name: str | None = ...) -> None:
    """Walk an OZI standard build definition directory."""
    ...
