# ozi/actions.py
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
"""Parsing actions for the OZI commandline interface."""
from __future__ import annotations

import json
import sys
from argparse import Action
from dataclasses import dataclass
from difflib import get_close_matches
from glob import glob
from pathlib import Path
from typing import TYPE_CHECKING
from typing import Any
from typing import Collection
from typing import NoReturn
from warnings import warn

import niquests  # pyright: ignore
from ozi_spec import METADATA
from ozi_spec import OZI
from ozi_spec import Metadata
from packaging.version import Version
from packaging.version import parse
from pyparsing import ParseException
from spdx_license_list import LICENSES
from tap_producer import TAP

from ozi_core._i18n import TRANSLATION
from ozi_core._logging import LOG_PATH
from ozi_core.config import CONF_PATH
from ozi_core.spdx import spdx_license_expression
from ozi_core.trove import Prefix
from ozi_core.trove import from_prefix

if TYPE_CHECKING:  # pragma: no cover
    from argparse import ArgumentParser
    from argparse import Namespace
    from collections.abc import Sequence

_prefix = Prefix()


@dataclass
class ExactMatch:
    """Exact matches data for packaging core metadata."""

    audience: tuple[str, ...] = from_prefix(_prefix.audience)
    language: tuple[str, ...] = from_prefix(_prefix.language)
    framework: tuple[str, ...] = from_prefix(_prefix.framework)
    environment: tuple[str, ...] = from_prefix(_prefix.environment)
    license: tuple[str, ...] = from_prefix(_prefix.license)
    license_id: tuple[str, ...] = tuple(
        k for k, v in LICENSES.items() if v.deprecated_id is False
    )
    license_exception_id: tuple[str, ...] = tuple(
        METADATA.spec.python.pkg.license.exceptions.keys()
    )
    status: tuple[str, ...] = from_prefix(_prefix.status)
    topic: tuple[str, ...] = from_prefix(_prefix.topic)


class CloseMatch(Action):
    """Special argparse choices action. Warn the user if a close match could not be found."""

    exact_match = ExactMatch()

    def __init__(
        self: CloseMatch,  # pyright: ignore
        option_strings: list[str],
        dest: str,
        nargs: int | str | None = None,
        **kwargs: Any,
    ) -> None:
        """Argparse init"""
        if nargs not in [None, '?']:
            text = 'nargs (other than "?") not allowed'
            raise ValueError(text)

        super().__init__(option_strings, dest, nargs=nargs, **kwargs)

    def close_matches(
        self: CloseMatch,
        key: str,
        value: str,
    ) -> Sequence[str]:
        """Get a close matches for a Python project packaging core metadata key.

        :param key: Python project packaging core metadata key name (normalized)
        :type key: str
        :param value: the value to query a close match for
        :type value: Sequence[str]
        :return: sequence with the best match or an empty sequence
        :rtype: Sequence[str]
        """
        if value is None:
            return []  # pragma: defer to good-first-issue
        no_match = False
        matches: list[str] | str = []
        if hasattr(self.exact_match, key):
            matches = get_close_matches(
                value,
                getattr(self.exact_match, key),
                cutoff=0.40,
            )
            no_match = False if len(matches) else True
        else:  # pragma: no cover
            matches = [value]
            no_match = True
        if no_match:  # pragma: no cover
            warn(
                TRANSLATION('err-no-close-match', key=key, value=value)
                + f'$ ozi-new -l {key}',
                RuntimeWarning,
                stacklevel=0,
            )
        return matches

    def _set_matches(
        self: CloseMatch,
        key: str,
        values: str | Sequence[str],
        namespace: Namespace,
    ) -> None:
        """Set the matches for a key in namespace."""
        match self.nargs:
            case '?':
                setattr(namespace, self.dest, [self.close_matches(key, v) for v in values])
            case _:
                setattr(
                    namespace,
                    self.dest,
                    self.close_matches(
                        key,
                        values if isinstance(values, str) else values[0],
                    ),
                )

    def __call__(
        self: CloseMatch,
        parser: ArgumentParser,
        namespace: Namespace,
        values: str | Sequence[str] | None,
        option_string: str | None = None,
    ) -> None:
        """Find closest matching class attribute."""
        if values is None:  # pragma: no cover
            return
        if option_string is not None:
            key = option_string.lstrip('-').replace('-', '_')
        else:
            key = ''  # pragma: defer to good-first-issue
        self._set_matches(key, values, namespace)


def check_for_update(
    current_version: Version,
    releases: Collection[Version],
) -> None:  # pragma: defer to python
    """Issue a warning if installed version of OZI is not up to date."""
    match max(releases):
        case latest if latest > current_version:
            TAP.not_ok(
                TRANSLATION(
                    'err-new-version',
                    latest=str(latest),
                    currentversion=str(current_version),
                ),
                'https://pypi.org/project/OZI/',
            )
        case latest if latest < current_version:
            TAP.ok(TRANSLATION('term-tap-dev-version'), str(current_version))
        case latest if latest == current_version:
            TAP.ok(TRANSLATION('term-tap-up-to-date'), str(current_version))


def check_version(version: str) -> NoReturn:  # pragma: defer to PyPI
    """Check for a newer version of OZI and exit."""
    response = niquests.get('https://pypi.org/pypi/OZI/json', timeout=30)
    match response.status_code:
        case 200:
            check_for_update(
                current_version=parse(version),
                releases=set(map(parse, response.json()['releases'].keys())),
            )
            TAP.end()
        case _:
            TAP.end(
                skip_reason=TRANSLATION(
                    'version-check-failed',
                    status=str(response.status_code),
                ),
            )
    exit(0)


def info(version: str) -> NoReturn:  # pragma: no cover
    """Print all metadata as JSON and exit."""
    sys.exit(print(json.dumps(Metadata(OZI(version)).asdict(), indent=2)))


def list_available(key: str) -> NoReturn:  # pragma: no cover
    """Print a list of valid values for a key and exit."""
    sys.exit(print(*sorted(getattr(ExactMatch, key.replace('-', '_'))), sep='\n'))


def license_expression(expr: str) -> NoReturn:  # pragma: no cover
    """Validate a SPDX license expression."""
    try:
        spdx_license_expression.parse_string(expr, parse_all=True)
        TAP.ok(expr, TRANSLATION('term-parsing-success'))
    except ParseException as e:
        TAP.not_ok(expr, str(e))
    TAP.end()
    exit(0)


def uninstall_user_files() -> NoReturn:  # noqa: C901  # pragma: defer to E2E
    """Remove configuration and log files created by OZI."""
    TAP.ok(f'remove {CONF_PATH} if it exists')
    CONF_PATH.unlink(missing_ok=True)
    TAP.ok(f'remove {LOG_PATH} if it exists')
    LOG_PATH.unlink(missing_ok=True)
    for i in glob(f'{LOG_PATH}.*'):
        TAP.ok(f'remove {i}')
        Path(i).unlink()
    try:
        CONF_PATH.parent.rmdir()
        TAP.ok(f'remove {CONF_PATH.parent} directory')
    except OSError as e:
        TAP.not_ok(str(e))
    try:
        LOG_PATH.parent.rmdir()
        TAP.ok(f'remove {LOG_PATH.parent} directory')
        TAP.ok(f'remove {LOG_PATH.parent.parent} directory')
    except OSError as e:
        TAP.not_ok(str(e))
    TAP.end()
    exit(0)
