# noqa: INP001
from __future__ import annotations

import argparse
import typing
from datetime import timedelta

import pytest
from hypothesis import given
from hypothesis import settings
from hypothesis import strategies as st

import ozi_core.actions


@settings(deadline=timedelta(milliseconds=500))
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
    nargs=st.one_of(st.none()),
    data=st.data(),
)
def test_fuzz_CloseMatch_nargs_None(  # noqa: N802, DC102, RUF100
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
    close_match(argparse.ArgumentParser(), argparse.Namespace(), data, option_strings)


@settings(deadline=timedelta(milliseconds=500))
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
    data=st.none(),
)
def test_fuzz_CloseMatch_nargs_append_None_values(  # noqa: N802, DC102, RUF100
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
    close_match(argparse.ArgumentParser(), argparse.Namespace(), data, option_strings)


@settings(deadline=timedelta(milliseconds=500))
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
    data=st.text(min_size=10, max_size=80),
)
def test_fuzz_CloseMatch_nargs_append_warns(  # noqa: N802, DC102, RUF100
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
    with pytest.warns(RuntimeWarning):
        close_match(argparse.ArgumentParser(), argparse.Namespace(), [data], option_strings)


@settings(deadline=timedelta(milliseconds=500))
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
    nargs=st.one_of(st.just('*')),
    data=st.text(min_size=10, max_size=80),
)
def test_fuzz_CloseMatch_nargs_invalid(  # noqa: N802, DC102, RUF100
    option_strings: str,
    dest: str,
    nargs: int | str | None,
    data: typing.Any,
) -> None:
    with pytest.raises(ValueError, match='nargs'):
        ozi_core.actions.CloseMatch(option_strings=[option_strings], dest=dest, nargs=nargs)
