# noqa: INP001
from __future__ import annotations

import argparse
import sys
import typing
import warnings
from datetime import timedelta

from hypothesis import given
from hypothesis import settings
from hypothesis import strategies as st

try:
    import atheris
except ImportError:

    class Atheris:
        def instrument_func(self, func):  # noqa: ANN
            return func

    atheris = Atheris()

if sys.version_info < (3, 11):
    warnings.filterwarnings('ignore', category=FutureWarning)
    import ozi_core.actions

    warnings.filterwarnings('default')
else:
    import ozi_core.actions


@settings(deadline=timedelta(milliseconds=1000))
@given(
    option_strings=st.one_of(
        st.just('--license'),
        st.just('--environment'),
        st.just('--framework'),
        st.just('--license-id'),
        st.just('--license-exception-id'),
        st.just('--audience'),
        st.just('--language'),
        st.just('--topic'),
        st.just('--status'),
    ),
    dest=st.text(min_size=1, max_size=20),
    nargs=st.one_of(st.just('?')),
    data=st.data(),
)
@atheris.instrument_func
def test_fuzz_CloseMatch_nargs_append(  # noqa: N802, DC102, RUF100
    option_strings: str,
    dest: str,
    nargs: int | str | None,
    data: typing.Any,
) -> None:
    close_match = ozi_core.actions.CloseMatch(
        option_strings=[option_strings],
        dest=dest,
        nargs=nargs,
    )
    data = data.draw(
        st.sampled_from(
            ozi_core.actions.ExactMatch().__getattribute__(
                option_strings.lstrip('-').replace('-', '_'),
            ),
        ),
    )
    close_match(argparse.ArgumentParser(), argparse.Namespace(), [data], option_strings)


if __name__ == '__main__':
    atheris.Setup(
        sys.argv,
        atheris.instrument_func(test_fuzz_CloseMatch_nargs_append.hypothesis.fuzz_one_input),
    )
    atheris.Fuzz()
