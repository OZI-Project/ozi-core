# ozi/__main__.py
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
"""``ozi`` console application."""  # pragma: no cover
from __future__ import annotations  # pragma: no cover

import argparse  # pragma: no cover
import sys  # pragma: no cover
from dataclasses import fields  # pragma: no cover

from ozi_core._i18n import TRANSLATION as _  # pragma: no cover  # pyright: ignore
from ozi_core.actions import ExactMatch  # pragma: no cover  # pyright: ignore
from ozi_core.actions import check_version  # pragma: no cover  # pyright: ignore
from ozi_core.actions import info  # pragma: no cover  # pyright: ignore
from ozi_core.actions import license_expression  # pragma: no cover  # pyright: ignore
from ozi_core.actions import list_available  # pragma: no cover  # pyright: ignore
from ozi_core.actions import uninstall_user_files  # pragma: no cover  # pyright: ignore

_CHOICES = _('term-choices')  # pragma: no cover
_SPDX_LICENSE_EXPRESSION = _('term-spdx-license-expression')  # pragma: no cover
_SEE_REF = _('term-see-ref')  # pragma: no cover
_PROJECT_AUTHORING_CONSOLE_APP = _('project-authoring-console-app')  # pragma: no cover
_PROJECT_MAINTENANCE_CONSOLE_APP = _(
    'term-project-maintenance-console-app'
)  # pragma: no cover
_HELP_NEW = _('term-help-new')  # pragma: no cover
_HELP_FIX = _('term-help-fix')  # pragma: no cover
_TOX_LINT = _('term-tox-e-lint')  # pragma: no cover
_TOX_TEST = _('term-tox-e-test')  # pragma: no cover
_TOX_DIST = _('term-tox-e-dist')  # pragma: no cover
_OPTIONS = _('term-options')  # pragma: no cover
_DISCLAIMER_TEXT = _('adm-disclaimer-text')  # pragma: no cover
_CONTINUOUS_INTEGRATION_CHECKPOINTS = _(
    'term-continuous-integration-checkpoints'
)  # pragma: no cover

EPILOG = f"""
METADATA_FIELD {_CHOICES}:
  | audience
  | environment
  | framework
  | language
  | license
  | license-exception-id
  | license-id
  | status
  | topic

LICENSE_EXPR: :term:`SPDX license expression` {_SPDX_LICENSE_EXPRESSION}
  | {_SEE_REF} https://spdx.github.io/spdx-spec/v2-draft/SPDX-license-expressions/

{_PROJECT_AUTHORING_CONSOLE_APP}:
  | ``ozi-new -h``         {_HELP_NEW}

{_PROJECT_MAINTENANCE_CONSOLE_APP}:
  | ``ozi-fix -h``         {_HELP_FIX}

{_CONTINUOUS_INTEGRATION_CHECKPOINTS}:
  | ``tox -e lint``        {_TOX_LINT}
  | ``tox -e test``        {_TOX_TEST}
  | ``tox -e dist``        {_TOX_DIST}
"""  # pragma: no cover


def setup_parser(version: str) -> argparse.ArgumentParser:  # pragma: no cover
    global _ozi_parser
    _ozi_parser = argparse.ArgumentParser(
        prog='ozi',
        description=sys.modules[__name__].__doc__,
        add_help=False,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=EPILOG,
        usage=f"""%(prog)s [{_OPTIONS}]

    {_DISCLAIMER_TEXT}""",
    )
    helpers = _ozi_parser.add_mutually_exclusive_group()
    helpers.add_argument(
        '-h',
        '--help',
        action='help',
        help=_('term-help-help'),
    )
    helpers.add_argument(
        '-e',
        '--check-license-expr',
        metavar='LICENSE_EXPR',
        action='store',
        help=_('term-help-valid-license-expression'),
    )
    helpers.add_argument(
        '-l',
        '--list-available',
        help=_('term-help-list-available'),
        default=None,
        metavar='METADATA_FIELD',
        action='store',
        choices={i.name.replace('_', '-') for i in fields(ExactMatch) if i.repr},
    )
    helpers.add_argument(
        '--uninstall-user-files',
        help=_('term-help-uninstall-user-files'),
        action='store_const',
        default=lambda: None,
        const=lambda: uninstall_user_files(),
    )
    helpers.add_argument(
        '-v',
        '--version',
        action='store_const',
        default=lambda: None,
        const=lambda: print(version) or exit(0),
        help=_('term-help-version'),
    )
    helpers.add_argument(
        '-c',
        '--check-version',
        action='store_const',
        default=lambda: None,
        const=lambda: check_version(version),
        help=_('term-help-check-version'),
    )
    helpers.add_argument(
        '-i',
        '--info',
        action='store_const',
        default=lambda: None,
        const=lambda: info(version),
        help=_('term-help-info'),
    )
    return _ozi_parser


def main() -> None:  # pragma: no cover
    """``ozi`` script entrypoint."""
    ozi, _ = _ozi_parser.parse_known_args()
    ozi.version()
    ozi.check_version()
    ozi.info()
    ozi.uninstall_user_files()
    if ozi.list_available:
        list_available(ozi.list_available)
    if ozi.check_license_expr:
        license_expression(ozi.check_license_expr)
    _ozi_parser.print_help()
