# noqa: INP001
# ruff: noqa: S101; flake8: DC102
"""Unit and fuzz tests for ``ozi-fix`` utility script"""
# Part of ozi.
# See LICENSE.txt in the project root for details.
from __future__ import annotations

import argparse
import difflib
import os
import pathlib
from copy import deepcopy
from datetime import timedelta

import pytest
from hypothesis import given
from hypothesis import settings
from hypothesis import strategies as st
from ozi_spec import METADATA  # pyright: ignore
from ozi_templates import load_environment  # pyright: ignore

import ozi_core.fix.missing  # pyright: ignore
import ozi_core.fix.rewrite_command  # pyright: ignore
import ozi_core.pkg_extra  # pyright: ignore
import ozi_core.render  # pyright: ignore
from ozi_core.fix.build_definition import unrollable_subdirs  # pyright: ignore

required_pkg_info_patterns = (
    'Author',
    'Author-email',
    'Description-Content-Type',
    'Home-page',
    'License',
    'License-Expression',
    'License-File',
    'Metadata-Version',
    'Name',
    'Programming Language :: Python',
    'Summary',
    'Version',
)

SAMPLE_MESON_BUILD = """# ozi/meson.build
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
custom_target(
    '_locales.py',
    input: 'generate_locales.py',
    output: '_locales.py',
    command: [python, '@INPUT@'],
    build_by_default: true,
    install: true,
    install_dir: python.get_install_dir() / 'ozi_core',
)
source_files = [
  '__init__.py',
  '__init__.pyi',
  '_i18n.py',
  '_i18n.pyi',
  '_locales.pyi',
  'actions.py',
  'actions.pyi',
  'comment.py',
  'comment.pyi',
  'generate_locales.py',
  'generate_locales.pyi',
  'meson.py',
  'meson.pyi',
  'pkg_extra.py',
  'pkg_extra.pyi',
  'py.typed',
  'render.py',
  'render.pyi',
  'spdx.py',
  'spdx.pyi',
  'trove.py',
  'trove.pyi'
]
foreach file : files(source_files)
    fs.copyfile(file)
    if not meson.is_subproject() or get_option('install-subprojects').enabled()
        python.install_sources(file, pure: true, subdir: 'ozi_core')
    endif
endforeach
source_children = [
    'data',
    'vendor',
    'fix',
    'new',
    'ui',
]
foreach child: source_children
    if child != 'ozi.phony'
        subdir(child)
    endif
endforeach
if false
    executable('source_files', source_files)
    executable('ext_files', ext_files)
    executable('source_children', source_children)
endif
foo_children = []
foreach child: foo_children
    if child != 'ozi.phony'
        subdir(child)
    endif
endforeach
"""

bad_namespace = argparse.Namespace(
    strict=False,
    verify_email=True,
    name='OZI-phony',
    keywords='foo,bar,baz',
    maintainer=[],
    maintainer_email=[],
    author=['foo'],
    author_email=['noreply@oziproject.dev'],
    home_page='https://oziproject.dev',
    summary='A' * 512,
    copyright_head='',
    license_expression='CC0-1.0',
    license_file='LICENSE.txt',
    license='CC0 1.0 Universal (CC0 1.0) Public Domain Dedication',
    license_id='ITWASAFICTION',
    license_exception_id='WEMADEITUP',
    topic=['Utilities'],
    status=['7 - Inactive'],
    environment=['Other Environment'],
    framework=['Pytest'],
    audience=['Other Audience'],
    ci_provider='github',
    project_url=['Home, https://oziproject.dev'],
    long_description_content_type='md',
    fix='',
    add=['ozi.phony'],
    remove=['ozi.phony'],
    dist_requires=[],
    allow_file=[],
    missing=True,
)

env = load_environment(vars(bad_namespace), METADATA.asdict())


@pytest.fixture
def bad_project(tmp_path_factory: pytest.TempPathFactory) -> pathlib.Path:
    """Fixture to wrap the ``ozi-new project`` functionality."""
    fn = tmp_path_factory.mktemp('project_')
    namespace = deepcopy(bad_namespace)
    namespace.target = fn
    preprocessed = ozi_core.new.validate.preprocess_arguments(namespace)
    postprocessed = ozi_core.new.validate.postprocess_arguments(preprocessed)
    ozi_core.render.RenderedContent(
        load_environment(vars(postprocessed), METADATA.asdict()),
        postprocessed.target,
        postprocessed.name,
        postprocessed.ci_provider,
        postprocessed.long_description_content_type,
    ).render()
    return fn


@pytest.mark.parametrize(
    'key',
    [i for i in METADATA.spec.python.src.required.root if i not in ['PKG-INFO']],
)
def test_report_missing_required_root_file(
    bad_project: pathlib.Path,
    key: str,
) -> None:
    """Check that we warn on missing files."""
    os.remove(bad_project.joinpath(key))
    with pytest.raises(RuntimeWarning):
        ozi_core.fix.missing.report(bad_project)


@pytest.mark.parametrize('key', METADATA.spec.python.src.required.test)
def test_report_missing_required_test_file(bad_project: pathlib.Path, key: str) -> None:
    """Check that we warn on missing files."""
    os.remove(bad_project.joinpath('tests') / key)
    with pytest.raises(RuntimeWarning):
        ozi_core.fix.missing.report(bad_project)


@pytest.mark.parametrize('key', METADATA.spec.python.src.required.source)
def test_report_missing_required_source_file(bad_project: pathlib.Path, key: str) -> None:
    """Check that we warn on missing files."""
    os.remove(bad_project.joinpath('ozi_phony') / key)
    with pytest.raises(RuntimeWarning):
        ozi_core.fix.missing.report(bad_project)


@given(
    type=st.just('target'),
    target=st.text(min_size=1, max_size=20),
    operation=st.text(min_size=1, max_size=20),
    sources=st.lists(st.text(min_size=1, max_size=20)),
    subdir=st.just(''),
    target_type=st.just('executable'),
)
def test_fuzz_RewriteCommand(  # noqa: N802, DC102, RUF100
    type: str,  # noqa: A002
    target: str,
    operation: str,
    sources: list[str],
    subdir: str,
    target_type: str,
) -> None:
    ozi_core.fix.rewrite_command.RewriteCommand(
        type=type,
        target=target,
        operation=operation,
        sources=sources,
        subdir=subdir,
        target_type=target_type,
    )


@given(
    target=st.just('.'),
    name=st.text(min_size=1, max_size=20),
    fix=st.sampled_from(('test', 'source', 'root')),
    commands=st.lists(
        st.dictionaries(
            keys=st.text(min_size=1, max_size=20),
            values=st.text(min_size=1, max_size=20),
        ),
    ),
)
def test_fuzz_Rewriter(  # noqa: N802, DC102, RUF100
    target: str,
    name: str,
    fix: str,
    commands: list[dict[str, str]],
) -> None:
    ozi_core.fix.rewrite_command.Rewriter(
        target=target,
        name=name,
        fix=fix,
        commands=commands,
        env=env,
    )


@pytest.mark.parametrize('fix', ['test', 'root', 'source'])
def test_Rewriter_bad_project__iadd__dir_nested_warns(  # noqa: N802, DC102, RUF100
    bad_project: pytest.FixtureRequest,
    fix: str,
) -> None:
    rewriter = ozi_core.fix.rewrite_command.Rewriter(
        target=str(bad_project),
        name='ozi_phony',
        fix=fix,
        env=env,
    )
    with pytest.warns(RuntimeWarning):
        rewriter += ['foo/foo/baz/']


@pytest.mark.parametrize('fix', ['test', 'root', 'source'])
def test_Rewriter_bad_project__iadd__dir(  # noqa: N802, DC102, RUF100
    bad_project: pytest.FixtureRequest,
    fix: str,
) -> None:
    rewriter = ozi_core.fix.rewrite_command.Rewriter(
        target=str(bad_project),
        name='ozi_phony',
        fix=fix,
        env=env,
    )
    rewriter += ['foo/']
    assert len(rewriter.commands) == 1


def test_Rewriter_bad_project__iadd__bad_fix(  # noqa: N802, DC102, RUF100
    bad_project: pytest.FixtureRequest,
) -> None:
    rewriter = ozi_core.fix.rewrite_command.Rewriter(
        target=str(bad_project),
        name='ozi_phony',
        fix='',
        env=env,
    )
    with pytest.warns(RuntimeWarning):
        rewriter += ['foo/']
    assert len(rewriter.commands) == 0


def test_Rewriter_bad_project__isub__bad_fix(  # noqa: N802, DC102, RUF100
    bad_project: pytest.FixtureRequest,
) -> None:
    rewriter = ozi_core.fix.rewrite_command.Rewriter(
        target=str(bad_project),
        name='ozi_phony',
        fix='',
        env=env,
    )
    rewriter -= ['foo.py']
    assert len(rewriter.commands) == 1


@pytest.mark.parametrize('fix', ['test', 'root', 'source'])
def test_Rewriter_bad_project__isub__non_existing_child(  # noqa: N802, DC102, RUF100
    bad_project: pytest.FixtureRequest,
    fix: str,
) -> None:
    rewriter = ozi_core.fix.rewrite_command.Rewriter(
        target=str(bad_project),
        name='ozi_phony',
        fix=fix,
        env=env,
    )
    with pytest.raises(RuntimeWarning):
        rewriter -= ['foo/']
    assert len(rewriter.commands) == 0


@pytest.mark.parametrize('fix', ['test', 'root', 'source'])
def test_Rewriter_bad_project__isub__child(  # noqa: N802, DC102, RUF100
    bad_project: pytest.FixtureRequest,
    fix: str,
) -> None:
    rewriter = ozi_core.fix.rewrite_command.Rewriter(
        target=str(bad_project),
        name='ozi_phony',
        fix=fix,
        env=env,
    )
    if fix == 'root':
        pathlib.Path(str(bad_project), 'foo').mkdir()
    elif fix == 'source':
        pathlib.Path(str(bad_project), 'ozi_phony', 'foo').mkdir()
    elif fix == 'test':
        pathlib.Path(str(bad_project), 'tests', 'foo').mkdir()
    rewriter -= ['foo/']
    assert len(rewriter.commands) == 1


@pytest.mark.parametrize('fix', ['test', 'root', 'source'])
def test_Rewriter_bad_project__isub__python_file(  # noqa: N802, DC102, RUF100
    bad_project: pytest.FixtureRequest,
    fix: str,
) -> None:
    rewriter = ozi_core.fix.rewrite_command.Rewriter(
        target=str(bad_project),
        name='ozi_phony',
        fix=fix,
        env=env,
    )
    if fix == 'root':
        pathlib.Path(str(bad_project), 'foo.py').touch()
    elif fix == 'source':
        pathlib.Path(str(bad_project), 'ozi_phony', 'foo.py').touch()
    elif fix == 'test':
        pathlib.Path(str(bad_project), 'tests', 'foo.py').touch()
    rewriter -= ['foo.py']
    assert len(rewriter.commands) == 1


@pytest.mark.parametrize('fix', ['test', 'root', 'source'])
def test_Rewriter_bad_project__isub__file(  # noqa: N802, DC102, RUF100
    bad_project: pytest.FixtureRequest,
    fix: str,
) -> None:
    rewriter = ozi_core.fix.rewrite_command.Rewriter(
        target=str(bad_project),
        name='ozi_phony',
        fix=fix,
        env=env,
    )
    if fix == 'root':
        pathlib.Path(str(bad_project), 'foo').touch()
    elif fix == 'source':
        pathlib.Path(str(bad_project), 'ozi_phony', 'foo').touch()
    elif fix == 'test':
        pathlib.Path(str(bad_project), 'tests', 'foo').touch()
    rewriter -= ['foo']
    assert len(rewriter.commands) == 1


@pytest.mark.parametrize('fix', ['test', 'root', 'source'])
def test_Rewriter_bad_project__iadd__file(  # noqa: N802, DC102, RUF100
    bad_project: pytest.FixtureRequest,
    fix: str,
) -> None:
    rewriter = ozi_core.fix.rewrite_command.Rewriter(
        target=str(bad_project),
        name='ozi_phony',
        fix=fix,
        env=env,
    )
    rewriter += ['foo.py']
    assert len(rewriter.commands) == 1


@pytest.mark.parametrize('fix', ['test', 'root', 'source'])
def test_Rewriter_bad_project__iadd__file_from_template(  # noqa: N802, DC102, RUF100
    bad_project: pytest.FixtureRequest | pathlib.Path,
    fix: str,
) -> None:
    rewriter = ozi_core.fix.rewrite_command.Rewriter(
        target=str(bad_project),
        name='ozi_phony',
        fix=fix,
        env=env,
    )
    pathlib.Path(bad_project / 'templates' / 'foo.py').touch()  # pyright: ignore
    pathlib.Path(bad_project / 'templates' / 'source').mkdir()  # pyright: ignore
    pathlib.Path(bad_project / 'templates' / 'source' / 'foo.py').touch()  # pyright: ignore
    pathlib.Path(bad_project / 'templates' / 'test').mkdir()  # pyright: ignore
    pathlib.Path(bad_project / 'templates' / 'test' / 'foo.py').touch()  # pyright: ignore
    rewriter += ['foo.py']
    assert len(rewriter.commands) == 1


@pytest.mark.parametrize('fix', ['test', 'root', 'source'])
def test_Rewriter_bad_project__iadd__non_python_file(  # noqa: N802, DC102, RUF100
    bad_project: pytest.FixtureRequest,
    fix: str,
) -> None:
    rewriter = ozi_core.fix.rewrite_command.Rewriter(
        target=str(bad_project),
        name='ozi_phony',
        fix=fix,
        env=env,
    )
    with pytest.warns(RuntimeWarning):
        rewriter += ['foo']
    assert len(rewriter.commands) == 1


header = """.. OZI
  Classifier: License-Expression :: Apache-2.0 WITH LLVM-exception
  Classifier: License-File :: LICENSE.txt
"""


@settings(deadline=timedelta(milliseconds=1000))
@given(payload=st.text(max_size=65535).map(header.__add__), as_message=st.booleans())
def test_fuzz_pkg_info_extra(payload: str, as_message: bool) -> None:  # noqa: DC102, RUF100
    ozi_core.pkg_extra._pkg_info_extra(
        payload=payload,
        as_message=as_message,
    )


def test_meson_unroll_subdirs() -> None:
    x = unrollable_subdirs.parse_string(SAMPLE_MESON_BUILD)
    y = '\n'.join([i.rstrip('\n') for i in x])
    assert "\nfoo_children = ['ozi.phony']\n" in y
    assert "\nsource_children = ['ozi.phony']\nforeach" in y
    assert "\nsubdir('data')\n" in y
    assert "\nsubdir('vendor')\n" in y
    assert "\nsubdir('fix')\n" in y
    assert "\nsubdir('new')\n" in y
    assert "\nsubdir('ui')\n" in y
    assert y != SAMPLE_MESON_BUILD
    z = '\n'.join([i.rstrip('\n') for i in unrollable_subdirs.parse_string(y)])
    assert y == z
    assert ''.join(difflib.context_diff(SAMPLE_MESON_BUILD, y)) == ''.join(
        difflib.context_diff(SAMPLE_MESON_BUILD, z),
    )
