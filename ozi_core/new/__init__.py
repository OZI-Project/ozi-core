# ozi/new/__init__.py
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
"""ozi-new: quick-start OZI project creation script."""
from __future__ import annotations

import shlex
import sys
from typing import TYPE_CHECKING
from unittest.mock import Mock

if sys.platform != 'win32':
    import termios
    import tty
else:  # pragma: no cover
    tty = Mock()
    termios = Mock()
    tty.setraw = lambda x: None
    termios.tcgetattr = lambda x: None
    termios.tcsetattr = lambda x, y, z: None

from ozi_spec import METADATA
from ozi_templates import load_environment
from tap_producer import TAP

from ozi_core.new.interactive import interactive_prompt
from ozi_core.new.parser import parser
from ozi_core.new.validate import postprocess_arguments
from ozi_core.new.validate import preprocess_arguments
from ozi_core.render import RenderedContent

if TYPE_CHECKING:  # pragma: no cover
    from argparse import Namespace


def project(project: Namespace) -> None:
    """Create a new project in a target directory."""
    project = postprocess_arguments(preprocess_arguments(project))
    RenderedContent(
        load_environment(vars(project), METADATA.asdict()),  # pyright: ignore
        project.target,
        project.name,
        project.ci_provider,
        project.long_description_content_type,
        project.update_wrapfile,
    ).render()


def wrap(project: Namespace) -> None:  # pragma: no cover
    """Create a new wrap file for publishing. Not a public function."""
    env = load_environment(vars(project), METADATA.asdict())  # pyright: ignore
    template = env.get_template('ozi.wrap.j2')
    with open('ozi.wrap', 'w', encoding='UTF-8') as f:
        f.write(template.render())


def main(args: list[str] | None = None) -> None:  # pragma: no cover
    """Main ozi.new entrypoint."""
    if args is None:
        TAP.version(14)
    ozi_new = parser.parse_args(args=args)
    ozi_new.argv = shlex.join(args) if args else shlex.join(sys.argv[1:])
    match ozi_new:
        case ozi_new if ozi_new.new in ['i', 'interactive']:
            fd = sys.stdin.fileno()
            original_attributes = termios.tcgetattr(fd)
            tty.setraw(sys.stdin)
            args = interactive_prompt(ozi_new)
            termios.tcsetattr(fd, termios.TCSADRAIN, original_attributes)
            TAP.comment(f'ozi-new {" ".join(args)}')
            ozi_new = parser.parse_args(args=args)
            main(args)
        case ozi_new if ozi_new.new in ['p', 'project']:
            project(ozi_new)
            TAP.end()
        case ozi_new if ozi_new.new in ['w', 'wrap']:
            wrap(ozi_new)
            TAP.end()
        case _:
            parser.print_usage()
    return None
