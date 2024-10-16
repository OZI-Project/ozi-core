"""
This type stub file was generated by pyright.
"""

from __future__ import annotations

import curses
import os
import sys
from argparse import Namespace
from typing import TYPE_CHECKING
from unittest.mock import Mock

from ozi_core.new.interactive.project import Project

"""
``ozi-new`` interactive prompts
"""
if sys.platform != 'win32':
    ...
else:
    ...
if TYPE_CHECKING:
    ...
def interactive_prompt(project: Namespace) -> list[str]:
    ...

