from __future__ import annotations

import sys
from typing import TYPE_CHECKING
from typing import Any
from typing import Sequence
from typing import TypeVar

from ozi_spec import METADATA  # pyright: ignore
from prompt_toolkit import Application  # pyright: ignore
from prompt_toolkit.application.current import get_app  # pyright: ignore
from prompt_toolkit.filters import Condition  # pyright: ignore
from prompt_toolkit.filters import FilterOrBool  # pyright: ignore
from prompt_toolkit.key_binding import KeyBindings  # pyright: ignore
from prompt_toolkit.key_binding import merge_key_bindings  # pyright: ignore
from prompt_toolkit.key_binding.bindings.focus import focus_next  # pyright: ignore
from prompt_toolkit.key_binding.bindings.focus import focus_previous  # pyright: ignore
from prompt_toolkit.key_binding.defaults import load_key_bindings  # pyright: ignore
from prompt_toolkit.layout import ConditionalMargin  # pyright: ignore
from prompt_toolkit.layout import Dimension as D  # pyright: ignore
from prompt_toolkit.layout import HSplit  # pyright: ignore
from prompt_toolkit.layout import Layout  # pyright: ignore
from prompt_toolkit.layout import ScrollbarMargin  # pyright: ignore
from prompt_toolkit.layout import Window  # pyright: ignore
from prompt_toolkit.layout.controls import FormattedTextControl  # pyright: ignore
from prompt_toolkit.shortcuts import button_dialog  # pyright: ignore
from prompt_toolkit.shortcuts import checkboxlist_dialog  # pyright: ignore
from prompt_toolkit.shortcuts import message_dialog  # pyright: ignore
from prompt_toolkit.shortcuts import radiolist_dialog  # pyright: ignore
from prompt_toolkit.shortcuts import yes_no_dialog  # pyright: ignore
from prompt_toolkit.styles import BaseStyle  # pyright: ignore
from prompt_toolkit.styles import Style  # pyright: ignore
from prompt_toolkit.validation import DynamicValidator  # pyright: ignore
from prompt_toolkit.validation import Validator  # pyright: ignore
from prompt_toolkit.widgets import Button  # pyright: ignore
from prompt_toolkit.widgets import Dialog  # pyright: ignore
from prompt_toolkit.widgets import Label  # pyright: ignore
from prompt_toolkit.widgets import RadioList
from prompt_toolkit.widgets import TextArea
from prompt_toolkit.widgets.toolbars import ValidationToolbar

from ozi_core._i18n import TRANSLATION
from ozi_core.new.interactive._style import _style
from ozi_core.new.interactive._style import _style_dict
from ozi_core.new.interactive.validator import LengthValidator
from ozi_core.new.interactive.validator import NotReservedValidator
from ozi_core.new.interactive.validator import PackageValidator
from ozi_core.new.interactive.validator import ProjectNameValidator
from ozi_core.new.interactive.validator import validate_message
from ozi_core.trove import Prefix
from ozi_core.trove import from_prefix

if TYPE_CHECKING:

    from prompt_toolkit.buffer import Buffer  # pyright: ignore
    from prompt_toolkit.completion import Completer  # pyright: ignore
    from prompt_toolkit.formatted_text import AnyFormattedText  # pyright: ignore
    from prompt_toolkit.key_binding.key_processor import KeyPressEvent  # pyright: ignore

    if sys.version_info >= (3, 11):
        from typing import Self
    elif sys.version_info < (3, 11):
        from typing_extensions import Self


def checkbox(checked: bool) -> str:
    if checked:
        return '☑'
    else:
        return '☐'


class Project:  # pragma: no cover
    def __init__(
        self,  # noqa: ANN101,RUF100
        allow_file: list[str] | None = None,
        ci_provider: str | None = None,
        copyright_head: str | None = None,
        enable_cython: bool = False,
        enable_uv: bool = False,
        github_harden_runner: bool = False,
        strict: bool = True,
        verify_email: bool = False,
    ) -> None:
        self.allow_file = allow_file
        self.ci_provider = ci_provider
        self.copyright_head = copyright_head
        self.enable_cython = enable_cython
        self.enable_uv = enable_uv
        self.github_harden_runner = github_harden_runner
        self.strict = strict
        self.verify_email = verify_email

    def name(  # noqa: C901,RUF100
        self: Self,
        output: dict[str, list[str]],
        prefix: dict[str, str],
        check_package_exists: bool = True,
    ) -> tuple[None | list[str] | str | bool, dict[str, list[str]], dict[str, str]]:

        def _check_package_exists() -> Validator:
            if check_package_exists:
                return NotReservedValidator(ProjectNameValidator())
            else:
                return ProjectNameValidator()

        while True:
            result, output, prefix = self.header_input(
                'Name',
                output,
                prefix,
                TRANSLATION('pro-name'),
                validator=DynamicValidator(_check_package_exists),
            )
            if result is True:
                return prefix.get('Name', '').replace('Name', '').strip(': '), output, prefix
            if isinstance(result, list):
                return result, output, prefix

    def summary(
        self: Self,
        project_name: str,
        output: dict[str, list[str]],
        prefix: dict[str, str],
    ) -> tuple[None | list[str] | str | bool, dict[str, list[str]], dict[str, str]]:
        while True:
            result, output, prefix = self.header_input(
                'Summary',
                output,
                prefix,
                TRANSLATION('pro-summary', projectname=project_name),
                validator=LengthValidator(),
            )
            if result is True:
                return result, output, prefix
            if isinstance(result, list):
                return result, output, prefix

    def keywords(
        self: Self,
        project_name: str,
        output: dict[str, list[str]],
        prefix: dict[str, str],
    ) -> tuple[None | list[str] | str | bool, dict[str, list[str]], dict[str, str]]:
        while True:
            result, output, prefix = self.header_input(
                'Keywords',
                output,
                prefix,
                TRANSLATION('pro-keywords', projectname=project_name),
                validator=LengthValidator(),
            )
            if result is True:
                return result, output, prefix
            if isinstance(result, list):
                return result, output, prefix

    def license_file(
        self: Self,
        project_name: str,
        output: dict[str, list[str]],
        prefix: dict[str, str],
    ) -> tuple[None | list[str] | str | bool, dict[str, list[str]], dict[str, str]]:
        while True:
            result = radiolist_dialog(
                values=(('LICENSE.txt', 'LICENSE.txt'),),
                title=TRANSLATION('dlg-title'),
                text=TRANSLATION('pro-license-file', projectname=project_name),
                style=_style,
                default='LICENSE.txt',
                ok_text=TRANSLATION('btn-ok'),
                cancel_text=TRANSLATION('btn-back'),
            ).run()
            if result is not None:
                output.update(
                    {'--license-file': [result] if isinstance(result, str) else []}
                )
            prefix.update(
                (
                    {
                        'License-File ::': f'License-File :: {result}',  # noqa: B950, RUF100, E501
                    }
                    if result
                    else {}
                ),
            )

    def home_page(
        self: Self,
        project_name: str,
        output: dict[str, list[str]],
        prefix: dict[str, str],
    ) -> tuple[None | list[str] | str | bool, dict[str, list[str]], dict[str, str]]:
        while True:
            result, output, prefix = self.header_input(
                'Home-page',
                output,
                prefix,
                TRANSLATION('pro-homepage', projectname=project_name),
                validator=LengthValidator(),
            )
            if result is True:
                return result, output, prefix
            if isinstance(result, list):
                return result, output, prefix

    def author(
        self: Self,
        project_name: str,
        output: dict[str, list[str]],
        prefix: dict[str, str],
    ) -> tuple[None | list[str] | str | bool, dict[str, list[str]], dict[str, str]]:
        while True:
            result, output, prefix = self.header_input(
                'Author',
                output,
                prefix,
                TRANSLATION('pro-author', projectname=project_name),
                validator=LengthValidator(),
                split_on=',',
            )
            if result is True:
                return result, output, prefix
            if isinstance(result, list):
                return result, output, prefix

    def author_email(
        self: Self,
        project_name: str,
        output: dict[str, list[str]],
        prefix: dict[str, str],
    ) -> tuple[None | list[str] | str | bool, dict[str, list[str]], dict[str, str]]:
        while True:
            result, output, prefix = self.header_input(
                'Author-email',
                output,
                prefix,
                TRANSLATION('pro-author-email', projectname=project_name),
                validator=LengthValidator(),
                split_on=',',
            )
            if result is True:
                return result, output, prefix
            if isinstance(result, list):
                return result, output, prefix

    def license_(  # noqa: C901,RUF100
        self: Self,
        project_name: str,
        output: dict[str, list[str]],
        prefix: dict[str, str],
    ) -> tuple[None | list[str] | str, dict[str, list[str]], dict[str, str]]:
        _default = output.setdefault('--license', [])
        while True:
            license_ = radiolist_dialog(
                values=sorted(
                    (zip(from_prefix(Prefix().license), from_prefix(Prefix().license))),
                ),
                title=TRANSLATION('dlg-title'),
                text=TRANSLATION('pro-license', projectname=project_name),
                style=_style,
                default=_default,
                cancel_text=TRANSLATION('btn-menu'),
                ok_text=TRANSLATION('btn-ok'),
            ).run()
            if license_ is None:
                result, output, prefix = self.menu_loop(output, prefix)
                if isinstance(result, list):
                    output.update({'--license': _default})
                    return result, output, prefix
            else:
                if validate_message(
                    license_ if license_ and isinstance(license_, str) else '',
                    LengthValidator(),
                )[0]:
                    break
                message_dialog(
                    style=_style,
                    title=TRANSLATION('dlg-title'),
                    text=TRANSLATION(
                        'msg-invalid-input',
                        value=license_ if license_ and isinstance(license_, str) else '',
                        errmsg='',
                    ),
                    ok_text=TRANSLATION('btn-ok'),
                ).run()
        prefix.update(
            {f'{Prefix().license}': f'{Prefix().license}{license_ if license_ else ""}'},
        )
        if isinstance(license_, str):
            output.update({'--license': [license_]})
        else:
            output.update({'--license': _default})
        return str(license_), output, prefix

    def license_expression(  # noqa: C901
        self: Self,
        project_name: str,
        _license: str,
        output: dict[str, list[str]],
        prefix: dict[str, str],
    ) -> tuple[None | list[str] | str, dict[str, list[str]], dict[str, str]]:
        _license_expression: str = ''
        while True:
            _possible_spdx: Sequence[str] | None = (
                METADATA.spec.python.pkg.license.ambiguous.get(
                    _license,
                    None,
                )
            )
            possible_spdx: Sequence[str] = _possible_spdx if _possible_spdx else ['']
            _default = output.setdefault('--license-expression', [possible_spdx[0]])

            if len(possible_spdx) < 1:
                _license_expression = input_dialog(
                    title=TRANSLATION('dlg-title'),
                    text=TRANSLATION(
                        'pro-license-expression-input',
                        license=_license,
                        projectname=project_name,
                    ),
                    default=_default[0],
                    style=_style,
                    cancel_text=TRANSLATION('btn-skip'),
                ).run()
            elif len(possible_spdx) == 1:
                _license_expression = input_dialog(
                    title=TRANSLATION('dlg-title'),
                    text=TRANSLATION(
                        'pro-license-expression-input',
                        license=_license,
                        projectname=project_name,
                    ),
                    default=_default[0],
                    style=_style,
                    cancel_text=TRANSLATION('btn-skip'),
                    ok_text=TRANSLATION('btn-ok'),
                ).run()
            else:
                license_id = radiolist_dialog(
                    values=sorted(zip(possible_spdx, possible_spdx)),
                    title=TRANSLATION('dlg-title'),
                    text=TRANSLATION(
                        'pro-license-expression-radio',
                        license=_license,
                        projectname=project_name,
                    ),
                    style=_style,
                    cancel_text=TRANSLATION('btn-menu'),
                    ok_text=TRANSLATION('btn-ok'),
                ).run()
                if license_id is None:
                    output.update({'--license-expression': _default})
                    result, output, prefix = self.menu_loop(output, prefix)
                    if isinstance(result, list):
                        return result, output, prefix
                else:
                    _license_expression = input_dialog(
                        title=TRANSLATION('dlg-title'),
                        text=TRANSLATION(
                            'pro-license-expression-input',
                            license=_license,
                            projectname=project_name,
                        ),
                        default=license_id,
                        style=_style,
                        cancel_text=TRANSLATION('btn-skip'),
                        ok_text=TRANSLATION('btn-ok'),
                    ).run()
                    if validate_message(license_id if license_id else '', LengthValidator())[
                        0
                    ]:
                        break
                    else:
                        message_dialog(
                            style=_style,
                            title=TRANSLATION('dlg-title'),
                            text=TRANSLATION(
                                'msg-invalid-input',
                                value=license_id,
                                errmsg='',
                            ),
                            ok_text=TRANSLATION('btn-ok'),
                        ).run()
            break
        if _license_expression:
            output.update({'--license-expression': [_license_expression]})
        else:
            output.update({'--license-expression': _default})
        prefix.update(
            {
                'License-Expression ::': f'License-Expression :: {_license_expression if _license_expression else ""}',  # pyright: ignore  # noqa: B950, RUF100, E501
            },
        )  # pyright: ignore  # noqa: B950, RUF100
        return _license_expression, output, prefix

    def maintainer(
        self: Self,
        project_name: str,
        output: dict[str, list[str]],
        prefix: dict[str, str],
    ) -> tuple[None | list[str] | str | bool, dict[str, list[str]], dict[str, str]]:
        while True:
            result, output, prefix = self.header_input(
                'Maintainer',
                output,
                prefix,
                TRANSLATION('pro-maintainer', projectname=project_name),
                validator=LengthValidator(),
                split_on=',',
            )
            if result is True:
                return result, output, prefix
            if isinstance(result, list):
                return result, output, prefix

    def maintainer_email(
        self: Self,
        project_name: str,
        output: dict[str, list[str]],
        prefix: dict[str, str],
    ) -> tuple[None | list[str] | str | bool, dict[str, list[str]], dict[str, str]]:
        while True:
            result, output, prefix = self.header_input(
                'Maintainer-email',
                output,
                prefix,
                TRANSLATION('pro-maintainer-email', projectname=project_name),
                validator=LengthValidator(),
                split_on=',',
            )
            if result is True:
                return result, output, prefix
            if isinstance(result, list):
                return result, output, prefix

    def requires_dist(
        self: Self,
        project_name: str,
        output: dict[str, list[str]],
        prefix: dict[str, str],
    ) -> tuple[list[str] | str | bool | None, dict[str, list[str]], dict[str, str]]:
        _requires_dist: list[str] = []
        output.setdefault('--requires-dist', [])
        while True:
            match button_dialog(
                title=TRANSLATION('dlg-title'),
                text='\n'.join(
                    (
                        'Requires-Dist:',
                        '\n'.join(_requires_dist),
                        '\n',
                        TRANSLATION('pro-requires-dist', projectname=project_name),
                    ),
                ),
                buttons=[
                    (TRANSLATION('pro-requires-dist-add'), True),
                    (TRANSLATION('pro-requires-dist-remove'), False),
                    (TRANSLATION('btn-ok'), 'ok'),
                    (TRANSLATION('btn-menu'), None),
                ],
                style=_style,
            ).run():
                case True:
                    requirement = input_dialog(
                        title=TRANSLATION('dlg-title'),
                        text=TRANSLATION('pro-requires-dist-search'),
                        validator=PackageValidator(),
                        style=_style,
                        cancel_text=TRANSLATION('btn-back'),
                    ).run()
                    if requirement:
                        _requires_dist += [requirement]
                        prefix.update(
                            {
                                f'Requires-Dist: {requirement}': (
                                    f'Requires-Dist: {requirement}'
                                ),
                            },
                        )
                        output['--requires-dist'].append(requirement)
                case False:
                    if len(_requires_dist) != 0:
                        del_requirement = checkboxlist_dialog(
                            title=TRANSLATION('dlg-title'),
                            text=TRANSLATION('pro-requires-dist-cbl-remove'),
                            values=list(zip(_requires_dist, _requires_dist)),
                            style=_style,
                            cancel_text=TRANSLATION('btn-back'),
                        ).run()
                        if del_requirement:
                            _requires_dist = list(
                                set(_requires_dist).symmetric_difference(
                                    set(del_requirement),
                                ),
                            )
                            for req in del_requirement:
                                output['--requires-dist'].remove(req)
                                prefix.pop(f'Requires-Dist: {req}')
                    else:
                        message_dialog(
                            title=TRANSLATION('dlg-title'),
                            text=TRANSLATION('pro-requires-dist-msg-remove-no-requirements'),
                            style=_style,
                            ok_text=TRANSLATION('btn-ok'),
                        ).run()
                case x if x and x == 'ok':
                    break
                case None:
                    result, output, prefix = self.menu_loop(output, prefix)
                    if result is not None:
                        return result, output, prefix
        return None, output, prefix

    def readme_type(
        self: Self,
        project_name: str,
        output: dict[str, list[str]],
        prefix: dict[str, str],
    ) -> tuple[str | list[str], dict[str, list[str]], dict[str, str]]:
        _default = output.setdefault('--readme-type', [])
        readme_type = radiolist_dialog(
            values=(
                ('rst', 'ReStructuredText'),
                ('md', 'Markdown'),
                ('txt', 'Plaintext'),
            ),
            title=TRANSLATION('dlg-title'),
            text=TRANSLATION('pro-readme-type', projectname=project_name),
            style=_style,
            default=_default,
            ok_text=TRANSLATION('btn-ok'),
            cancel_text=TRANSLATION('btn-back'),
        ).run()
        if readme_type is not None:
            output.update(
                {'--readme-type': [readme_type] if isinstance(readme_type, str) else []},
            )
        else:
            output.update({'--readme-type': _default})
        prefix.update(
            (
                {
                    'Description-Content-Type:': f'Description-Content-Type: {readme_type}',  # noqa: B950, RUF100, E501
                }
                if readme_type
                else {}
            ),
        )
        return str(readme_type), output, prefix

    def typing(
        self: Self,
        project_name: str,
        output: dict[str, list[str]],
        prefix: dict[str, str],
    ) -> tuple[str | list[str], dict[str, list[str]], dict[str, str]]:
        _default = output.setdefault('--typing', [])
        result = radiolist_dialog(
            values=(
                ('Typed', TRANSLATION('pro-typing-radio-typed')),
                ('Stubs Only', TRANSLATION('pro-typing-radio-stubs-only')),
            ),
            title=TRANSLATION('dlg-title'),
            text=TRANSLATION('pro-typing', projectname=project_name),
            style=_style,
            ok_text=TRANSLATION('btn-ok'),
            default=_default,
            cancel_text=TRANSLATION('btn-back'),
        ).run()
        if result is not None:
            output.update({'--typing': [result] if isinstance(result, str) else []})
        else:
            output.update({'--typing': _default})
        prefix.update(
            (
                {
                    'Typing ::': f'Typing :: {result}',  # noqa: B950, RUF100, E501
                }
                if result
                else {}
            ),
        )
        return str(result), output, prefix

    def project_urls(
        self: Self,
        project_name: str,
        output: dict[str, list[str]],
        prefix: dict[str, str],
    ) -> tuple[str, dict[str, list[str]], dict[str, str]]:
        _default = output.setdefault('--project-url', [])
        url = None
        while True:
            result = checkboxlist_dialog(
                values=(
                    (
                        TRANSLATION('pro-project-urls-cbl-changelog'),
                        TRANSLATION('pro-project-urls-cbl-changelog'),
                    ),
                    (
                        TRANSLATION('pro-project-urls-cbl-documentation'),
                        TRANSLATION('pro-project-urls-cbl-documentation'),
                    ),
                    (
                        TRANSLATION('pro-project-urls-cbl-bug-report'),
                        TRANSLATION('pro-project-urls-cbl-bug-report'),
                    ),
                    (
                        TRANSLATION('pro-project-urls-cbl-funding'),
                        TRANSLATION('pro-project-urls-cbl-funding'),
                    ),
                    (
                        TRANSLATION('pro-project-urls-cbl-source'),
                        TRANSLATION('pro-project-urls-cbl-source'),
                    ),
                ),
                title=TRANSLATION('dlg-title'),
                text=TRANSLATION('pro-project-urls-cbl', projectname=project_name),
                style=_style,
                ok_text=TRANSLATION('btn-ok'),
                cancel_text=TRANSLATION('btn-back'),
            ).run()
            if result is not None:
                for i in result:
                    url = input_dialog(
                        title=TRANSLATION('dlg-title'),
                        text=TRANSLATION(
                            'pro-project-urls-input',
                            urltype=i,
                            projectname=project_name,
                        ),
                        ok_text=TRANSLATION('btn-ok'),
                        cancel_text=TRANSLATION('btn-back'),
                        default='https://',
                        style=_style,
                    ).run()
                    if url is None:
                        break
                    output['--project-url'].append(f'{i}, {url}')
                    prefix.update(
                        (
                            {
                                f'Project-URL: {i}': f'Project-URL: {i}, {url}',  # noqa: B950, RUF100, E501
                            }
                            if i
                            else {}
                        ),
                    )
                continue
            else:
                output.update({'--project-url': _default})
                break

        return f'{result}, {url}', output, prefix

    def header_input(
        self: Self,
        label: str,
        output: dict[str, list[str]],
        prefix: dict[str, str],
        *args: str,
        validator: Validator | None = None,
        split_on: str | None = None,
    ) -> tuple[
        bool | None | list[str],
        dict[str, list[str]],
        dict[str, str],
    ]:  # pragma: no cover
        _default = output.setdefault(f'--{label.lower()}', [])
        header = input_dialog(
            title=TRANSLATION('dlg-title'),
            text='\n'.join(args),
            validator=validator,
            default=_default[0] if len(_default) > 0 else '',
            style=_style,
            cancel_text=TRANSLATION('btn-menu'),
            ok_text=TRANSLATION('btn-ok'),
        ).run()
        if header is None:
            output.update(
                {
                    f'--{label.lower()}': _default if len(_default) > 0 else [],
                },
            )
            result, output, prefix = self.menu_loop(output, prefix)
            return result, output, prefix
        else:
            if validator is not None:
                valid, errmsg = validate_message(header, validator)
                if valid:
                    prefix.update({label: f'{label}: {header}'})
                    if split_on:
                        output.update(
                            {f'--{label.lower()}': header.rstrip(split_on).split(split_on)},
                        )
                    else:
                        output.update({f'--{label.lower()}': [header]})
                    return True, output, prefix
                message_dialog(
                    title=TRANSLATION('dlg-title'),
                    text=TRANSLATION('msg-input-invalid', value=header, errmsg=errmsg),
                    style=_style,
                    ok_text=TRANSLATION('btn-ok'),
                ).run()
            output.update(
                {f'--{label.lower()}': _default if len(_default) > 0 else []},
            )
        return None, output, prefix

    def menu_loop(
        self: Project,
        output: dict[str, list[str]],
        prefix: dict[str, str],
    ) -> tuple[
        None | list[str] | bool,
        dict[str, list[str]],
        dict[str, str],
    ]:  # pragma: no cover
        while True:
            _default: str | list[str] | None = None
            match button_dialog(
                title=TRANSLATION('dlg-title'),
                text=TRANSLATION('main-menu-text'),
                buttons=[
                    (TRANSLATION('main-menu-btn-metadata'), 1),
                    (TRANSLATION('main-menu-btn-options'), 0),
                    (TRANSLATION('main-menu-btn-reset'), False),
                    (TRANSLATION('btn-exit'), None),
                    (TRANSLATION('main-menu-btn-edit'), -1),
                    (TRANSLATION('btn-back'), True),
                ],
                style=_style,
            ).run():
                case True:
                    break
                case False:
                    if yes_no_dialog(
                        title=TRANSLATION('dlg-title'),
                        text=TRANSLATION('main-menu-yn-reset'),
                        style=_style,
                        yes_text=TRANSLATION('btn-yes'),
                        no_text=TRANSLATION('btn-no'),
                    ).run():
                        return ['interactive', '.'], output, prefix
                case None:
                    if yes_no_dialog(
                        title=TRANSLATION('dlg-title'),
                        text=TRANSLATION('main-menu-yn-exit'),
                        style=_style,
                        yes_text=TRANSLATION('btn-yes'),
                        no_text=TRANSLATION('btn-no'),
                    ).run():
                        return [], output, prefix
                case -1:
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
                                break
                            case x if x and isinstance(x, str):
                                project_name = (
                                    prefix.get('Name', '').replace('Name', '').strip(': ')
                                )
                                match x:
                                    case x if x == 'name':
                                        result, output, prefix = self.name(output, prefix)
                                        if isinstance(result, list):
                                            return result, output, prefix
                                    case x if x == 'license_expression':
                                        result, output, prefix = self.license_expression(
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
                                        result, output, prefix = self.license_(
                                            project_name,
                                            output,
                                            prefix,
                                        )
                                        if isinstance(result, str):
                                            result, output, prefix = self.license_expression(
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
                                                key=TRANSLATION('edit-menu-btn-' + x),
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
                                        result, output, prefix = getattr(self, x)(
                                            project_name,
                                            output,
                                            prefix,
                                        )
                                        if isinstance(result, list):
                                            return result, output, prefix
                case 0:
                    while True:
                        match radiolist_dialog(
                            title=TRANSLATION('dlg-title'),
                            text=TRANSLATION('opt-menu-title'),
                            values=[
                                (
                                    'enable_cython',
                                    TRANSLATION(
                                        'opt-menu-enable-cython',
                                        value=checkbox(self.enable_cython),
                                    ),
                                ),
                                (
                                    'enable_uv',
                                    TRANSLATION(
                                        'opt-menu-enable-uv',
                                        value=checkbox(self.enable_uv),
                                    ),
                                ),
                                (
                                    'github_harden_runner',
                                    TRANSLATION(
                                        'opt-menu-github-harden-runner',
                                        value=checkbox(self.github_harden_runner),
                                    ),
                                ),
                                (
                                    'strict',
                                    TRANSLATION(
                                        'opt-menu-strict', value=checkbox(self.strict)
                                    ),
                                ),
                                (
                                    'verify_email',
                                    TRANSLATION(
                                        'opt-menu-verify-email',
                                        value=checkbox(self.verify_email),
                                    ),
                                ),
                                ('allow_file', TRANSLATION('opt-menu-allow-file')),
                                ('ci_provider', TRANSLATION('opt-menu-ci-provider')),
                                ('copyright_head', TRANSLATION('opt-menu-copyright-head')),
                                (
                                    'language',
                                    TRANSLATION(
                                        'opt-menu-language',
                                        value=TRANSLATION('lang-' + TRANSLATION.locale),
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
                                setting = getattr(self, x)
                                if setting is None:
                                    setattr(self, x, True)
                                else:
                                    flag = '' if not setting else 'no-'
                                    output.update(
                                        {
                                            f'--{flag}{x.replace("_", "-")}': [
                                                f'--{flag}{x.replace("_", "-")}',
                                            ],
                                        },
                                    )
                                    setattr(self, x, not setting)
                            case x if x and x == 'strict':
                                for i in ('--strict', '--no-strict'):
                                    if i in output:
                                        output.pop(i)
                                setting = getattr(self, x)
                                if setting is None:
                                    setattr(self, x, False)
                                else:
                                    flag = '' if setting else 'no-'
                                    output.update(
                                        {
                                            f'--{flag}{x.replace("_", "-")}': [
                                                f'--{flag}{x.replace("_", "-")}',
                                            ],
                                        },
                                    )
                                    setattr(self, x, not setting)
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
                                    self.copyright_head = result
                                    output.update(
                                        {'--copyright-head': [self.copyright_head]}
                                    )
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
                                    self.allow_file = [i.strip() for i in result.split(',')]
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
                                    self.ci_provider = result
                                    output.update({'--ci-provider': [self.ci_provider]})
                            case x if x == 'language':
                                result = radiolist_dialog(
                                    title=TRANSLATION('dlg-title'),
                                    text=TRANSLATION('opt-menu-language-text'),
                                    values=list(
                                        zip(
                                            TRANSLATION.data.keys(),
                                            [
                                                TRANSLATION('lang-' + i)
                                                for i in TRANSLATION.data.keys()
                                            ],
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
                case 1:
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


_T = TypeVar('_T')


class Admonition(RadioList[_T]):
    """Simple scrolling text dialog."""

    open_character = ''
    close_character = ''
    container_style = 'class:admonition-list'
    default_style = 'class:admonition'
    selected_style = 'class:admonition-selected'
    checked_style = 'class:admonition-checked'
    multiple_selection = False

    def __init__(  # noqa: C901
        self,  # noqa: ANN101,RUF100
        values: Sequence[tuple[_T, Any]],
        default: _T | None = None,
    ) -> None:  # pragma: no cover
        super().__init__(values, default)
        kb = KeyBindings()

        @kb.add('pageup')
        def _pageup(event: KeyPressEvent) -> None:
            w = event.app.layout.current_window
            if w.render_info:
                self._selected_index = max(
                    0,
                    self._selected_index - len(w.render_info.displayed_lines),
                )

        @kb.add('pagedown')
        def _pagedown(event: KeyPressEvent) -> None:
            w = event.app.layout.current_window
            if w.render_info:
                self._selected_index = min(
                    len(self.values) - 1,
                    self._selected_index + len(w.render_info.displayed_lines),
                )

        @kb.add('up')
        def _up(event: KeyPressEvent) -> None:
            _pageup(event)

        @kb.add('down')
        def _down(event: KeyPressEvent) -> None:
            _pagedown(event)

        @kb.add('enter')
        @kb.add(' ')
        def _click(event: KeyPressEvent) -> None:
            self._handle_enter()

        self.control = FormattedTextControl(
            self._get_text_fragments,
            key_bindings=kb,
            focusable=True,
        )

        self.window = Window(
            content=self.control,
            style=self.container_style,
            right_margins=[
                ConditionalMargin(
                    margin=ScrollbarMargin(display_arrows=True),
                    filter=Condition(lambda: self.show_scrollbar),
                ),
            ],
            dont_extend_height=True,
            wrap_lines=True,
            always_hide_cursor=True,
        )

    def _handle_enter(self) -> None:  # noqa: ANN101,RUF100
        pass  # pragma: no cover


def _return_none() -> None:
    """Button handler that returns None."""
    get_app().exit()


def admonition_dialog(  # noqa: C901
    title: str = '',
    text: str = '',
    heading_label: str = '',
    ok_text: str | None = None,
    cancel_text: str | None = None,
    style: BaseStyle | None = None,
) -> Application[list[Any]]:  # pragma: no cover
    """Admonition dialog shortcut.
    The focus can be moved between the list and the Ok/Cancel button with tab.
    """
    if ok_text is None:
        ok_text = TRANSLATION('btn-ok')
    if cancel_text is None:
        cancel_text = TRANSLATION('btn-exit')

    if style is None:
        style_dict = _style_dict
        style_dict.update(
            {
                'dialog.body admonition-list': '#e1e7ef',
                'dialog.body admonition': '#e1e7ef',
                'dialog.body admonition-selected': '#030711',
                'dialog.body admonition-checked': '#030711',
            },
        )
        style = Style.from_dict(style_dict)

    def ok_handler() -> None:
        get_app().exit(result=True)

    lines = text.splitlines()

    cb_list = Admonition(values=list(zip(lines, lines)), default=None)
    longest_line = len(max(lines, key=len))
    dialog = Dialog(
        title=title,
        body=HSplit(
            [Label(text=heading_label, dont_extend_height=True), cb_list],
            padding=1,
        ),
        buttons=[
            Button(text=ok_text, handler=ok_handler),
            Button(text=cancel_text, handler=_return_none),
        ],
        with_background=True,
        width=min(max(longest_line + 8, 40), 80),
    )
    bindings = KeyBindings()
    bindings.add('tab')(focus_next)
    bindings.add('s-tab')(focus_previous)

    return Application(
        layout=Layout(dialog),
        key_bindings=merge_key_bindings([load_key_bindings(), bindings]),
        mouse_support=True,
        style=style,
        full_screen=True,
    )


def input_dialog(
    title: AnyFormattedText = '',
    text: AnyFormattedText = '',
    ok_text: str | None = None,
    cancel_text: str | None = None,
    completer: Completer | None = None,
    validator: Validator | None = None,
    password: FilterOrBool = False,
    style: BaseStyle | None = None,
    default: str = '',
) -> Application[str]:
    """
    Display a text input box.
    Return the given text, or None when cancelled.
    """
    if ok_text is None:
        ok_text = TRANSLATION('btn-ok')
    if cancel_text is None:
        cancel_text = TRANSLATION('btn-back')

    def accept(buf: Buffer) -> bool:
        get_app().layout.focus(ok_button)
        return True  # Keep text.

    def ok_handler() -> None:
        get_app().exit(result=textfield.text)

    ok_button = Button(text=ok_text, handler=ok_handler)
    cancel_button = Button(text=cancel_text, handler=_return_none)
    lines = default.splitlines()
    longest_line = len(max(lines, key=len)) if len(lines) > 0 else 40
    textfield = TextArea(
        text=default,
        multiline=True,
        password=password,
        completer=completer,
        validator=validator,
        accept_handler=accept,
        height=max(len(lines), 1),
        width=min(max(longest_line + 8, 40), 80),
    )

    dialog = Dialog(
        title=title,
        body=HSplit(
            [
                Label(text=text, dont_extend_height=True),
                textfield,
                ValidationToolbar(),
            ],
            padding=D(preferred=1, max=1),
        ),
        buttons=[ok_button, cancel_button],
        with_background=True,
    )
    bindings = KeyBindings()
    bindings.add('tab')(focus_next)
    bindings.add('s-tab')(focus_previous)

    return Application(
        layout=Layout(dialog),
        key_bindings=merge_key_bindings([load_key_bindings(), bindings]),
        mouse_support=True,
        style=style,
        full_screen=True,
    )
