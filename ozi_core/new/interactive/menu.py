from __future__ import annotations

from dataclasses import asdict
from typing import Any

from ozi_spec import METADATA
from prompt_toolkit.shortcuts import button_dialog  # pyright: ignore
from prompt_toolkit.shortcuts import checkboxlist_dialog  # pyright: ignore
from prompt_toolkit.shortcuts import radiolist_dialog  # pyright: ignore
from prompt_toolkit.shortcuts import yes_no_dialog  # pyright: ignore

from ozi_core._i18n import TRANSLATION
from ozi_core.config import OziConfig
from ozi_core.config import read_user_config
from ozi_core.config import write_user_config
from ozi_core.trove import Prefix
from ozi_core.trove import from_prefix
from ozi_core.ui._style import _style
from ozi_core.ui.dialog import admonition_dialog
from ozi_core.ui.dialog import input_dialog
from ozi_core.ui.menu import MenuButton
from ozi_core.ui.menu import checkbox


def main_menu(  # pragma: no cover
    project: Any,
    output: dict[str, list[str]],
    prefix: dict[str, str],
) -> tuple[None | list[str] | bool, dict[str, list[str]], dict[str, str]]:
    while True:
        match button_dialog(
            title=TRANSLATION('new-dlg-title'),
            text=TRANSLATION('main-menu-text'),
            buttons=[
                MenuButton.METADATA._tuple,
                MenuButton.OPTIONS._tuple,
                MenuButton.RESET._tuple,
                MenuButton.EXIT._tuple,
                MenuButton.EDIT._tuple,
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
                    return [], output, prefix
            case MenuButton.EDIT.value:
                result, output, prefix = edit_menu(project, output, prefix)
                if isinstance(result, list):
                    return result, output, prefix
            case MenuButton.OPTIONS.value:
                result, output, prefix = options_menu(project, output, prefix)
                if isinstance(result, list):
                    return result, output, prefix
            case MenuButton.METADATA.value:
                if admonition_dialog(
                    title=TRANSLATION('new-dlg-title'),
                    heading_label=TRANSLATION('adm-metadata'),
                    text='\n'.join(
                        prefix.values() if len(prefix) > 0 else {'Name:': 'Name:'},
                    ),
                    ok_text=MenuButton.PROMPT._str,
                    cancel_text=MenuButton.BACK._str,
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
            title=TRANSLATION('new-dlg-title'),
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
            cancel_text=MenuButton.BACK._str,
            ok_text=MenuButton.OK._str,
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
                    title=TRANSLATION('new-dlg-title'),
                    text=TRANSLATION('opt-menu-copyright-head-input'),
                    style=_style,
                    cancel_text=MenuButton.BACK._str,
                    ok_text=MenuButton.OK._str,
                    default=_default[0],
                    multiline=True,
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
                    title=TRANSLATION('new-dlg-title'),
                    text=TRANSLATION('opt-menu-allow-file-input'),
                    style=_style,
                    cancel_text=MenuButton.BACK._str,
                    ok_text=MenuButton.OK._str,
                    default=','.join(_default),
                ).run()
                if result != ','.join(_default) and result is not None:
                    project.allow_file = [i.strip() for i in result.split(',')]
                    output.update({'--allow-file': [result]})
            case x if x and x == 'ci_provider':
                _default = output.setdefault('--ci-provider', ['github'])
                result = radiolist_dialog(
                    title=TRANSLATION('new-dlg-title'),
                    text=TRANSLATION('opt-menu-ci-provider-input'),
                    values=[('github', 'GitHub')],
                    cancel_text=MenuButton.BACK._str,
                    ok_text=MenuButton.OK._str,
                    default=_default[0],
                    style=_style,
                ).run()
                if result in _default and result is not None:
                    project.ci_provider = result
                    output.update({'--ci-provider': [project.ci_provider]})
            case x if x == 'language':
                result = radiolist_dialog(
                    title=TRANSLATION('new-dlg-title'),
                    text=TRANSLATION('opt-menu-language-text'),
                    values=list(
                        zip(
                            TRANSLATION.data.keys(),
                            [TRANSLATION(f'lang-{i}') for i in TRANSLATION.data.keys()],
                        ),
                    ),
                    cancel_text=MenuButton.BACK._str,
                    ok_text=MenuButton.OK._str,
                    default=TRANSLATION.locale,
                    style=_style,
                ).run()
                if result is not None:
                    TRANSLATION.locale = result
            case _:
                if yes_no_dialog(
                    title=TRANSLATION('new-dlg-title'),
                    text=TRANSLATION('opt-menu-save-config'),
                    yes_text=MenuButton.YES._str,
                    no_text=MenuButton.NO._str,
                    style=_style,
                ).run():
                    config = asdict(read_user_config())
                    config['new'].update(**vars(project))
                    config['interactive'].update(language=TRANSLATION.locale)
                    write_user_config(OziConfig(**config))
                break
    return None, output, prefix


def edit_menu(  # pragma: no cover
    project: Any,
    output: dict[str, list[str]],
    prefix: dict[str, str],
) -> tuple[None | list[str] | bool, dict[str, list[str]], dict[str, str]]:
    while True:
        match radiolist_dialog(
            title=TRANSLATION('new-dlg-title'),
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
            cancel_text=MenuButton.BACK._str,
            ok_text=MenuButton.OK._str,
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
                        config = asdict(read_user_config())
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
                            title=TRANSLATION('new-dlg-title'),
                            text=TRANSLATION(
                                'pro-classifier-cbl',
                                key=TRANSLATION(f'edit-menu-btn-{x}'),
                            ),
                            default_values=(
                                config['new']['language'] if x == 'language' else None
                            ),
                            style=_style,
                            ok_text=MenuButton.OK._str,
                            cancel_text=MenuButton.BACK._str,
                        ).run()
                        if classifier is not None:
                            for i in classifier:
                                output[f'--{x}'].append(i)
                                if x in ['language']:
                                    config['new'].update(
                                        {x: output[f'--{x}']} | vars(project)
                                    )
                                    write_user_config(OziConfig(**config))
                        prefix.update(
                            (
                                {
                                    f'{header}': f'{header}{classifier}',
                                }
                                if classifier
                                else {}
                            ),
                        )
                    case x if x and x in (
                        'author',
                        'author_email',
                        'maintainer',
                        'maintainer_email',
                        'readme_type',
                    ):
                        result, output, prefix = getattr(project, x)(
                            project_name,
                            output,
                            prefix,
                        )
                        if isinstance(result, list):
                            return result, output, prefix
                        if yes_no_dialog(
                            title=TRANSLATION('new-dlg-title'),
                            text=TRANSLATION('opt-menu-save-config'),
                            yes_text=MenuButton.YES._str,
                            no_text=MenuButton.NO._str,
                            style=_style,
                        ).run():
                            config = asdict(read_user_config())
                            config['new'].update(
                                {x: output[f'--{x.replace("_", "-")}'][0]} | vars(project)
                            )
                            write_user_config(OziConfig(**config))
                    case x:
                        result, output, prefix = getattr(project, x)(
                            project_name,
                            output,
                            prefix,
                        )
                        if isinstance(result, list):
                            return result, output, prefix
