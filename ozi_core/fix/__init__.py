# ozi/fix/__init__.py
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
"""ozi-fix: Project fix script that outputs a meson rewriter JSON array."""
from __future__ import annotations

import json
import os
import sys
from contextlib import suppress
from pathlib import Path
from subprocess import PIPE
from subprocess import Popen
from typing import TYPE_CHECKING
from typing import NoReturn
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
from ozi_templates.filter import underscorify  # pyright: ignore
from tap_producer import TAP

from ozi_core.fix.build_definition import unroll_subdirs
from ozi_core.fix.build_definition import walk
from ozi_core.fix.interactive import interactive_prompt
from ozi_core.fix.missing import get_relpath_expected_files
from ozi_core.fix.missing import report
from ozi_core.fix.parser import parser
from ozi_core.fix.rewrite_command import Rewriter
from ozi_core.new.validate import valid_copyright_head

if TYPE_CHECKING:  # pragma: no cover
    from argparse import Namespace

    from jinja2 import Environment


def _setup(project: Namespace) -> tuple[Namespace, Environment]:  # pragma: no cover
    TAP.version(14)
    project.target = Path(os.path.relpath(os.path.join('/', project.target), '/')).absolute()
    if not project.target.exists():
        TAP.bail_out(f'target: {project.target} does not exist.')
    elif not project.target.is_dir():
        TAP.bail_out(f'target: {project.target} is not a directory.')
    with suppress(ValueError):
        project.add.remove('ozi.phony')
        project.remove.remove('ozi.phony')
    project.add = list(set(project.add))
    project.remove = list(set(project.remove))
    env = load_environment(vars(project), METADATA.asdict())  # pyright: ignore
    return project, env


def main(args: list[str] | None = None) -> NoReturn:  # pragma: no cover
    """Main ozi.fix entrypoint."""
    project = parser.parse_args(args=args)
    project.missing = project.fix in {'missing', 'm', 'mis'}
    project.interactive = project.fix in {'interactive', 'i'}
    match [project.interactive, project.missing, project.strict]:
        case [True, False, _]:
            with TAP.suppress():  # pyright: ignore
                project, env = _setup(project)
                name, *_ = report(project.target)
                project.name = underscorify(name)
            fd = sys.stdin.fileno()
            original_attributes = termios.tcgetattr(fd)
            tty.setraw(sys.stdin)
            args = interactive_prompt(project)
            termios.tcsetattr(fd, termios.TCSADRAIN, original_attributes)
            TAP.comment(f'ozi-fix {" ".join(args)}')
            main(args)
        case [False, True, False]:
            project, _ = _setup(project)
            name, *_ = report(project.target)
        case [False, False, _]:
            with TAP.suppress():  # pyright: ignore
                project, env = _setup(project)
                name, *_ = report(project.target)
                project.name = underscorify(name)
                project.license_file = 'LICENSE.txt'
                project.copyright_head = valid_copyright_head(
                    project.copyright_head,
                    name,
                    project.license_file,
                )
                rewriter = Rewriter(str(project.target), project.name, project.fix, env)
                rewriter += project.add
                rewriter -= project.remove
                for d in walk(
                    project.target,
                    get_relpath_expected_files(project.fix, name)[0],
                    [],
                ):
                    for k in d.keys():
                        build_text = unroll_subdirs(project.target, k)
                        Path(project.target / k / 'meson.build').write_text(build_text)
                TAP.plan()
            if len(project.add) > 0 or len(project.remove) > 0:
                out = json.dumps(rewriter.commands, indent=4 if project.pretty else None)
                if project.interactive_io:
                    res = Popen(
                        ['tox', '-e', 'invoke', '--', 'rewrite', out],
                        stdin=PIPE,
                    )
                    res.communicate()
                    if res.returncode != 0:
                        TAP.comment('ozi-fix failed to rewrite project files')
                else:
                    print(out)
            else:
                parser.print_help()
        case [False, True, True]:
            with TAP.strict():  # pyright: ignore
                project, _ = _setup(project)
                name, *_ = report(project.target)
        case [True, True, _]:
            TAP.bail_out('subcommands `interactive` and `missing` are mutually exclusive')
        case [_, _, _]:
            TAP.bail_out('Name discovery failed.')
    exit(0)
