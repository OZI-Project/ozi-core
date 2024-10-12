"""
``ozi-new`` interactive prompts
"""

from __future__ import annotations

import os
import sys
from typing import TYPE_CHECKING
from unittest.mock import Mock

if sys.platform != 'win32':
    import curses
else:
    curses = Mock()
    curses.tigetstr = lambda x: b''
    curses.setupterm = lambda: None

from ozi_core.new.interactive.project import Project

if TYPE_CHECKING:
    from argparse import Namespace


def interactive_prompt(project: Namespace) -> list[str]:  # pragma: no cover
    curses.setupterm()
    e3 = curses.tigetstr('E3') or b''
    clear_screen_seq = curses.tigetstr('clear') or b''
    os.write(sys.stdout.fileno(), e3 + clear_screen_seq)
    project_prompt = Project(check_package_exists=project.check_package_exists)
    return project_prompt()
