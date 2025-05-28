# noqa: INP001
# ruff: noqa: S101; flake8: DC102
"""Unit and fuzz tests for ``ozi-fix`` utility script"""
# Part of ozi.
# See LICENSE.txt in the project root for details.
from __future__ import annotations

import sys

from hypothesis import given
from hypothesis import strategies as st

import ozi_core.fix.rewrite_command  # pyright: ignore

try:
    import atheris
except ImportError:

    class Atheris:
        def instrument_func(self, func):  # noqa: ANN
            return func

    atheris = Atheris()


@given(
    type=st.just('target'),
    target=st.text(min_size=1, max_size=20),
    operation=st.text(min_size=1, max_size=20),
    sources=st.lists(st.text(min_size=1, max_size=20)),
    subdir=st.just(''),
    target_type=st.just('executable'),
)
@atheris.instrument_func
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


if __name__ == '__main__':
    atheris.Setup(
        sys.argv, atheris.instrument_func(test_fuzz_RewriteCommand.hypothesis.fuzz_one_input)
    )
    atheris.Fuzz()
