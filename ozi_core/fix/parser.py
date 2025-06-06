# ozi/fix/parser.py
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
"""``ozi-fix`` console application."""
import sys
from argparse import SUPPRESS
from argparse import ArgumentParser
from argparse import BooleanOptionalAction

from pathvalidate.argparse import validate_filepath_arg

from ozi_core._i18n import TRANSLATION as _
from ozi_core.fix.validate import AppendRewriteCommandTarget
from ozi_core.ui.defaults import COPYRIGHT_HEAD
from ozi_core.ui.defaults import FIX_PRETTY
from ozi_core.ui.defaults import FIX_STRICT

_.mime_type = 'text/plain;charset=UTF-8'
_OPTIONS = _('term-options')
_OUTPUT = _('term-output')
_DISCLAIMER_TEXT = _('adm-disclaimer-text')
_POSITIONAL_ARGS = _('term-positional-args')

parser = ArgumentParser(
    prog='ozi-fix',
    description=sys.modules[__name__].__doc__,
    add_help=False,
    usage=f"""%(prog)s [{_OPTIONS}] | [{_POSITIONAL_ARGS}]

{_DISCLAIMER_TEXT}
""",
)
parser.add_argument(
    '--add',
    metavar='FILENAME',
    nargs='?',
    action=AppendRewriteCommandTarget,
    default=[],
    help=SUPPRESS,
)
parser.add_argument(
    '--remove',
    metavar='FILENAME',
    nargs='?',
    action=AppendRewriteCommandTarget,
    default=[],
    help=SUPPRESS,
)
parser.add_argument(
    '--strict',
    default=FIX_STRICT,
    action=BooleanOptionalAction,
    help=SUPPRESS,
)
parser.add_argument(
    '--pretty',
    default=FIX_PRETTY,
    action=BooleanOptionalAction,
    help=SUPPRESS,
)
parser.add_argument(
    '--update-wrapfile',
    action=BooleanOptionalAction,
    default=False,
    help=SUPPRESS,
)
subparser = parser.add_subparsers(help='', metavar='', dest='fix')
helpers = parser.add_mutually_exclusive_group()
helpers.add_argument('-h', '--help', action='help', help=_('term-help-help'))
missing_parser = subparser.add_parser(
    'missing',
    prog='ozi-fix missing',
    aliases=['m', 'mis'],
    usage=f'%(prog)s [{_OPTIONS}] [{_OUTPUT}] target',
    allow_abbrev=True,
    help=_('term-help-fix-missing'),
)
missing_parser.add_argument(
    '--add',
    metavar='FILENAME',
    nargs='?',
    action=AppendRewriteCommandTarget,
    default=[],
    help=SUPPRESS,
)
missing_parser.add_argument(
    '--remove',
    metavar='FILENAME',
    nargs='?',
    action=AppendRewriteCommandTarget,
    default=[],
    help=SUPPRESS,
)
missing_parser.add_argument(
    '--update-wrapfile',
    action=BooleanOptionalAction,
    default=False,
    help=_('term-help-update-wrapfile'),
)
missing_output = missing_parser.add_argument_group(_('term-output'))
missing_output.add_argument(
    '--strict',
    default=FIX_STRICT,
    action=BooleanOptionalAction,
    help=_('term-help-strict'),
)
missing_output.add_argument(
    '--pretty',
    default=FIX_PRETTY,
    action=BooleanOptionalAction,
    help=_('term-help-pretty'),
)
missing_parser.add_argument(
    'target',
    type=validate_filepath_arg,
    nargs='?',
    default='.',
    help=_('term-help-fix-target'),
)
source_parser = subparser.add_parser(
    'source',
    aliases=['s', 'src'],
    prog='ozi-fix source',
    usage=f'%(prog)s [{_OPTIONS}] [{_OUTPUT}] target',
    allow_abbrev=True,
    help=_('term-help-fix-source'),
)
test_parser = subparser.add_parser(
    'test',
    prog='ozi-fix test',
    usage=f'%(prog)s [{_OPTIONS}] [{_OUTPUT}] target',
    aliases=['t', 'tests'],
    allow_abbrev=True,
    help=_('term-help-fix-test'),
)
source_parser.add_argument(
    '-a',
    '--add',
    metavar='FILENAME',
    nargs='?',
    action=AppendRewriteCommandTarget,
    default=[],
    help=_('term-help-fix-add'),
)
source_parser.add_argument(
    '-r',
    '--remove',
    metavar='FILENAME',
    nargs='?',
    action=AppendRewriteCommandTarget,
    default=[],
    help=_('term-help-fix-remove'),
)
source_parser.add_argument(
    '-c',
    '--copyright-head',
    metavar='HEADER',
    type=str,
    default=COPYRIGHT_HEAD,
    help=_('term-copyright-head'),
)
source_parser.add_argument(
    '--update-wrapfile',
    action=BooleanOptionalAction,
    default=False,
    help=_('term-help-update-wrapfile'),
)
source_output = source_parser.add_argument_group(_('term-output'))
source_output.add_argument(
    '--strict',
    default=FIX_STRICT,
    action=BooleanOptionalAction,
    help=_('term-help-strict'),
)
source_output.add_argument(
    '--pretty',
    default=FIX_PRETTY,
    action=BooleanOptionalAction,
    help=_('term-help-pretty'),
)
source_output.add_argument(
    '--interactive-io',
    default=False,
    action=BooleanOptionalAction,
    help=SUPPRESS,
)
source_parser.add_argument(
    'target',
    type=validate_filepath_arg,
    nargs='?',
    default='.',
    help=_('term-help-fix-target'),
)
test_parser.add_argument(
    '-a',
    '--add',
    metavar='FILENAME',
    nargs='?',
    action=AppendRewriteCommandTarget,
    default=[],
    help=_('term-help-fix-add'),
)
test_parser.add_argument(
    '-r',
    '--remove',
    metavar='FILENAME',
    nargs='?',
    action=AppendRewriteCommandTarget,
    default=[],
    help=_('term-help-fix-remove'),
)
test_parser.add_argument(
    '-c',
    '--copyright-head',
    metavar='HEADER',
    type=str,
    default=COPYRIGHT_HEAD,
    help=_('term-copyright-head'),
)
test_parser.add_argument(
    '--update-wrapfile',
    action=BooleanOptionalAction,
    default=False,
    help=_('term-help-update-wrapfile'),
)
test_output = test_parser.add_argument_group(_('term-output'))
test_output.add_argument(
    '--strict',
    default=FIX_STRICT,
    action=BooleanOptionalAction,
    help=_('term-help-strict'),
)
test_output.add_argument(
    '--pretty',
    default=FIX_PRETTY,
    action=BooleanOptionalAction,
    help=_('term-help-pretty'),
)
test_output.add_argument(
    '--interactive-io',
    default=False,
    action=BooleanOptionalAction,
    help=SUPPRESS,
)
test_parser.add_argument(
    'target',
    type=validate_filepath_arg,
    nargs='?',
    default='.',
    help=_('term-help-fix-target'),
)
interactive_parser = subparser.add_parser(
    'interactive',
    prog='ozi-fix interactive',
    aliases=['i'],
    usage='%(prog)s target',
    allow_abbrev=True,
    help=_('term-help-fix-interactive'),
)
interactive_parser.add_argument(
    'target',
    type=validate_filepath_arg,
    nargs='?',
    default='.',
    help=_('term-help-fix-target'),
)
