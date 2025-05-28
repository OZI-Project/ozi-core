# noqa: INP001
# ruff: noqa: S101; flake8: DC102
"""Unit and fuzz tests for ``ozi-fix`` utility script"""
# Part of ozi.
# See LICENSE.txt in the project root for details.
from __future__ import annotations

import sys
from datetime import timedelta

from hypothesis import given
from hypothesis import settings
from hypothesis import strategies as st

import ozi_core.pkg_extra

try:
    import atheris
except ImportError:

    class Atheris:
        def instrument_func(self, func):  # noqa: ANN
            return func

    atheris = Atheris()


header = """.. OZI
  Classifier: License-Expression :: Apache-2.0 WITH LLVM-exception
  Classifier: License-File :: LICENSE.txt
"""


@settings(deadline=timedelta(milliseconds=1000))
@given(payload=st.text(max_size=65535).map(header.__add__), as_message=st.booleans())
@atheris.instrument_func
def test_fuzz_pkg_info_extra(payload: str, as_message: bool) -> None:  # noqa: DC102, RUF100
    ozi_core.pkg_extra._pkg_info_extra(
        payload=payload,
        as_message=as_message,
    )


if __name__ == '__main__':
    atheris.Setup(
        sys.argv, atheris.instrument_func(test_fuzz_pkg_info_extra.hypothesis.fuzz_one_input)
    )
    atheris.Fuzz()
