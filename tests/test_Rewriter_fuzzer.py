# noqa: INP001
# ruff: noqa: S101; flake8: DC102
"""Unit and fuzz tests for ``ozi-fix`` utility script"""
# Part of ozi.
# See LICENSE.txt in the project root for details.
from __future__ import annotations

import argparse
import sys

from hypothesis import given
from hypothesis import strategies as st
from ozi_spec import METADATA
from ozi_templates import load_environment  # pyright: ignore

import ozi_core.fix.rewrite_command

try:
    import atheris
except ImportError:

    class Atheris:
        def instrument_func(self, func):  # noqa: ANN
            return func

    atheris = Atheris()

bad_namespace = argparse.Namespace(
    strict=False,
    verify_email=True,
    name='OZI-phony',
    keywords='foo,bar,baz',
    maintainer=[],
    maintainer_email=[],
    author=['foo'],
    author_email=['noreply@oziproject.dev'],
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
@atheris.instrument_func
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


if __name__ == '__main__':
    atheris.Setup(
        sys.argv, atheris.instrument_func(test_fuzz_Rewriter.hypothesis.fuzz_one_input)
    )
    atheris.Fuzz()
