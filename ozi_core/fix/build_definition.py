# ozi/fix/build_definition.py
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
"""Build definition check utilities."""
from __future__ import annotations

import os
from pathlib import Path
from typing import Generator

from ozi_spec import METADATA
from pyparsing import Combine
from pyparsing import DelimitedList
from pyparsing import FollowedBy
from pyparsing import Keyword
from pyparsing import LineEnd
from pyparsing import Literal
from pyparsing import OneOrMore
from pyparsing import Optional
from pyparsing import SkipTo
from pyparsing import StringEnd
from pyparsing import White
from pyparsing import Word
from pyparsing import ZeroOrMore
from pyparsing import alphanums
from pyparsing import alphas
from pyparsing import match_previous_literal
from pyparsing import quoted_string
from pyparsing import rest_of_line
from tap_producer import TAP

from ozi_core import comment
from ozi_core._i18n import TRANSLATION
from ozi_core.meson import get_items_by_suffix
from ozi_core.meson import query_build_value

IGNORE_MISSING = {
    'subprojects',
    *METADATA.spec.python.src.repo.hidden_dirs,
    *METADATA.spec.python.src.repo.ignore_dirs,
    *METADATA.spec.python.src.allow_files,
}
_commasepitem = (
    Combine(
        OneOrMore(
            ~Literal(',')
            + ~LineEnd()
            + quoted_string
            + Optional(White(' \t') + ~FollowedBy(LineEnd() | ',')),
        ),
    )
    .streamline()
    .set_name('commaItem')
)
comma_separated_list = DelimitedList(
    Optional(quoted_string.copy() | _commasepitem, default=''),
).set_name('comma separated list')
SP = White(' ', min=1)
NL = White('\n', min=1)
bound = Word(alphas, alphanums + '_')
assigned = Word(alphas, alphanums + '_')
array_assign = (
    assigned
    + Literal('=')
    + Literal('[')
    + Optional(comma_separated_list, default='')
    + Literal(']')
    + rest_of_line
).set_parse_action(
    lambda t: [
        *[f'subdir({i})' for i in t[3:-2] if len(i) and i.strip('\'"') != 'ozi.phony'],
        ' '.join(t[:3]) + "'ozi.phony'" + t[-2] + t[-1],  # type: ignore
    ],
)
foreach_bind = (
    Keyword('foreach') + bound + ':' + match_previous_literal(assigned) + rest_of_line
).set_parse_action(lambda t: ' '.join(t).strip())
bindvar = match_previous_literal(bound)
foreach_end = (Keyword('endforeach') + rest_of_line).set_parse_action(
    lambda t: ' '.join(t).strip(),
)
if_ozi_phony = (
    Keyword('if') + bindvar + Literal('!=') + Literal("'ozi.phony'") + rest_of_line
).set_parse_action(lambda t: '    ' + ' '.join(t).strip())
endif = (Keyword('endif') + rest_of_line).set_parse_action(
    lambda t: '    ' + ' '.join(t).strip(),
)
subdir_call = ('subdir(' + bindvar + ')' + rest_of_line).set_parse_action(
    lambda t: '        ' + ''.join(t),
)
literal_subdir_loop = (
    array_assign + foreach_bind + if_ozi_phony + subdir_call + endif + foreach_end
)
unrollable_subdirs = (
    ZeroOrMore(SkipTo(literal_subdir_loop, include=True))
    + SkipTo(StringEnd(), include=True).leave_whitespace()
)


def unroll_subdirs(target: Path, rel_path: Path) -> str:  # pragma: defer to E2E
    """Opens a meson.build file and returns the file with literal subdir loops converted
    to single static assignment form.
    """
    with open(target / rel_path / 'meson.build', 'r') as f:
        text = unrollable_subdirs.parse_file(f)
    return '\n'.join([i.strip('\n') for i in text])


def inspect_files(
    target: Path,
    rel_path: Path,
    found_files: list[str],
    extra_files: list[str],
) -> dict[str, list[str]]:  # pragma: no cover
    build_files = [str(rel_path / 'meson.build'), str(rel_path / 'meson.options')]
    _found_files = {'found': [], 'missing': []}
    for file in extra_files:
        found_literal = query_build_value(
            str(target / rel_path),
            file,
        )
        if found_literal and file not in _found_files:
            build_file = str((rel_path / file).parent / 'meson.build')
            TAP.ok(f'{build_file} {TRANSLATION("term-found")} {rel_path / file}')
            build_files += [str(rel_path / file)]
            comment.comment_diagnostic(target, rel_path, file)
            _found_files['found'].append(file)
        if str(rel_path / file) not in build_files and file not in found_files:
            build_file = str(rel_path / 'meson.build')
            TAP.not_ok(f'{build_file} {TRANSLATION("term-missing")} {rel_path / file}')
            _found_files['missing'].append(file)
    return _found_files


def process(
    target: Path,
    rel_path: Path,
    found_files: list[str] | None = None,
) -> dict[str, list[str]]:  # pragma: no cover
    """Process an OZI project build definition's files."""
    try:
        extra_files = [
            file
            for file in os.listdir(target / rel_path)
            if os.path.isfile(target / rel_path / file)
            and not os.path.islink(target / rel_path / file)
        ]
    except FileNotFoundError as e:
        TAP.not_ok(TRANSLATION('term-missing'), e.filename)
        extra_files = []
    found_files = found_files if found_files else []
    extra_files = list(set(extra_files).symmetric_difference(set(found_files)))
    files = inspect_files(
        target=target,
        rel_path=rel_path,
        found_files=found_files,
        extra_files=extra_files,
    )
    return files


def validate(
    target: Path,
    rel_path: Path,
    subdirs: list[str],
    children: set[str] | None,
) -> Generator[Path, None, None]:  # pragma: no cover
    """Validate an OZI standard build definition's directories."""
    for directory in subdirs:
        if directory not in IGNORE_MISSING:
            TAP.ok(
                str(rel_path / 'meson.build'),
                TRANSLATION('term-subdir'),
                str(directory),
            )
            yield Path(rel_path / directory)
        else:
            TAP.ok(
                str(rel_path / 'meson.build'),
                TRANSLATION('term-missing'),
                str(directory),
                skip=True,
            )


def walk(
    target: Path,
    rel_path: Path,
    found_files: list[str] | None = None,
    project_name: str | None = None,
) -> Generator[dict[Path, dict[str, list[str]]], None, None]:  # pragma: no cover
    """Walk an OZI standard build definition directory."""
    files = process(target, rel_path, found_files)
    yield {rel_path: files}
    found_files = files['found'] + files['missing']
    children = list(
        validate(
            target,
            rel_path,
            subdirs=[
                directory
                for directory in os.listdir(target / rel_path)
                if os.path.isdir(target / rel_path / directory)
                and directory not in [project_name, 'tests']
                and rel_path != Path('.')
            ],
            children=get_items_by_suffix(str((target / rel_path)), 'children'),
        ),
    )
    if rel_path == Path('.') and project_name:
        children += [Path('.')]  # pragma: no cover
    for child in children:
        walk(target, child, found_files=found_files)  # pragma: no cover
