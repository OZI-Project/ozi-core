# ozi/new/validate.py
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
"""ozi-new input validation."""
from __future__ import annotations

import re
from pathlib import Path
from typing import TYPE_CHECKING
from typing import Any
from typing import Sequence
from urllib.parse import urlparse

from ozi_spec import METADATA  # pyright: ignore
from pyparsing import Combine
from pyparsing import ParseException
from pyparsing import ParseResults
from pyparsing import Regex
from tap_producer import TAP
from trove_classifiers import classifiers

from ozi_core.spdx import spdx_license_expression
from ozi_core.vendor.email_validator import EmailNotValidError
from ozi_core.vendor.email_validator import EmailSyntaxError
from ozi_core.vendor.email_validator import ValidatedEmail
from ozi_core.vendor.email_validator import validate_email

if TYPE_CHECKING:  # pragma: no cover
    from argparse import Namespace
    from typing import Callable
    from typing import TypeAlias

    Composable: TypeAlias = Callable[[Namespace], Namespace]

_CLASSIFIERS = {i.partition(' :: ')[2].strip() for i in classifiers}


def valid_classifier(classifier: str) -> None:
    """Validate a classifier string"""
    if classifier in _CLASSIFIERS or classifier in classifiers:
        TAP.ok('Classifier', classifier)
    else:  # pragma: no cover
        TAP.not_ok('Classifier', 'invalid', classifier)


def valid_project_url(project_url: Sequence[str]) -> None:
    """Validate a list of project urls strings of the format ``name,url``."""
    for name, url in [str(i).split(',') for i in project_url]:
        if len(name) > 32:
            TAP.not_ok('Project-URL', 'name', 'too long', '>32 characters')
        else:
            TAP.ok('Project-URL', 'name')
        parsed_url = urlparse(url)
        match parsed_url:
            case p if p.scheme != 'https':
                TAP.diagnostic('only https:// url scheme is supported')
                TAP.not_ok('Project-URL', 'url', 'scheme', 'unsupported')
            case p if p.netloc == '':
                TAP.not_ok('Project-URL', 'url', 'netloc', 'not parseable')
            case _:
                TAP.ok('Project-URL', 'netloc')


def valid_home_page(home_page: str) -> None:
    """Validate a project homepage url"""
    home_url = urlparse(home_page)
    if home_url.scheme != 'https':  # pragma: defer to good-issue
        TAP.not_ok('Home-page', 'url', 'scheme', 'unsupported')
    else:
        TAP.ok('Home-page', 'scheme')
    if home_url.netloc == '':  # pragma: defer to good-issue
        TAP.not_ok('Home-page url netloc could not be parsed.')
    else:
        TAP.ok('Home-page', 'netloc')


def valid_summary(summary: str) -> None:
    """Validate project summary length."""
    if len(summary) > 512:
        TAP.not_ok('Summary', '>512 characters', 'PyPI limit')
    else:
        TAP.ok('Summary')


def valid_contact_info(  # noqa: C901
    author: str,
    maintainer: str,
    author_email: Sequence[str],
    maintainer_email: Sequence[str],
) -> None:
    """Validate project contact info metadata.

    :param author: comma-separated author names
    :type author: str
    :param maintainer: comma-separated maintainer names
    :type maintainer: str
    :param author_email: author email addresses
    :type author_email: Sequence[str]
    :param maintainer_email: maintainer email addresses
    :type maintainer_email: Sequence[str]
    """
    author_and_maintainer_email = False
    if set(author_email).intersection(maintainer_email):
        TAP.not_ok(
            'One or more Author-Email and Maintainer-Email are identical.',
            'Maintainer-Email should be empty',
        )
    elif any(map(len, maintainer_email)) and not any(map(len, author_email)):
        TAP.not_ok('Maintainer-Email', 'provided without setting Author-Email')
    elif any(map(len, maintainer_email)) and any(map(len, author_email)):
        author_and_maintainer_email = True
        TAP.ok('Author-Email(s) and Maintainter-Email(s) provided.')
    else:
        TAP.ok('Author-Email(s) provided.')

    if set(author_email).intersection(maintainer_email):
        TAP.not_ok(  # pragma: defer to good-issue
            'Author and Maintainer are identical',
            'Maintainer should be empty',
        )
    elif len(maintainer) and not author:
        TAP.not_ok('Maintainer', 'provided without setting Author')
    elif len(maintainer) and len(author):
        TAP.ok('Author and Maintainer provided.')
    elif author_and_maintainer_email and not maintainer:
        TAP.not_ok(  # pragma: defer to good issue
            'Maintainer-Email',
            'expected Maintainer name missing',
        )
    else:
        TAP.ok('Author provided.')


def valid_license(_license: str, license_expression: str) -> str:
    """Validate license and check against license expression."""
    if isinstance(_license, list):  # pragma: no cover
        TAP.diagnostic('multiple licenses match, only selected the first', licenses=_license)
        _license = _license[0]
    possible_spdx: Sequence[str] = METADATA.spec.python.pkg.license.ambiguous.get(
        _license,
        (),
    )
    if (
        _license in iter(METADATA.spec.python.pkg.license.ambiguous)
        and len(METADATA.spec.python.pkg.license.ambiguous[_license]) > 1
        and license_expression.split(' ')[0] not in possible_spdx
    ):  # pragma: no cover
        TAP.diagnostic(
            'ambiguous license, set --license-expression to one based on the following:',
            licenses=tuple(possible_spdx),
            reference='https://github.com/pypa/trove-classifiers/issues/17',
        )
        TAP.not_ok('License', 'ambiguous per PEP 639', _license)
    else:
        TAP.ok('License')
    return _license


def valid_copyright_head(copyright_head: str, project_name: str, license_file: str) -> str:
    """Validate a copyright header.

    :param copyright_head: the header text in full
    :type copyright_head: str
    :param project_name: the project name
    :type project_name: str
    :param license_file: the license filename
    :type license_file: str
    """
    if len(copyright_head) == 0:
        copyright_head = '\n'.join(
            [
                f'Part of {project_name}.',
                f'See {license_file} in the project root for details.',
            ],
        )
        TAP.ok('Default-Copyright-Header')
    else:
        if project_name not in copyright_head:
            TAP.diagnostic('project name not found in copyright header')
        elif license_file not in copyright_head:  # pragma: no cover
            TAP.diagnostic('license filename not found in copyright header')
        TAP.ok('Custom-Copyright-Header')
    return copyright_head


def valid_project_name(name: str | ParseResults) -> None:
    """Validate a project name."""
    try:
        Regex('^([A-Z]|[A-Z][A-Z0-9._-]*[A-Z0-9])$', re.IGNORECASE).set_name(
            'Package-Index-Name',
        ).parse_string(str(name))
        TAP.ok('Name')
    except ParseException as e:
        TAP.not_ok(*str(e).split('\n'))


def valid_spdx(expr: Any | ParseResults) -> None:
    """Validate a SPDX license expression."""
    try:
        expr = Combine(
            spdx_license_expression,
            join_string=' ',
        ).parse_string(
            str(expr),
        )[0]
        TAP.ok('License-Expression')
    except ParseException as e:  # pragma: defer to good-issue
        TAP.not_ok(*str(e).split('\n'))


def valid_email(email: str, verify: bool = False) -> ValidatedEmail | None:
    """Validate a single email address."""
    try:
        return validate_email(email, check_deliverability=verify)
    except (EmailNotValidError, EmailSyntaxError) as e:
        TAP.not_ok(*str(e).split('\n'))
        return None  # pragma: no cover


def valid_emails(
    author_email: list[str],
    maintainer_email: list[str],
    verify: bool,
) -> tuple[list[str], list[str]]:
    """Validate lists of author and maintainer emails."""
    _author_email = []
    _maintainer_email = []
    for email in set(author_email).union(maintainer_email):
        emailinfo = valid_email(email, verify=verify)
        match emailinfo:
            case ValidatedEmail() if email in author_email:
                _author_email += [emailinfo.normalized]
                TAP.ok('Author-Email')
            case ValidatedEmail() if email in maintainer_email:
                _maintainer_email += [emailinfo.normalized]
                TAP.ok('Maintainer-Email')
            case None:  # pragma: no cover
                continue
    return _author_email, _maintainer_email


def _valid_project(project: Namespace) -> Namespace:
    """Validate a project namespace."""
    valid_project_name(name=project.name)
    valid_summary(project.summary)
    project.license = valid_license(
        _license=project.license,
        license_expression=project.license_expression,
    )
    valid_home_page(home_page=project.home_page)
    valid_project_url(project_url=project.project_url)
    project.copyright_head = valid_copyright_head(
        copyright_head=project.copyright_head,
        project_name=project.name,
        license_file=project.license_file,
    )
    valid_spdx(project.license_expression)
    valid_contact_info(
        author=project.author,
        maintainer=project.maintainer,
        author_email=project.author_email,
        maintainer_email=project.maintainer_email,
    )
    for i in [
        project.audience,
        project.environment,
        project.framework,
        project.topic,
    ]:
        for classifier in i:
            valid_classifier(classifier)
    return project


def preprocess_arguments(project: Namespace) -> Namespace:
    """Preprocess (validate) arguments for project namespace."""
    if project.strict:
        with TAP.strict():  # pragma: no cover
            return _valid_project(project)
    else:
        return _valid_project(project)


def postprocess_arguments(project: Namespace) -> Namespace:
    """Postprocess (normalize) arguments for project namespace."""
    project.author_email, project.maintainer_email = valid_emails(
        author_email=project.author_email,
        maintainer_email=project.maintainer_email,
        verify=project.verify_email,
    )
    project.keywords = project.keywords.split(',')
    project.name = re.sub(r'[-_.]+', '-', project.name)
    project.target = Path(project.target)
    project.topic = list(set(project.topic))
    project.dist_requires = list(set(project.dist_requires))
    if any(
        i for i in project.target.iterdir() if i not in project.allow_file
    ):  # defer to good-issue
        TAP.not_ok('target directory not empty', 'no files will be created', skip=True)
    match project.ci_provider:
        case 'github':  # pragma: no cover
            pass
        case _:
            TAP.not_ok(
                f'--ci-provider "{project.ci_provider}" unrecognized. ci_user will not be set.',
            )
    project.allow_file = set(map(Path, project.allow_file))
    return project
