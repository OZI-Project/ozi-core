from __future__ import annotations

from enum import Enum
from enum import auto
from enum import unique
from typing import Any

from ozi_spec import METADATA
from prompt_toolkit.shortcuts import button_dialog  # pyright: ignore
from prompt_toolkit.shortcuts import checkboxlist_dialog  # pyright: ignore
from prompt_toolkit.shortcuts import radiolist_dialog  # pyright: ignore
from prompt_toolkit.shortcuts import yes_no_dialog  # pyright: ignore

from ozi_core._i18n import TRANSLATION
from ozi_core.new.interactive._style import _style
from ozi_core.new.interactive.dialog import admonition_dialog
from ozi_core.new.interactive.dialog import input_dialog
from ozi_core.trove import Prefix
from ozi_core.trove import from_prefix


def checkbox(checked: bool) -> str:  # pragma: no cover
    if checked:
        return '☑'
    else:
        return '☐'


@unique
class MenuButton(Enum):
    """Non-composable menu action enum."""

    ADD = auto()
    BACK = auto()
    EDIT = auto()
    EXIT = auto()
    MENU = auto()
    METADATA = auto()
    OK = auto()
    OPTIONS = auto()
    PROMPT = auto()
    REMOVE = auto()
    RESET = auto()


def main_menu(  # pragma: no cover
    project: Any,
    output: dict[str, list[str]],
    prefix: dict[str, str],
) -> tuple[None | list[str] | bool, dict[str, list[str]], dict[str, str]]:
    while True:
        match button_dialog(
            title=TRANSLATION('dlg-title'),
            text=TRANSLATION('main-menu-text'),
            buttons=[
                (TRANSLATION('main-menu-btn-metadata'), MenuButton.METADATA),
                (TRANSLATION('main-menu-btn-options'), MenuButton.OPTIONS),
                (TRANSLATION('main-menu-btn-reset'), MenuButton.RESET),
                (TRANSLATION('btn-exit'), MenuButton.EXIT),
                (TRANSLATION('main-menu-btn-edit'), MenuButton.EDIT),
                (TRANSLATION('btn-back'), MenuButton.BACK),
            ],
            style=_style,
        ).run():
            case MenuButton.BACK:
                break
            case MenuButton.RESET:
                if yes_no_dialog(
                    title=TRANSLATION('dlg-title'),
                    text=TRANSLATION('main-menu-yn-reset'),
                    style=_style,
                    yes_text=TRANSLATION('btn-yes'),
                    no_text=TRANSLATION('btn-no'),
                ).run():
                    return ['interactive', '.'], output, prefix
            case MenuButton.EXIT:
                if yes_no_dialog(
                    title=TRANSLATION('dlg-title'),
                    text=TRANSLATION('main-menu-yn-exit'),
                    style=_style,
                    yes_text=TRANSLATION('btn-yes'),
                    no_text=TRANSLATION('btn-no'),
                ).run():
                    return [], output, prefix
            case MenuButton.EDIT:
                result, output, prefix = edit_menu(project, output, prefix)
                if isinstance(result, list):
                    return result, output, prefix
            case MenuButton.OPTIONS:
                result, output, prefix = options_menu(project, output, prefix)
                if isinstance(result, list):
                    return result, output, prefix
            case MenuButton.METADATA:
                if admonition_dialog(
                    title=TRANSLATION('dlg-title'),
                    heading_label=TRANSLATION('adm-metadata'),
                    text='\n'.join(
                        prefix.values() if len(prefix) > 0 else {'Name:': 'Name:'},
                    ),
                    ok_text=TRANSLATION('btn-prompt'),
                    cancel_text=TRANSLATION('btn-back'),
                ).run():
                    break
    return None, output, prefix


def options_menu(  # pragma: no cover
    project: Any,
    output: dict[str, list[str]],
    prefix: dict[str, str],
) -> tuple[None | list[str] | bool, dict[str, list[str]], dict[str, str]]:
    _default: str | list[str] | None = None
    while True:
        match radiolist_dialog(
            title=TRANSLATION('dlg-title'),
            text=TRANSLATION('opt-menu-title'),
            values=[
                (
                    'enable_cython',
                    TRANSLATION(
                        'opt-menu-enable-cython',
                        value=checkbox(project.enable_cython),
                    ),
                ),
                (
                    'enable_uv',
                    TRANSLATION(
                        'opt-menu-enable-uv',
                        value=checkbox(project.enable_uv),
                    ),
                ),
                (
                    'github_harden_runner',
                    TRANSLATION(
                        'opt-menu-github-harden-runner',
                        value=checkbox(project.github_harden_runner),
                    ),
                ),
                (
                    'strict',
                    TRANSLATION('opt-menu-strict', value=checkbox(project.strict)),
                ),
                (
                    'verify_email',
                    TRANSLATION(
                        'opt-menu-verify-email',
                        value=checkbox(project.verify_email),
                    ),
                ),
                ('allow_file', TRANSLATION('opt-menu-allow-file')),
                ('ci_provider', TRANSLATION('opt-menu-ci-provider')),
                ('copyright_head', TRANSLATION('opt-menu-copyright-head')),
                (
                    'language',
                    TRANSLATION(
                        'opt-menu-language',
                        value=TRANSLATION(f'lang-{TRANSLATION.locale}'),
                    ),
                ),
            ],
            style=_style,
            cancel_text=TRANSLATION('btn-back'),
            ok_text=TRANSLATION('btn-ok'),
        ).run():
            case x if x and x in (
                'enable_cython',
                'enable_uv',
                'github_harden_runner',
                'verify_email',
            ):
                for i in (
                    f'--{x.replace("_", "-")}',
                    f'--no-{x.replace("_", "-")}',
                ):
                    if i in output:
                        output.pop(i)
                setting = getattr(project, x)
                if setting is None:
                    setattr(project, x, True)
                else:
                    flag = '' if not setting else 'no-'
                    output.update(
                        {
                            f'--{flag}{x.replace("_", "-")}': [
                                f'--{flag}{x.replace("_", "-")}',
                            ],
                        },
                    )
                    setattr(project, x, not setting)
            case x if x and x == 'strict':
                for i in ('--strict', '--no-strict'):
                    if i in output:
                        output.pop(i)
                setting = getattr(project, x)
                if setting is None:
                    setattr(project, x, False)
                else:
                    flag = '' if setting else 'no-'
                    output.update(
                        {
                            f'--{flag}{x.replace("_", "-")}': [
                                f'--{flag}{x.replace("_", "-")}',
                            ],
                        },
                    )
                    setattr(project, x, not setting)
            case x if x and x == 'copyright_head':
                _default = output.setdefault(
                    '--copyright-head',
                    [
                        'Part of {project_name}.\nSee LICENSE.txt in the project root for details.',  # noqa: B950, RUF100, E501
                    ],
                )
                result = input_dialog(
                    title=TRANSLATION('dlg-title'),
                    text=TRANSLATION('opt-menu-copyright-head-input'),
                    style=_style,
                    cancel_text=TRANSLATION('btn-back'),
                    ok_text=TRANSLATION('btn-ok'),
                    default=_default[0],
                ).run()
                if result in _default:
                    project.copyright_head = result
                    output.update({'--copyright-head': [project.copyright_head]})
            case x if x and x == 'allow_file':
                _default = output.setdefault(
                    '--allow-file',
                    list(METADATA.spec.python.src.allow_files),
                )
                result = input_dialog(
                    title=TRANSLATION('dlg-title'),
                    text=TRANSLATION('opt-menu-allow-file-input'),
                    style=_style,
                    cancel_text=TRANSLATION('btn-back'),
                    ok_text=TRANSLATION('btn-ok'),
                    default=','.join(_default),
                ).run()
                if result != ','.join(_default) and result is not None:
                    project.allow_file = [i.strip() for i in result.split(',')]
                    output.update({'--allow-file': [result]})
            case x if x and x == 'ci_provider':
                _default = output.setdefault('--ci-provider', ['github'])
                result = radiolist_dialog(
                    title=TRANSLATION('dlg-title'),
                    text=TRANSLATION('opt-menu-ci-provider-input'),
                    values=[('github', 'GitHub')],
                    cancel_text=TRANSLATION('btn-back'),
                    ok_text=TRANSLATION('btn-ok'),
                    default=_default[0],
                    style=_style,
                ).run()
                if result in _default and result is not None:
                    project.ci_provider = result
                    output.update({'--ci-provider': [project.ci_provider]})
            case x if x == 'language':
                result = radiolist_dialog(
                    title=TRANSLATION('dlg-title'),
                    text=TRANSLATION('opt-menu-language-text'),
                    values=list(
                        zip(
                            TRANSLATION.data.keys(),
                            [TRANSLATION(f'lang-{i}') for i in TRANSLATION.data.keys()],
                        ),
                    ),
                    cancel_text=TRANSLATION('btn-back'),
                    ok_text=TRANSLATION('btn-ok'),
                    default=TRANSLATION.locale,
                    style=_style,
                ).run()
                if result is not None:
                    TRANSLATION.locale = result
            case _:
                break
    return None, output, prefix


def edit_menu(  # pragma: no cover
    project: Any,
    output: dict[str, list[str]],
    prefix: dict[str, str],
) -> tuple[None | list[str] | bool, dict[str, list[str]], dict[str, str]]:
    while True:
        match radiolist_dialog(
            title=TRANSLATION('dlg-title'),
            text=TRANSLATION('edit-menu-text'),
            values=[
                ('name', TRANSLATION('edit-menu-btn-name')),
                ('summary', TRANSLATION('edit-menu-btn-summary')),
                ('keywords', TRANSLATION('edit-menu-btn-keywords')),
                ('home_page', TRANSLATION('edit-menu-btn-homepage')),
                ('author', TRANSLATION('edit-menu-btn-author')),
                ('author_email', TRANSLATION('edit-menu-btn-email')),
                ('license_', TRANSLATION('edit-menu-btn-license')),
                (
                    'license_expression',
                    TRANSLATION('edit-menu-btn-license-expression'),
                ),
                ('license_file', TRANSLATION('edit-menu-btn-license-file')),
                ('maintainer', TRANSLATION('edit-menu-btn-maintainer')),
                (
                    'maintainer_email',
                    TRANSLATION('edit-menu-btn-maintainer-email'),
                ),
                ('project_urls', TRANSLATION('edit-menu-btn-project-url')),
                (
                    'requires_dist',
                    TRANSLATION('edit-menu-btn-requires-dist'),
                ),
                ('audience', TRANSLATION('edit-menu-btn-audience')),
                ('environment', TRANSLATION('edit-menu-btn-environment')),
                ('framework', TRANSLATION('edit-menu-btn-framework')),
                ('language', TRANSLATION('edit-menu-btn-language')),
                ('status', TRANSLATION('edit-menu-btn-status')),
                ('topic', TRANSLATION('edit-menu-btn-topic')),
                ('typing', TRANSLATION('edit-menu-btn-typing')),
                ('readme_type', TRANSLATION('edit-menu-btn-readme-type')),
            ],
            cancel_text=TRANSLATION('btn-back'),
            ok_text=TRANSLATION('btn-ok'),
            style=_style,
        ).run():
            case None:
                return None, output, prefix
            case x if x and isinstance(x, str):
                project_name = prefix.get('Name', '').replace('Name', '').strip(': ')
                match x:
                    case x if x == 'name':
                        result, output, prefix = project.name(output, prefix)
                        if isinstance(result, list):
                            return result, output, prefix
                    case x if x == 'license_expression':
                        result, output, prefix = project.license_expression(
                            project_name,
                            prefix.get(
                                'License',
                                '',
                            )
                            .replace(
                                'License',
                                '',
                            )
                            .strip(': '),
                            output,
                            prefix,
                        )
                        if isinstance(result, list):
                            return result, output, prefix
                    case x if x == 'license_':
                        result, output, prefix = project.license_(
                            project_name,
                            output,
                            prefix,
                        )
                        if isinstance(result, str):
                            result, output, prefix = project.license_expression(
                                project_name,
                                result,
                                output,
                                prefix,
                            )
                        if isinstance(result, list):  # pyright: ignore
                            return result, output, prefix
                    case x if x and x in (
                        'audience',
                        'environment',
                        'framework',
                        'language',
                        'status',
                        'topic',
                    ):
                        output.setdefault(f'--{x}', [])
                        header = getattr(Prefix(), x)
                        classifier = checkboxlist_dialog(
                            values=sorted(
                                (
                                    zip(
                                        from_prefix(header),
                                        from_prefix(header),
                                    )
                                ),
                            ),
                            title=TRANSLATION('dlg-title'),
                            text=TRANSLATION(
                                'pro-classifier-cbl',
                                key=TRANSLATION(f'edit-menu-btn-{x}'),
                            ),
                            style=_style,
                            ok_text=TRANSLATION('btn-ok'),
                            cancel_text=TRANSLATION('btn-back'),
                        ).run()
                        if classifier is not None:
                            for i in classifier:
                                output[f'--{x}'].append(i)
                        prefix.update(
                            (
                                {
                                    f'{header}': f'{header}{classifier}',
                                }
                                if classifier
                                else {}
                            ),
                        )
                    case x:
                        result, output, prefix = getattr(project, x)(
                            project_name,
                            output,
                            prefix,
                        )
                        if isinstance(result, list):
                            return result, output, prefix
