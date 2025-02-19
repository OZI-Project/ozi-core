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

from ozi_core._i18n import TRANSLATION
from ozi_core.actions import CloseMatch
from ozi_core.ui.defaults import COPYRIGHT_HEAD

parser = argparse.ArgumentParser(
    prog='ozi-new',
    description=sys.modules[__name__].__doc__,
    add_help=False,
    usage='\n'.join(
        [
            f'%(prog)s [{TRANSLATION("term-options")}] | [{TRANSLATION("term-positional-args")}]',
            TRANSLATION('adm-disclaimer-text'),
        ],
    ),
)
subparser = parser.add_subparsers(help='', metavar='', dest='new')
interactive_parser = subparser.add_parser(
    'interactive',
    aliases=['i'],
    description=TRANSLATION('term-desc-new-interactive'),
    help=TRANSLATION('term-help-new-interactive'),
    prog='ozi-new interactive',
    usage=f'%(prog)s [{TRANSLATION("term-options")}] | [{TRANSLATION("term-positional-args")}]',
)
PROJECT_METADATA_HELP = f'[{TRANSLATION("term-required-metadata")}] [{TRANSLATION("term-optional-metadata")}] [{TRANSLATION("term-default-metadata")}]'  # noqa: B950,E501,RUF100
project_parser = subparser.add_parser(
    'project',
    aliases=['p'],
    description=TRANSLATION('term-desc-new-project'),
    help=TRANSLATION('term-help-new-project'),
    prog='ozi-new project',
    usage=f'%(prog)s [{TRANSLATION("term-options")}] {PROJECT_METADATA_HELP} [{TRANSLATION("term-defaults")}] target',  # noqa: B950,E501,RUF100
)
interactive_parser.add_argument(
    'target',
    type=validate_filepath_arg,
    nargs='?',
    default='.',
    help=TRANSLATION('term-help-new-target'),
)
interactive_defaults = interactive_parser.add_argument_group(TRANSLATION('term-defaults'))
interactive_defaults.add_argument(
    '-c',
    '--check-package-exists',
    default=True,
    action=argparse.BooleanOptionalAction,
    help=TRANSLATION('term-help-check-package-exists'),
)
required = project_parser.add_argument_group(TRANSLATION('term-required-metadata'))
optional = project_parser.add_argument_group(TRANSLATION('term-optional-metadata'))
defaults = project_parser.add_argument_group(TRANSLATION('term-default-metadata'))
ozi_defaults = project_parser.add_argument_group(TRANSLATION('term-defaults'))
ozi_required = project_parser.add_argument_group(TRANSLATION('term-required'))
ozi_defaults.add_argument(
    '-c',
    '--copyright-head',
    type=str,
    default=COPYRIGHT_HEAD,
    help=TRANSLATION('term-copyright-head'),
    metavar='HEADER',
)
ozi_defaults.add_argument(
    '--ci-provider',
    type=str,
    default='github',
    choices=frozenset(METADATA.spec.python.ci.providers),
    metavar='github',
    help=TRANSLATION('term-ci-provider'),
)
required.add_argument(
    '-n',
    '--name',
    type=str,
    help=TRANSLATION(
        'term-help',
        name=TRANSLATION('edit-menu-btn-name'),
        text=TRANSLATION('term-help-name'),
    ),
)
required.add_argument(
    '-a',
    '--author',
    type=str,
    help=TRANSLATION(
        'term-help',
        name=TRANSLATION('edit-menu-btn-author'),
        text=TRANSLATION('term-help-author'),
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
    help=TRANSLATION(
        'term-help',
        name=TRANSLATION('edit-menu-btn-email'),
        text=TRANSLATION('term-help-author-email'),
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
    help=TRANSLATION(
        'term-help',
        name=TRANSLATION('edit-menu-btn-summary'),
        text=TRANSLATION('term-help-summary'),
    ),
)
required.add_argument(
    '--license-expression',
    type=str,
    help=TRANSLATION(
        'term-help',
        name=TRANSLATION('edit-menu-btn-license-expression'),
        text=TRANSLATION('term-help-license-expression'),
    ),
)
required.add_argument(
    '-l',
    '--license',
    type=str,
    help=TRANSLATION(
        'term-help',
        name=TRANSLATION('edit-menu-btn-license'),
        text=TRANSLATION('term-help-license'),
    ),
    action=CloseMatch,
)
defaults.add_argument(
    '--audience',
    '--intended-audience',
    metavar='AUDIENCE_NAMES',
    type=str,
    help=TRANSLATION(
        'term-help-default',
        name=TRANSLATION('edit-menu-btn-audience'),
        text=TRANSLATION('term-help-audience'),
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
    help=TRANSLATION(
        'term-help-default',
        name=TRANSLATION('edit-menu-btn-typing'),
        text=TRANSLATION('term-help-typing'),
        default=str(METADATA.spec.python.pkg.info.classifiers.typing),
    ),
    default=METADATA.spec.python.pkg.info.classifiers.typing,
)
defaults.add_argument(
    '--environment',
    metavar='ENVIRONMENT_NAMES',
    default=METADATA.spec.python.pkg.info.classifiers.environment,
    help=TRANSLATION(
        'term-help-default',
        name=TRANSLATION('edit-menu-btn-environment'),
        text=TRANSLATION('term-help-environment'),
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
    help=TRANSLATION(
        'term-help-default',
        name=TRANSLATION('edit-menu-btn-license-file'),
        text=TRANSLATION('term-help-license-file'),
        default='LICENSE.txt',
    ),
    type=str,
)
optional.add_argument(
    '--keywords',
    default='',
    help=TRANSLATION(
        'term-help',
        name=TRANSLATION('edit-menu-btn-keywords'),
        text=TRANSLATION('term-help-keywords'),
    ),
    type=str,
)
optional.add_argument(
    '--maintainer',
    default=[],
    action='append',
    nargs='?',
    metavar='MAINTAINER_NAMES',
    help=TRANSLATION(
        'term-help',
        name=TRANSLATION('edit-menu-btn-maintainer'),
        text=TRANSLATION('term-help-maintainer'),
    ),
)
optional.add_argument(
    '--maintainer-email',
    help=TRANSLATION(
        'term-help',
        name=TRANSLATION('edit-menu-btn-maintainer-email'),
        text=TRANSLATION('term-help-maintainer-email'),
    ),
    action='append',
    metavar='MAINTAINER_EMAILS',
    default=[],
    nargs='?',
)
optional.add_argument(
    '--framework',
    help=TRANSLATION(
        'term-help',
        name=TRANSLATION('edit-menu-btn-framework'),
        text=TRANSLATION('term-help-framework'),
    ),
    metavar='FRAMEWORK_NAMES',
    action='append',
    type=str,
    nargs='?',
    default=[],
)
optional.add_argument(
    '--project-url',
    help=TRANSLATION(
        'term-help',
        name=TRANSLATION('edit-menu-btn-project-url'),
        text=TRANSLATION('term-help-project-url'),
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
    help=TRANSLATION(
        'term-help-default',
        name=TRANSLATION('edit-menu-btn-language'),
        text=TRANSLATION('term-help-language'),
        default=str(['English']),
    ),
    action='append',
    type=str,
    nargs='?',
)
optional.add_argument(
    '--topic',
    help=TRANSLATION(
        'term-help',
        name=TRANSLATION('edit-menu-btn-topic'),
        text=TRANSLATION('term-help-topic'),
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
    action=CloseMatch,
    default=METADATA.spec.python.pkg.info.classifiers.development_status,
    help=TRANSLATION(
        'term-help-default',
        name=TRANSLATION('edit-menu-btn-status'),
        text=TRANSLATION('term-help-status'),
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
    help=TRANSLATION(
        'term-help-default',
        name=TRANSLATION('edit-menu-btn-readme-type'),
        text=str(('rst', 'md', 'txt')),
        default='rst',
    ),
)
optional.add_argument(
    '-r',
    '--dist-requires',
    '--requires-dist',
    help=TRANSLATION(
        'term-help',
        name=TRANSLATION('edit-menu-btn-requires-dist'),
        text=TRANSLATION('term-help-requires-dist'),
    ),
    action='append',
    type=str,
    nargs='?',
    default=[],
    metavar='DIST_REQUIRES',
)

output = parser.add_mutually_exclusive_group()
output.add_argument('-h', '--help', action='help', help=TRANSLATION('term-help-help'))
ozi_defaults.add_argument(
    '--verify-email',
    default=False,
    action=argparse.BooleanOptionalAction,
    help=TRANSLATION('term-help-verify-email'),
)
ozi_defaults.add_argument(
    '--update-wrapfile',
    action=argparse.BooleanOptionalAction,
    default=False,
    help=TRANSLATION('term-help-update-wrapfile'),
)
ozi_defaults.add_argument(
    '--enable-cython',
    default=False,
    action=argparse.BooleanOptionalAction,
    help=TRANSLATION('term-help-enable-cython'),
)
ozi_defaults.add_argument(
    '--enable-uv',
    default=False,
    action=argparse.BooleanOptionalAction,
    help=TRANSLATION('term-help-enable-uv'),
)
ozi_defaults.add_argument(
    '--github-harden-runner',
    default=False,
    action=argparse.BooleanOptionalAction,
    help=TRANSLATION('term-help-github-harden-runner'),
)
ozi_defaults.add_argument(
    '--strict',
    default=False,
    action=argparse.BooleanOptionalAction,
    help=TRANSLATION('term-help-strict'),
)
ozi_defaults.add_argument(
    '--allow-file',
    help=TRANSLATION(
        'term-help-default',
        name=TRANSLATION('term-help-name-allow-file'),
        text=TRANSLATION('term-help-allow-file'),
        default=str(METADATA.spec.python.src.allow_files),
    ),
    action='append',
    type=str,
    nargs='?',
    metavar='ALLOW_FILE_PATTERNS',
    default=METADATA.spec.python.src.allow_files,
)
ozi_required.add_argument(
    'target',
    type=validate_filepath_arg,
    nargs='?',
    default='.',
    help=TRANSLATION('term-help-new-target'),
)
