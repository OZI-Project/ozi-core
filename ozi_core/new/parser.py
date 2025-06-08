# ozi/new/parser.py
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
"""``ozi-new`` console application."""
from __future__ import annotations

import argparse
import sys

from ozi_spec import METADATA
from pathvalidate.argparse import validate_filepath_arg

from ozi_core._i18n import TRANSLATION as _
from ozi_core.ui.defaults import COPYRIGHT_HEAD

_.mime_type = 'text/plain;charset=UTF-8'
_OPTIONS = _('term-options')
_REQUIRED_METADATA = _('term-required-metadata')
_DISCLAIMER_TEXT = _('adm-disclaimer-text')
_POSITIONAL_ARGS = _('term-positional-args')
_OPTIONAL_METADATA = _('term-optional-metadata')
_DEFAULT_METADATA = _('term-default-metadata')
_DEFAULTS = _('terms-defaults')

parser = argparse.ArgumentParser(
    prog='ozi-new',
    description=sys.modules[__name__].__doc__,
    add_help=False,
    usage='\n'.join(
        [
            f'%(prog)s [{_OPTIONS}] | [{_POSITIONAL_ARGS}]',
            _DISCLAIMER_TEXT,
        ],
    ),
)
subparser = parser.add_subparsers(help='', metavar='', dest='new')
interactive_parser = subparser.add_parser(
    'interactive',
    aliases=['i'],
    description=_('term-desc-new-interactive'),
    help=_('term-help-new-interactive'),
    prog='ozi-new interactive',
    usage=f'%(prog)s [{_OPTIONS}] | [{_POSITIONAL_ARGS}]',
)
webui_parser = subparser.add_parser(
    'webui',
    aliases=['w'],
    description=_('term-desc-new-webui'),
    help=_('term-help-new-webui'),
    prog='ozi-new webui',
    usage=f'%(prog)s [{_OPTIONS}] | [{_POSITIONAL_ARGS}]',
)
PROJECT_METADATA_HELP = f'[{_REQUIRED_METADATA}] [{_OPTIONAL_METADATA}] [{_DEFAULT_METADATA}]'  # noqa: B950,E501,RUF100
project_parser = subparser.add_parser(
    'project',
    aliases=['p'],
    description=_('term-desc-new-project'),
    help=_('term-help-new-project'),
    prog='ozi-new project',
    usage=f'%(prog)s [{_OPTIONS}] {PROJECT_METADATA_HELP} [{_DEFAULTS}] target',  # noqa: B950,E501,RUF100
)
webui_parser.add_argument(
    'target',
    type=validate_filepath_arg,
    nargs='?',
    default='.',
    help=_('term-help-new-target'),
)
interactive_parser.add_argument(
    'target',
    type=validate_filepath_arg,
    nargs='?',
    default='.',
    help=_('term-help-new-target'),
)
interactive_defaults = interactive_parser.add_argument_group(_('term-defaults'))
interactive_defaults.add_argument(
    '-c',
    '--check-package-exists',
    default=True,
    action=argparse.BooleanOptionalAction,
    help=_('term-help-check-package-exists'),
)
required = project_parser.add_argument_group(_('term-required-metadata'))
optional = project_parser.add_argument_group(_('term-optional-metadata'))
defaults = project_parser.add_argument_group(_('term-default-metadata'))
ozi_defaults = project_parser.add_argument_group(_('term-defaults'))
ozi_required = project_parser.add_argument_group(_('term-required'))
ozi_defaults.add_argument(
    '-c',
    '--copyright-head',
    type=str,
    default=COPYRIGHT_HEAD,
    help=_('term-copyright-head'),
    metavar='HEADER',
)
ozi_defaults.add_argument(
    '--ci-provider',
    type=str,
    default='github',
    choices=frozenset(METADATA.spec.python.ci.providers),
    metavar='github',
    help=_('term-ci-provider'),
)
required.add_argument(
    '-n',
    '--name',
    type=str,
    help=_(
        'term-help',
        name=_('edit-menu-btn-name'),
        text=_('term-help-name'),
    ),
)
required.add_argument(
    '-a',
    '--author',
    type=str,
    help=_(
        'term-help',
        name=_('edit-menu-btn-author'),
        text=_('term-help-author'),
    ),
    action='append',
    default=[],
    metavar='AUTHOR_NAMES',
    nargs='?',
)
required.add_argument(
    '-e',
    '--author-email',
    type=str,
    help=_(
        'term-help',
        name=_('edit-menu-btn-email'),
        text=_('term-help-author-email'),
    ),
    default=[],
    metavar='AUTHOR_EMAILS',
    nargs='?',
    action='append',
)
required.add_argument(
    '-s',
    '--summary',
    type=str,
    help=_(
        'term-help',
        name=_('edit-menu-btn-summary'),
        text=_('term-help-summary'),
    ),
)
required.add_argument(
    '--license-expression',
    type=str,
    help=_(
        'term-help',
        name=_('edit-menu-btn-license-expression'),
        text=_('term-help-license-expression'),
    ),
)
required.add_argument(
    '-l',
    '--license',
    type=str,
    help=_(
        'term-help',
        name=_('edit-menu-btn-license'),
        text=_('term-help-license'),
    ),
)
defaults.add_argument(
    '--audience',
    '--intended-audience',
    metavar='AUDIENCE_NAMES',
    type=str,
    help=_(
        'term-help-default',
        name=_('edit-menu-btn-audience'),
        text=_('term-help-audience'),
        default=str(METADATA.spec.python.pkg.info.classifiers.intended_audience),
    ),
    default=METADATA.spec.python.pkg.info.classifiers.intended_audience,
    nargs='?',
    action='append',
)
defaults.add_argument(
    '--typing',
    type=str,
    choices=frozenset(('Typed', 'Stubs Only')),
    nargs='?',
    metavar='PY_TYPED_OR_STUBS',
    help=_(
        'term-help-default',
        name=_('edit-menu-btn-typing'),
        text=_('term-help-typing'),
        default=str(METADATA.spec.python.pkg.info.classifiers.typing),
    ),
    default=METADATA.spec.python.pkg.info.classifiers.typing,
)
defaults.add_argument(
    '--environment',
    metavar='ENVIRONMENT_NAMES',
    default=METADATA.spec.python.pkg.info.classifiers.environment,
    help=_(
        'term-help-default',
        name=_('edit-menu-btn-environment'),
        text=_('term-help-environment'),
        default=str(METADATA.spec.python.pkg.info.classifiers.environment),
    ),
    action='append',
    nargs='?',
    type=str,
)
defaults.add_argument(
    '--license-file',
    default='LICENSE.txt',
    metavar='LICENSE_FILENAME',
    choices=frozenset(('LICENSE.txt',)),
    help=_(
        'term-help-default',
        name=_('edit-menu-btn-license-file'),
        text=_('term-help-license-file'),
        default='LICENSE.txt',
    ),
    type=str,
)
optional.add_argument(
    '--keywords',
    default='',
    help=_(
        'term-help',
        name=_('edit-menu-btn-keywords'),
        text=_('term-help-keywords'),
    ),
    type=str,
)
optional.add_argument(
    '--maintainer',
    default=[],
    action='append',
    nargs='?',
    metavar='MAINTAINER_NAMES',
    help=_(
        'term-help',
        name=_('edit-menu-btn-maintainer'),
        text=_('term-help-maintainer'),
    ),
)
optional.add_argument(
    '--maintainer-email',
    help=_(
        'term-help',
        name=_('edit-menu-btn-maintainer-email'),
        text=_('term-help-maintainer-email'),
    ),
    action='append',
    metavar='MAINTAINER_EMAILS',
    default=[],
    nargs='?',
)
optional.add_argument(
    '--framework',
    help=_(
        'term-help',
        name=_('edit-menu-btn-framework'),
        text=_('term-help-framework'),
    ),
    metavar='FRAMEWORK_NAMES',
    action='append',
    type=str,
    nargs='?',
    default=[],
)
optional.add_argument(
    '--project-url',
    help=_(
        'term-help',
        name=_('edit-menu-btn-project-url'),
        text=_('term-help-project-url'),
    ),
    action='append',
    metavar='PROJECT_URLS',
    default=[],
    nargs='?',
)
defaults.add_argument(
    '--language',
    '--natural-language',
    metavar='LANGUAGE_NAMES',
    default=['English'],
    help=_(
        'term-help-default',
        name=_('edit-menu-btn-language'),
        text=_('term-help-language'),
        default=str(['English']),
    ),
    action='append',
    type=str,
    nargs='?',
)
optional.add_argument(
    '--topic',
    help=_(
        'term-help',
        name=_('edit-menu-btn-topic'),
        text=_('term-help-topic'),
    ),
    nargs='?',
    metavar='TOPIC_NAMES',
    action='append',
    type=str,
    default=[],
)
defaults.add_argument(
    '--status',
    '--development-status',
    default=METADATA.spec.python.pkg.info.classifiers.development_status,
    help=_(
        'term-help-default',
        name=_('edit-menu-btn-status'),
        text=_('term-help-status'),
        default=str(['1 - Planning']),
    ),
    type=str,
)
defaults.add_argument(
    '--long-description-content-type',
    '--readme-type',
    metavar='README_TYPE',
    default='rst',
    choices=('rst', 'md', 'txt'),
    help=_(
        'term-help-default',
        name=_('edit-menu-btn-readme-type'),
        text=str(('rst', 'md', 'txt')),
        default='rst',
    ),
)
optional.add_argument(
    '-r',
    '--dist-requires',
    '--requires-dist',
    help=_(
        'term-help',
        name=_('edit-menu-btn-requires-dist'),
        text=_('term-help-requires-dist'),
    ),
    action='append',
    type=str,
    nargs='?',
    default=[],
    metavar='DIST_REQUIRES',
)

output = parser.add_mutually_exclusive_group()
output.add_argument('-h', '--help', action='help', help=_('term-help-help'))
ozi_defaults.add_argument(
    '--verify-email',
    default=False,
    action=argparse.BooleanOptionalAction,
    help=_('term-help-verify-email'),
)
ozi_defaults.add_argument(
    '--update-wrapfile',
    action=argparse.BooleanOptionalAction,
    default=False,
    help=_('term-help-update-wrapfile'),
)
ozi_defaults.add_argument(
    '--enable-create-pull-request',
    default=True,
    action=argparse.BooleanOptionalAction,
    help=_('term-help-enable-create-pull-request'),
)
ozi_defaults.add_argument(
    '--enable-cython',
    default=False,
    action=argparse.BooleanOptionalAction,
    help=_('term-help-enable-cython'),
)
ozi_defaults.add_argument(
    '--enable-uv',
    default=False,
    action=argparse.BooleanOptionalAction,
    help=_('term-help-enable-uv'),
)
ozi_defaults.add_argument(
    '--github-harden-runner',
    default=False,
    action=argparse.BooleanOptionalAction,
    help=_('term-help-github-harden-runner'),
)
ozi_defaults.add_argument(
    '--signed-wheel',
    default=False,
    action=argparse.BooleanOptionalAction,
    help=_('term-help-signed-wheel'),
)
ozi_defaults.add_argument(
    '--strict',
    default=False,
    action=argparse.BooleanOptionalAction,
    help=_('term-help-strict'),
)
ozi_defaults.add_argument(
    '--testpypi',
    default=False,
    action=argparse.BooleanOptionalAction,
    help=_('term-help-testpypi'),
)
ozi_defaults.add_argument(
    '--allow-file',
    help=_(
        'term-help-default',
        name=_('term-help-name-allow-file'),
        text=_('term-help-allow-file'),
        default=str(METADATA.spec.python.src.allow_files),
    ),
    action='append',
    type=str,
    nargs='?',
    metavar='ALLOW_FILE_PATTERNS',
    default=list(METADATA.spec.python.src.allow_files),
)
ozi_required.add_argument(
    'target',
    type=validate_filepath_arg,
    nargs='?',
    default='.',
    help=_('term-help-new-target'),
)
