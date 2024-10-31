from __future__ import annotations

import os
import sys
from typing import TYPE_CHECKING
from unittest.mock import Mock

from ozi_core._i18n import TRANSLATION
from ozi_core.fix.build_definition import inspect_files
from ozi_core.fix.missing import get_relpath_expected_files
from ozi_core.ui._style import _style
from ozi_core.ui.dialog import input_dialog
from ozi_core.ui.menu import MenuButton

from prompt_toolkit.shortcuts.dialogs import button_dialog
from prompt_toolkit.shortcuts.dialogs import checkboxlist_dialog
from prompt_toolkit.shortcuts.dialogs import radiolist_dialog
from prompt_toolkit.shortcuts.dialogs import message_dialog
from prompt_toolkit.shortcuts.dialogs import yes_no_dialog

if sys.platform != 'win32':
    import curses
else:
    curses = Mock()
    curses.tigetstr = lambda x: b''
    curses.setupterm = lambda: None

if TYPE_CHECKING:
    from argparse import Namespace


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
    def add_or_remove(
        self: Prompt,
        project_name: str,
        output: dict[str, list[str]],
        prefix: dict[str, str],
    ) -> tuple[list[str] | str | bool | None, dict[str, list[str]], dict[str, str]]:
        add_files: list[str] = []
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
                    add_path = radiolist_dialog(
                        title=TRANSLATION('fix-dlg-title'),
                        text=TRANSLATION('fix-add'),
                        style=_style,
                        cancel_text=MenuButton.BACK._str,
                        values=[('source', 'source'), ('test', 'test'), ('root', 'root')],
                    ).run()
                    if add_path:
                        rel_path, expected = get_relpath_expected_files(add_path, project_name)
                        inspect_files(project.target, rel_path, expected)
                        input_dialog(
                            title=TRANSLATION('fix-dlg-title'),
                            text=''
                        )
                        add_files += []
                        prefix.update(
                            {
                                f'Add: {add_path}': (
                                    f'Add: {add_path}'
                                ),
                            },
                        )
                        output['--add'].append(add_path)
                case MenuButton.REMOVE.value:
                    if len(add_files) != 0:
                        del_files = checkboxlist_dialog(
                            title=TRANSLATION('fix-dlg-title'),
                            text=TRANSLATION('fix-remove'),
                            values=list(zip(add_files, add_files)),
                            style=_style,
                            cancel_text=MenuButton.BACK._str,
                        ).run()
                        if del_files:
                            add_files = list(
                                set(add_files).symmetric_difference(
                                    set(del_files),
                                ),
                            )
                            for f in del_files:
                                output['--remove'].append(f)
                                prefix.update({f'Remove: {f}': f'Remove: {f}'})
                    else:
                        message_dialog(
                            title=TRANSLATION('fix-dlg-title'),
                            text=TRANSLATION('fix-nothing-to-remove'),
                            style=_style,
                            ok_text=MenuButton.OK._str,
                        ).run()
                case MenuButton.OK.value:
                    break
                case MenuButton.MENU.value:
                    result, output, prefix = main_menu(output, prefix)
                    if result is not None:
                        return result, output, prefix
        return None, output, prefix


def interactive_prompt(project: Namespace) -> list[str]:  # pragma: no cover
    ret_args = ['source']
    curses.setupterm()
    e3 = curses.tigetstr('E3') or b''
    clear_screen_seq = curses.tigetstr('clear') or b''
    os.write(sys.stdout.fileno(), e3 + clear_screen_seq)
    p = Prompt()
    result, output, prefix = p.add_or_remove(project_name=project.name, output={}, prefix={})
    if isinstance(result, list):
        return result
    for k, v in output.items():
        for i in v:
            if len(i) > 0:
                ret_args += [k, i]
    return ret_args + ['.']
