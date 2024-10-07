"""
``ozi-new`` interactive prompts
"""

from __future__ import annotations

import curses
import os
import sys
from typing import TYPE_CHECKING

from tap_producer import TAP

from ozi_core._i18n import TRANSLATION
from ozi_core.new.interactive.dialog import Project
from ozi_core.new.interactive.dialog import _style
from ozi_core.new.interactive.dialog import admonition_dialog
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
            title=TRANSLATION('dlg-title'),
            heading_label=TRANSLATION('adm-disclaimer-title'),
            text=TRANSLATION('adm-disclaimer-text'),
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
        text=TRANSLATION('adm-maintainers'),
        style=_style,
        yes_text=TRANSLATION('btn-yes'),
        no_text=TRANSLATION('btn-no'),
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
        title=TRANSLATION('dlg-title'),
        heading_label=TRANSLATION('adm-confirm'),
        text='\n'.join(prefix.values()),
        ok_text=TRANSLATION('btn-ok'),
        cancel_text=TRANSLATION('btn-menu'),
    ).run():
        result, output, prefix = _P.menu_loop(output, prefix)
        if isinstance(result, list):
            return result

    ret_args = ['project']

    for k, v in output.items():
        for i in v:
            if len(i) > 0:
                ret_args += [k, i]
    TAP.diagnostic(f'ozi-new {" ".join(ret_args)}')
    return ret_args
