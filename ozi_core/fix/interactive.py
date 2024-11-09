from __future__ import annotations

import os
import sys
from io import UnsupportedOperation
from typing import TYPE_CHECKING
from unittest.mock import Mock

from prompt_toolkit.shortcuts.dialogs import button_dialog
from prompt_toolkit.shortcuts.dialogs import checkboxlist_dialog
from prompt_toolkit.shortcuts.dialogs import radiolist_dialog
from prompt_toolkit.shortcuts.dialogs import yes_no_dialog
from tap_producer import TAP

from ozi_core._i18n import TRANSLATION
from ozi_core.fix.build_definition import walk
from ozi_core.fix.missing import get_relpath_expected_files
from ozi_core.ui._style import _style
from ozi_core.ui.dialog import input_dialog
from ozi_core.ui.menu import MenuButton

if sys.platform != 'win32':  # pragma: no cover
    import curses
else:  # pragma: no cover
    curses = Mock()
    curses.tigetstr = lambda x: b''
    curses.setupterm = lambda: None

if TYPE_CHECKING:  # pragma: no cover
    from argparse import Namespace
    from pathlib import Path


def main_menu(  # pragma: no cover
    output: dict[str, list[str]],
    prefix: dict[str, str],
) -> tuple[None | list[str] | bool, dict[str, list[str]], dict[str, str]]:
    while True:
        match button_dialog(
            title=TRANSLATION('new-dlg-title'),
            text=TRANSLATION('main-menu-text'),
            buttons=[
                MenuButton.RESET._tuple,
                MenuButton.EXIT._tuple,
                MenuButton.BACK._tuple,
            ],
            style=_style,
        ).run():
            case MenuButton.BACK.value:
                break
            case MenuButton.RESET.value:
                if yes_no_dialog(
                    title=TRANSLATION('new-dlg-title'),
                    text=TRANSLATION('main-menu-yn-reset'),
                    style=_style,
                    yes_text=MenuButton.YES._str,
                    no_text=MenuButton.NO._str,
                ).run():
                    return ['interactive', '.'], output, prefix
            case MenuButton.EXIT.value:
                if yes_no_dialog(
                    title=TRANSLATION('new-dlg-title'),
                    text=TRANSLATION('main-menu-yn-exit'),
                    style=_style,
                    yes_text=MenuButton.YES._str,
                    no_text=MenuButton.NO._str,
                ).run():
                    return ['-h'], output, prefix
    return None, output, prefix


class Prompt:
    def __init__(self: Prompt, target: Path) -> None:  # pragma: no cover
        self.target = target
        self.fix: str = 'root'

    def set_fix_mode(  # pragma: no cover
        self: Prompt,
        project_name: str,
        output: dict[str, list[str]],
        prefix: dict[str, str],
    ) -> tuple[list[str] | str | bool | None, dict[str, list[str]], dict[str, str]]:
        self.fix = radiolist_dialog(
            title=TRANSLATION('fix-dlg-title'),
            text=TRANSLATION('fix-add'),
            style=_style,
            cancel_text=MenuButton.MENU._str,
            values=[('source', 'source'), ('test', 'test'), ('root', 'root')],
        ).run()
        if self.fix is not None:
            output['fix'].append(self.fix)
        return None, output, prefix

    def add_or_remove(  # pragma: no cover
        self: Prompt,
        project_name: str,
        output: dict[str, list[str]],
        prefix: dict[str, str],
    ) -> tuple[list[str] | str | bool | None, dict[str, list[str]], dict[str, str]]:
        add_files: list[str] = []
        rem_files: list[str] = []
        output.setdefault('--add', [])
        output.setdefault('--remove', [])
        while True:
            match button_dialog(
                title=TRANSLATION('fix-dlg-title'),
                text='\n'.join(
                    (
                        '\n'.join(iter(prefix)),
                        '\n',
                        TRANSLATION('fix-add-or-remove', projectname=project_name),
                    ),
                ),
                buttons=[
                    MenuButton.ADD._tuple,
                    MenuButton.REMOVE._tuple,
                    MenuButton.MENU._tuple,
                    MenuButton.OK._tuple,
                ],
                style=_style,
            ).run():
                case MenuButton.ADD.value:
                    rel_path, _ = get_relpath_expected_files(self.fix, project_name)
                    files = []
                    with TAP.suppress():
                        for d in walk(self.target, rel_path, []):
                            for v in d.values():
                                files += [str(i) for i in v['missing']]
                    result = checkboxlist_dialog(
                        title=TRANSLATION('fix-dlg-title'),
                        text='',
                        values=[('input', '<input>')] + [(i, i) for i in sorted(files)],
                        style=_style,
                    ).run()
                    if result is not None:
                        add_files += [i for i in result if i != 'input']
                        if len(add_files) > 0:
                            prefix.update(
                                {
                                    f'Add-{self.fix}: {add_files}': (
                                        f'Add-{self.fix}: {add_files}'
                                    ),
                                },
                            )
                            for f in add_files:
                                output['--add'].append(f)
                        if 'input' in set(result):
                            result = input_dialog(
                                title=TRANSLATION('fix-dlg-title'),
                                cancel_text=MenuButton.MENU._str,
                            ).run()
                            if result is not None:
                                add_files += [result]
                                prefix.update(
                                    {
                                        f'Add-{self.fix}: {add_files}': (
                                            f'Add-{self.fix}: {add_files}'
                                        ),
                                    },
                                )
                                output['--add'].append(str(result))
                case MenuButton.REMOVE.value:
                    rel_path, _ = get_relpath_expected_files(self.fix, project_name)
                    files = []
                    with TAP.suppress():
                        for d in walk(self.target, rel_path, []):
                            for v in d.values():
                                files += [str(i) for i in v['found']]
                    result = checkboxlist_dialog(
                        title=TRANSLATION('fix-dlg-title'),
                        text='',
                        values=[('input', '<input>')] + [(i, i) for i in sorted(files)],
                        style=_style,
                    ).run()
                    if result is not None:
                        rem_files += [i for i in result if i != 'input']
                        if len(rem_files) > 0:
                            prefix.update(
                                {
                                    f'Remove-{self.fix}: {rem_files}': (
                                        f'Remove-{self.fix}: {rem_files}'
                                    ),
                                },
                            )
                            for f in rem_files:
                                output['--remove'].append(f)
                        if 'input' in set(result):
                            result = input_dialog(
                                title=TRANSLATION('fix-dlg-title'),
                                cancel_text=MenuButton.MENU._str,
                            ).run()
                            if result is not None:
                                rem_files += [result]
                                prefix.update(
                                    {
                                        f'Remove-{self.fix}: {rem_files}': (
                                            f'Remove-{self.fix}: {rem_files}'
                                        ),
                                    },
                                )
                                output['--remove'].append(str(result))
                case MenuButton.OK.value:
                    break
                case MenuButton.MENU.value:
                    result, output, prefix = main_menu(output, prefix)
                    if result is not None:
                        return result, output, prefix
        return None, output, prefix


def interactive_prompt(project: Namespace) -> list[str]:  # pragma: no cover # noqa: C901
    ret_args = []
    try:
        curses.setupterm()
        e3 = curses.tigetstr('E3') or b''
        clear_screen_seq = curses.tigetstr('clear') or b''
        os.write(sys.stdout.fileno(), e3 + clear_screen_seq)
    except UnsupportedOperation:
        pass
    p = Prompt(project.target)
    result, output, prefix = p.set_fix_mode(
        project_name=project.name, output={'fix': []}, prefix={}
    )
    if isinstance(result, list):
        return result
    result, output, prefix = p.add_or_remove(
        project_name=project.name, output=output, prefix=prefix
    )
    if isinstance(result, list):
        return result
    fix = output.pop('fix')
    for k, v in output.items():
        for i in v:
            if len(i) > 0:
                ret_args += [k, i]
    return fix + ret_args + ['--interactive-io', '.']
