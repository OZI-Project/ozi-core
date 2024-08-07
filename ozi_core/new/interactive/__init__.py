"""
``ozi-new`` interactive prompts
"""

from __future__ import annotations

import curses
import os
import sys
from typing import TYPE_CHECKING

from tap_producer import TAP

from ozi_core.new.interactive.dialog import Project
from ozi_core.new.interactive.dialog import _style
from ozi_core.new.interactive.dialog import admonition_dialog
from ozi_core.new.interactive.dialog import menu_loop
from ozi_core.new.interactive.dialog import yes_no_dialog

if TYPE_CHECKING:
    from argparse import Namespace


_P = Project()


def interactive_prompt(project: Namespace) -> list[str]:  # noqa: C901  # pragma: no cover
    curses.setupterm()
    e3 = curses.tigetstr('E3') or b''
    clear_screen_seq = curses.tigetstr('clear') or b''
    os.write(sys.stdout.fileno(), e3 + clear_screen_seq)

    if (
        admonition_dialog(
            title='ozi-new interactive prompt',
            heading_label='Disclaimer',
            text="""
The information provided on this prompt does not, and is not intended
to, constitute legal advice. All information, content, and materials
available on this prompt are for general informational purposes only.
Information on this prompt may not constitute the most up-to-date
legal or other information.

THE LICENSE TEMPLATES, LICENSE IDENTIFIERS, LICENSE CLASSIFIERS,
AND LICENSE EXPRESSION PARSING SERVICES, AND ALL OTHER CONTENTS ARE
PROVIDED "AS IS", NO REPRESENTATIONS ARE MADE THAT THE CONTENT IS
ERROR-FREE AND/OR APPLICABLE FOR ANY PURPOSE, INCLUDING MERCHANTABILITY.

Readers of this prompt should contact their attorney to obtain advice
with respect to any particular legal matter. The OZI Project is not a
law firm and does not provide legal advice. No reader or user of this
prompt should act or abstain from acting on the basis of information
on this prompt without first seeking legal advice from counsel in the
relevant jurisdiction. Legal counsel can ensure that the information
provided in this prompt is applicable to your particular situation.
Use of, or reading, this prompt or any of the resources contained
within does not create an attorney-client relationship.
""",
        ).run()
        is None
    ):
        return []

    prefix: dict[str, str] = {}
    output: dict[str, list[str]] = {}
    project_name = '""'

    result, output, prefix = _P.name(output, prefix, project.check_package_exists)
    if isinstance(result, list):
        return result
    if isinstance(result, str):
        project_name = result

    result, output, prefix = _P.summary(project_name, output, prefix)
    if isinstance(result, list):
        return result

    result, output, prefix = _P.keywords(project_name, output, prefix)
    if isinstance(result, list):
        return result

    result, output, prefix = _P.home_page(project_name, output, prefix)
    if isinstance(result, list):
        return result

    result, output, prefix = _P.author(project_name, output, prefix)
    if isinstance(result, list):
        return result

    result, output, prefix = _P.author_email(project_name, output, prefix)
    if isinstance(result, list):
        return result

    result, output, prefix = _P.license_(project_name, output, prefix)
    if isinstance(result, list):
        return result
    _license = result if result else ''

    result, output, prefix = _P.license_expression(project_name, _license, output, prefix)
    if isinstance(result, list):
        return result

    if yes_no_dialog(
        title='ozi-new interactive prompt',
        text=f'Are there any maintainers of {project_name}?\n(other than the author or authors)',
        style=_style,
    ).run():
        result, output, prefix = _P.maintainer(project_name, output, prefix)
        if isinstance(result, list):
            return result

        result, output, prefix = _P.maintainer_email(project_name, output, prefix)
        if isinstance(result, list):
            return result

    result, output, prefix = _P.requires_dist(project_name, output, prefix)
    if isinstance(result, list):
        return result

    while not admonition_dialog(
        title='ozi-new interactive prompt',
        heading_label='Confirm project creation?\nPKG-INFO Metadata:',
        text='\n'.join(prefix.values()),
        ok_text='✔ Ok',
        cancel_text='☰  Menu',
    ).run():
        result, output, prefix = menu_loop(output, prefix)
        if isinstance(result, list):
            return result

    ret_args = ['project']

    for k, v in output.items():
        for i in v:
            if len(i) > 0:
                ret_args += [k, i]
    TAP.diagnostic('ozi-new project args', ' '.join(ret_args))
    return ret_args
