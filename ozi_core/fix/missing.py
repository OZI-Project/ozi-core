# ozi/fix/missing.py
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
"""Find missing OZI project files."""
from __future__ import annotations

import re
import sys
from contextlib import suppress
from email import message_from_string
from pathlib import Path
from typing import TYPE_CHECKING

from ozi_spec import METADATA
from ozi_templates.filter import underscorify  # pyright: ignore
from tap_producer import TAP

from ozi_core._i18n import TRANSLATION
from ozi_core.fix.build_definition import walk
from ozi_core.meson import load_ast
from ozi_core.meson import project_metadata
from ozi_core.pkg_extra import parse_extra_pkg_info

if sys.version_info >= (3, 11):  # pragma: no cover
    import tomllib as toml
elif sys.version_info < (3, 11):  # pragma: no cover
    import tomli as toml

if TYPE_CHECKING:  # pragma: no cover
    from email.message import Message

PKG_INFO = """Metadata-Version: @METADATA_VERSION@
Name: @PROJECT_NAME@
Version: @SCM_VERSION@
License: @LICENSE@
@REQUIRED@
@REQUIREMENTS_IN@

@README_TEXT@
"""

readme_ext_to_content_type = {
    '.rst': 'text/x-rst',
    '.md': 'text/markdown',
    '.txt': 'text/plain',
    '': 'text/plain',
}


def get_relpath_expected_files(
    kind: str | None,
    name: str,
) -> tuple[Path, tuple[str, ...] | tuple[()]]:
    match kind:
        case 'test':
            rel_path = Path('tests')
            expected_files = METADATA.spec.python.src.required.test
        case 'root':
            rel_path = Path('.')
            expected_files = METADATA.spec.python.src.required.root
        case 'source':
            rel_path = Path(underscorify(name).lower())
            expected_files = METADATA.spec.python.src.required.source
        case _:  # pragma: no cover
            rel_path = Path('.')
            expected_files = ()
    return rel_path, expected_files


def render_requirements(target: Path) -> str:
    """Render requirements.in as it would appear in PKG-INFO"""
    try:
        requirements = (  # pragma: no cover
            r.partition('\u0023')[0]
            for r in filter(
                lambda r: not (r.startswith('\u0023') or r == '\n'),
                target.joinpath('requirements.in').read_text('utf-8').splitlines(),
            )
        )
    except FileNotFoundError:
        with target.joinpath('pyproject.toml').open('rb') as f:
            requirements = toml.load(f).get('project', {}).get('dependencies', [])
    return ''.join([f'Requires-Dist: {req}\n' for req in requirements])


def render_pkg_info(target: Path, name: str, _license: str) -> Message:  # noqa: C901
    """Render PKG-INFO as it would be produced during packaging."""
    with target.joinpath('pyproject.toml').open('rb') as f:
        pyproject = toml.load(f)
        setuptools_scm = pyproject.get('tool', {}).get('setuptools_scm', {})
        ozi_build = pyproject.get('tool', {}).get('ozi-build', {}).get('metadata', {})
        if setuptools_scm.get('version_file_template'):  # pragma: no cover
            TAP.ok('setuptools_scm', 'PKG-INFO', 'template')
            return message_from_string(
                setuptools_scm.get('version_file_template', '@README_TEXT@')
                .replace(
                    '@README_TEXT@',
                    target.joinpath('README').read_text(),
                )
                .replace('@PROJECT_NAME@', name)
                .replace('@LICENSE@', _license)
                .replace('@REQUIREMENTS_IN@\n', render_requirements(target))
                .replace('@SCM_VERSION@', '{version}'),
            )
        else:
            required = ''
            for key in ('home-page', 'summary', 'author', 'author-email', 'keywords'):
                val = ozi_build.get(key, None)
                if val is not None:  # pragma: no cover
                    required += f'{key.capitalize()}: {val}\n'
            for ext in ('.rst', '.txt', '.md'):
                readme = target.joinpath(f'README{ext}')
                if readme.exists():
                    required += (
                        f'Description-Content-Type: {readme_ext_to_content_type.get(ext)}\n'
                    )
            required += ''.join(
                [f'Classifier: {req}\n' for req in ozi_build.get('classifiers', [])],
            )
            msg = (
                PKG_INFO.replace('@LICENSE@', _license)
                .replace('@REQUIREMENTS_IN@', render_requirements(target).strip())
                .replace('@SCM_VERSION@', '{version}')
                .replace('@PROJECT_NAME@', name)
                .replace('@METADATA_VERSION@', METADATA.spec.python.support.metadata_version)
                .replace('@REQUIRED@', required.strip('\n'))
                .replace('@README_TEXT@', target.joinpath('README').read_text())
            )
            return message_from_string(msg)


def python_support(pkg_info: Message) -> set[tuple[str, str]]:
    """Check PKG-INFO Message for python support."""
    remaining_pkg_info = {
        (k, v)
        for k, v in pkg_info.items()
        if k not in METADATA.spec.python.pkg.info.required
    }
    for k, v in iter(METADATA.ozi.python_support.classifiers[:4]):
        if (k, v) in remaining_pkg_info:
            TAP.ok(k, v)
        else:
            TAP.not_ok(TRANSLATION('term-missing'), v)  # pragma: no cover
    return remaining_pkg_info


def required_extra_pkg_info(pkg_info: Message) -> dict[str, str]:
    """Check missing required OZI extra PKG-INFO"""
    remaining_pkg_info = python_support(pkg_info)
    remaining_pkg_info.difference_update(set(iter(METADATA.ozi.python_support.classifiers)))
    for k, v in iter(remaining_pkg_info):
        TAP.ok(k, v)
    extra_pkg_info, errstr = parse_extra_pkg_info(pkg_info)
    if errstr not in ('', None):
        TAP.not_ok(TRANSLATION('term-missing'), str(errstr))  # pragma: no cover
    for k, v in extra_pkg_info.items():
        TAP.ok(k, v)
    return extra_pkg_info


def required_pkg_info(
    target: Path,
) -> tuple[str, dict[str, str]]:
    """Find missing required PKG-INFO"""
    ast = load_ast(str(target))
    name = ''
    license_ = ''
    if ast:
        name, license_ = project_metadata(ast)
    pkg_info = render_pkg_info(target, name, license_)
    for i in METADATA.spec.python.pkg.info.required:
        v = pkg_info.get(i, None)
        if v is not None:
            TAP.ok(i, v)
        else:  # pragma: no cover
            TAP.not_ok(TRANSLATION('term-missing'), i)
    extra_pkg_info = required_extra_pkg_info(pkg_info)
    name = re.sub(r'[-_.]+', '-', pkg_info.get('Name', '')).lower()
    return name, extra_pkg_info


def required_files(
    kind: str,
    target: Path,
    name: str,
) -> list[str]:
    """Count missing files required by OZI"""
    found_files = []
    rel_path, expected_files = get_relpath_expected_files(kind, name)
    for file in expected_files:
        f = rel_path / file
        if not target.joinpath(f).exists():  # pragma: no cover
            TAP.not_ok(TRANSLATION('term-missing'), str(f))
            continue  # pragma: defer to https://github.com/nedbat/coveragepy/issues/198
        TAP.ok(str(f))
        found_files.append(file)
    with suppress(FileNotFoundError):
        list(
            walk(
                target,
                rel_path,
                found_files=found_files,
                project_name=underscorify(name).lower(),
            ),
        )
    return found_files


def report(
    target: Path,
) -> tuple[str, Message | None, list[str], list[str], list[str]]:
    """Report missing OZI project files
    :param target: Relative path to target directory.
    :return: Normalized Name, PKG-INFO, found_root, found_sources, found_tests
    """
    target = Path(target)
    name = None
    pkg_info = None
    extra_pkg_info: dict[str, str] = {}
    try:
        name, extra_pkg_info = required_pkg_info(target)
    except FileNotFoundError:
        name = ''
        TAP.not_ok(TRANSLATION('term-missing'), TRANSLATION('term-required-metadata'))
    found_source_files = required_files(
        'source',
        target,
        name,
    )
    found_test_files = required_files(
        'test',
        target,
        name,
    )
    found_root_files = required_files(
        'root',
        target,
        name,
    )
    all_files = (  # pragma: defer to TAP-Consumer
        ['PKG-INFO'],
        extra_pkg_info,
        found_root_files,
        found_source_files,
        found_test_files,
    )
    try:  # pragma: defer to TAP-Consumer
        sum(map(len, all_files))
    except TypeError:  # pragma: defer to TAP-Consumer
        TAP.bail_out(TRANSLATION('term-missing'))
    return (  # pragma: defer to TAP-Consumer
        name,
        pkg_info,
        found_root_files,
        found_source_files,
        found_test_files,
    )
