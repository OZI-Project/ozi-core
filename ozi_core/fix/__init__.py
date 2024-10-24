# ozi/fix/__init__.py
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
"""ozi-fix: Project fix script that outputs a meson rewriter JSON array."""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import TYPE_CHECKING
from typing import NoReturn

from ozi_spec import METADATA
from ozi_templates import load_environment
from ozi_templates.filter import underscorify  # pyright: ignore
from tap_producer import TAP

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
    project.add.remove('ozi.phony')
    project.add = list(set(project.add))
    project.remove.remove('ozi.phony')
    project.remove = list(set(project.remove))
    env = load_environment(vars(project), METADATA.asdict())  # pyright: ignore
    return project, env


def main() -> NoReturn:  # pragma: no cover
    """Main ozi.fix entrypoint."""
    project = parser.parse_args()
    project.missing = project.fix == 'missing' or project.fix == 'm'
    with TAP() as t:
        match [project.missing, project.strict]:
            case [True, False]:
                project, _ = _setup(project)
                name, *_ = report(project.target)
            case [False, _]:
                with t.suppress():  # pyright: ignore
                    project, env = _setup(project)
                    name, *_ = report(project.target)
                    project.name = underscorify(name)
                    project.license_file = 'LICENSE.txt'
                    project.copyright_head = valid_copyright_head(
                        project.copyright_head, name, project.license_file
                    )
                    rewriter = Rewriter(str(project.target), project.name, project.fix, env)
                    rewriter += project.add
                    rewriter -= project.remove
                    t.plan()
                if len(project.add) > 0 or len(project.remove) > 0:
                    print(
                        json.dumps(rewriter.commands, indent=4 if project.pretty else None)
                    )
                else:
                    parser.print_help()
            case [True, True]:
                with t.strict():  # pyright: ignore
                    project, _ = _setup(project)
                    name, *_ = report(project.target)
            case [_, _]:
                t.bail_out('Name discovery failed.')
    exit(0)
