"""
``ozi-new`` interactive prompts
"""

from __future__ import annotations

import os
import sys
from dataclasses import asdict
from typing import TYPE_CHECKING
from unittest.mock import Mock

if sys.platform != 'win32':
    import curses
else:
    curses = Mock()
    curses.tigetstr = lambda x: b''
    curses.setupterm = lambda: None

from ozi_core.config import read_user_config
from ozi_core.new.interactive.project import Project

if TYPE_CHECKING:
    from argparse import Namespace


def interactive_prompt(project: Namespace) -> list[str]:  # pragma: no cover
    curses.setupterm()
    e3 = curses.tigetstr('E3') or b''
    clear_screen_seq = curses.tigetstr('clear') or b''
    os.write(sys.stdout.fileno(), e3 + clear_screen_seq)
    config = asdict(read_user_config())
    project_prompt = Project(
        allow_file=config['new']['allow_file'],
        check_package_exists=project.check_package_exists,
        ci_provider=config['new']['ci_provider'],
        copyright_head=config['new']['copyright_head'],
        enable_cython=config['new']['enable_cython'],
        enable_uv=config['new']['enable_uv'],
        github_harden_runner=config['new']['github_harden_runner'],
        strict=config['new']['strict'],
        verify_email=config['new']['verify_email'],
    )
    return project_prompt()
