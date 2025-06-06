from __future__ import annotations

import os
import sys
from contextlib import suppress
from dataclasses import asdict
from io import UnsupportedOperation
from typing import TYPE_CHECKING
from typing import Any
from unittest.mock import Mock

from prompt_toolkit.shortcuts.dialogs import button_dialog
from prompt_toolkit.shortcuts.dialogs import checkboxlist_dialog
from prompt_toolkit.shortcuts.dialogs import message_dialog
from prompt_toolkit.shortcuts.dialogs import radiolist_dialog
from prompt_toolkit.shortcuts.dialogs import yes_no_dialog
from tap_producer import TAP

from ozi_core._i18n import TRANSLATION
from ozi_core.config import OziConfig
from ozi_core.config import read_user_config
from ozi_core.config import write_user_config
from ozi_core.fix.build_definition import walk
from ozi_core.fix.missing import get_relpath_expected_files
from ozi_core.fix.validate import RewriteCommandTargetValidator
from ozi_core.new.interactive.validator import validate_message
from ozi_core.ui._style import _style
from ozi_core.ui.defaults import COPYRIGHT_HEAD
from ozi_core.ui.defaults import FIX_PRETTY
from ozi_core.ui.defaults import FIX_STRICT
from ozi_core.ui.dialog import input_dialog
from ozi_core.ui.menu import MenuButton
from ozi_core.ui.menu import checkbox

if sys.platform != 'win32':  # pragma: no cover
    import curses
else:  # pragma: no cover
    curses = Mock()
    curses.tigetstr = lambda x: b''
    curses.setupterm = lambda: None

if TYPE_CHECKING:  # pragma: no cover
    from argparse import Namespace
    from pathlib import Path

global _
_ = TRANSLATION


def options_menu(  # pragma: no cover
    prompt: Any,
    output: dict[str, list[str]],
    prefix: dict[str, str],
) -> tuple[None | list[str] | bool, dict[str, list[str]], dict[str, str]]:
    _default: str | list[str] | None = None
    while True:
        match radiolist_dialog(
            title=_('fix-dlg-title'),
            text=_('opt-menu-title'),
            values=[
                (
                    'strict',
                    _('opt-menu-strict', value=checkbox(prompt.strict)),
                ),
                (
                    'pretty',
                    _('opt-menu-pretty', value=checkbox(prompt.pretty)),
                ),
                (
                    'update_wrapfile',
                    _('opt-menu-update-wrapfile', value=checkbox(prompt.update_wrapfile)),
                ),
                ('copyright_head', _('opt-menu-copyright-head')),
                (
                    'language',
                    _(
                        'opt-menu-language',
                        value=_(f'lang-{TRANSLATION.locale}'),
                    ),
                ),
            ],
            style=_style,
            cancel_text=_('btn-back'),
            ok_text=_('btn-ok'),
        ).run():
            case x if x and x in ('strict', 'pretty', 'update_wrapfile'):
                for i in (f'--{x.replace("_", "-")}', f'--no-{x.replace("_", "-")}'):
                    if i in output:
                        output.pop(i)
                setting = getattr(prompt, x)
                if setting is None:
                    setattr(prompt, x, False)
                else:
                    flag = '' if setting else 'no-'
                    output.update(
                        {
                            f'--{flag}{x.replace("_", "-")}': [
                                f'--{flag}{x.replace("_", "-")}',
                            ],
                        },
                    )
                    setattr(prompt, x, not setting)
            case x if x and x == 'copyright_head':
                _default = output.setdefault('--copyright-head', [COPYRIGHT_HEAD])
                result = input_dialog(
                    title=_('fix-dlg-title'),
                    text=_('opt-menu-copyright-head-input'),
                    style=_style,
                    cancel_text=_('btn-back'),
                    ok_text=_('btn-ok'),
                    default=_default[0],
                    multiline=True,
                ).run()
                if result in _default:
                    prompt.copyright_head = result
                    output.update({'--copyright-head': [prompt.copyright_head]})
            case x if x == 'language':
                result = radiolist_dialog(
                    title=_('fix-dlg-title'),
                    text=_('opt-menu-language-text'),
                    values=list(
                        zip(
                            TRANSLATION.data.keys(),
                            [_(f'lang-{i}') for i in {'en', 'zh'}],
                        ),
                    ),
                    cancel_text=_('btn-back'),
                    ok_text=_('btn-ok'),
                    default=TRANSLATION.locale,
                    style=_style,
                ).run()
                if result is not None:
                    TRANSLATION.locale = result
            case _:
                if yes_no_dialog(
                    title=_('fix-dlg-title'),
                    text=_('opt-menu-save-config'),
                    yes_text=_('btn-yes'),
                    no_text=_('btn-no'),
                    style=_style,
                ).run():
                    config = asdict(read_user_config())
                    config['fix'].update(
                        **{
                            k: v
                            for k, v in vars(prompt).items()
                            if k not in ['fix', 'target']
                        }
                    )
                    config['interactive'].update(language=TRANSLATION.locale)
                    write_user_config(OziConfig(**config))
                break
    return None, output, prefix


def main_menu(  # pragma: no cover
    prompt: Any,
    output: dict[str, list[str]],
    prefix: dict[str, str],
) -> tuple[None | list[str] | bool, dict[str, list[str]], dict[str, str]]:
    while True:
        match button_dialog(
            title=_('new-dlg-title'),
            text=_('main-menu-text'),
            buttons=[
                (_('btn-options'), MenuButton.OPTIONS.value),
                (_('btn-reset'), MenuButton.RESET.value),
                (_('btn-exit'), MenuButton.EXIT.value),
                (_('btn-back'), MenuButton.BACK.value),
            ],
            style=_style,
        ).run():
            case MenuButton.OPTIONS.value:
                result, output, prefix = options_menu(prompt, output, prefix)
                if isinstance(result, list):
                    return result, output, prefix
            case MenuButton.BACK.value:
                break
            case MenuButton.RESET.value:
                if yes_no_dialog(
                    title=_('new-dlg-title'),
                    text=_('main-menu-yn-reset'),
                    style=_style,
                    yes_text=_('btn-yes'),
                    no_text=_('btn-no'),
                ).run():
                    return ['interactive', '.'], output, prefix
            case MenuButton.EXIT.value:
                if yes_no_dialog(
                    title=_('new-dlg-title'),
                    text=_('main-menu-yn-exit'),
                    style=_style,
                    yes_text=_('btn-yes'),
                    no_text=_('btn-no'),
                ).run():
                    return ['-h'], output, prefix
    return None, output, prefix


class Prompt:
    def __init__(  # pragma: no cover
        self: Prompt,
        target: Path,
        strict: bool | None = None,
        pretty: bool | None = None,
        copyright_head: str | None = None,
        update_wrapfile: bool | None = None,
    ) -> None:
        self.target = target
        self.fix: str | None = 'root'
        self.strict = strict if strict is not None else FIX_STRICT
        self.pretty = pretty if pretty is not None else FIX_PRETTY
        self.copyright_head = (
            copyright_head if copyright_head is not None else COPYRIGHT_HEAD
        )
        self.update_wrapfile = update_wrapfile if update_wrapfile is not None else False
        TRANSLATION.locale = asdict(read_user_config())['interactive']['language']

    def set_fix_mode(  # pragma: no cover
        self: Prompt,
        project_name: str,
        output: dict[str, list[str]],
        prefix: dict[str, str],
    ) -> tuple[list[str] | str | bool | None, dict[str, list[str]], dict[str, str]]:
        while True:
            self.fix = radiolist_dialog(
                title=_('fix-dlg-title'),
                text=_('fix-add'),
                style=_style,
                cancel_text=_('btn-menu'),
                ok_text=_('btn-ok'),
                values=[('source', 'source'), ('test', 'test'), ('root', 'root')],
            ).run()
            if self.fix is not None:
                output['fix'].append(self.fix)
                return None, output, prefix
            else:
                result, output, prefix = main_menu(self, output, prefix)
                if result is not None:
                    return result, output, prefix

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
                title=_('fix-dlg-title'),
                text='\n'.join(
                    (
                        '\n'.join(iter(prefix)),
                        '\n',
                        _('fix-add-or-remove', projectname=project_name),
                    ),
                ),
                buttons=[
                    (_('btn-add'), MenuButton.ADD.value),
                    (_('btn-remove'), MenuButton.REMOVE.value),
                    (_('btn-menu'), MenuButton.MENU.value),
                    (_('btn-ok'), MenuButton.OK.value),
                ],
                style=_style,
            ).run():
                case MenuButton.ADD.value:
                    rel_path, __ = get_relpath_expected_files(self.fix, project_name)
                    files = []
                    with TAP.suppress():
                        for d in walk(self.target, rel_path, []):
                            for v in d.values():
                                files += [str(i) for i in v['missing']]
                    result: Any = checkboxlist_dialog(
                        title=_('fix-dlg-title'),
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
                                title=_('fix-dlg-title'),
                                cancel_text=_('btn-menu'),
                                style=_style,
                                validator=RewriteCommandTargetValidator(),
                            ).run()
                            if result is not None:
                                valid, errmsg = validate_message(
                                    result,
                                    RewriteCommandTargetValidator(),
                                )
                                if valid:
                                    add_files += [result]
                                    prefix.update(
                                        {
                                            f'Add-{self.fix}: {add_files}': (
                                                f'Add-{self.fix}: {add_files}'
                                            ),
                                        },
                                    )
                                    output['--add'].append(str(result))
                                else:
                                    message_dialog(
                                        title=_('fix-dlg-title'),
                                        text=_(
                                            'msg-input-invalid',
                                            value=result,
                                            errmsg=errmsg,
                                        ),
                                        style=_style,
                                        ok_text=_('btn-ok'),
                                    ).run()
                case MenuButton.REMOVE.value:
                    rel_path, __ = get_relpath_expected_files(self.fix, project_name)
                    files = []
                    with TAP.suppress():
                        for d in walk(self.target, rel_path, []):
                            for v in d.values():
                                files += [str(i) for i in v['found']]
                    result = checkboxlist_dialog(
                        title=_('fix-dlg-title'),
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
                                title=_('fix-dlg-title'),
                                cancel_text=_('btn-menu'),
                                style=_style,
                                validator=RewriteCommandTargetValidator(),
                            ).run()
                            if result is not None:
                                valid, errmsg = validate_message(
                                    result,
                                    RewriteCommandTargetValidator(),
                                )
                                if valid:
                                    rem_files += [result]
                                    prefix.update(
                                        {
                                            f'Remove-{self.fix}: {rem_files}': (
                                                f'Remove-{self.fix}: {rem_files}'
                                            ),
                                        },
                                    )
                                    output['--remove'].append(str(result))
                                else:
                                    message_dialog(
                                        title=_('fix-dlg-title'),
                                        text=_(
                                            'msg-input-invalid',
                                            value=result,
                                            errmsg=errmsg,
                                        ),
                                        style=_style,
                                        ok_text=_('btn-ok'),
                                    ).run()
                case MenuButton.OK.value:
                    break
                case MenuButton.MENU.value:
                    result, output, prefix = main_menu(self, output, prefix)
                    if result is not None:
                        return result, output, prefix
        return None, output, prefix


def interactive_prompt(project: Namespace) -> list[str]:  # pragma: no cover # noqa: C901
    ret_args = []
    with suppress(UnsupportedOperation):
        curses.setupterm()
        e3 = curses.tigetstr('E3') or b''
        clear_screen_seq = curses.tigetstr('clear') or b''
        os.write(sys.stdout.fileno(), e3 + clear_screen_seq)
    p = Prompt(project.target, **asdict(read_user_config())['fix'])
    result, output, prefix = p.set_fix_mode(
        project_name=project.name,
        output={'fix': []},
        prefix={},
    )
    if isinstance(result, list):
        return result
    result, output, prefix = p.add_or_remove(
        project_name=project.name,
        output=output,
        prefix=prefix,
    )
    if isinstance(result, list):
        return result
    fix = output.pop('fix')
    for k, v in output.items():
        for i in v:
            if len(i) > 0:
                ret_args += [k, i]
    return fix + ret_args + ['--interactive-io', '.']
