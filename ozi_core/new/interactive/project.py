from __future__ import annotations

from dataclasses import asdict
from typing import TYPE_CHECKING

from ozi_spec import METADATA
from prompt_toolkit.shortcuts import button_dialog  # pyright: ignore
from prompt_toolkit.shortcuts import checkboxlist_dialog  # pyright: ignore
from prompt_toolkit.shortcuts import message_dialog  # pyright: ignore
from prompt_toolkit.shortcuts import radiolist_dialog  # pyright: ignore
from prompt_toolkit.shortcuts.dialogs import yes_no_dialog  # pyright: ignore
from prompt_toolkit.validation import DynamicValidator  # pyright: ignore
from prompt_toolkit.validation import Validator  # pyright: ignore

from ozi_core._i18n import TRANSLATION
from ozi_core.config import read_user_config
from ozi_core.new.interactive.menu import main_menu
from ozi_core.new.interactive.validator import LengthValidator
from ozi_core.new.interactive.validator import NotReservedValidator
from ozi_core.new.interactive.validator import PackageValidator
from ozi_core.new.interactive.validator import ProjectNameValidator
from ozi_core.new.interactive.validator import validate_message
from ozi_core.trove import Prefix
from ozi_core.trove import from_prefix
from ozi_core.ui._style import _style
from ozi_core.ui.dialog import admonition_dialog
from ozi_core.ui.dialog import input_dialog
from ozi_core.ui.menu import MenuButton

if TYPE_CHECKING:  # pragma: no cover
    from collections.abc import Sequence


class Project:  # pragma: no cover
    def __init__(  # noqa: DC104,ANN101,RUF100
        self: Project,
        allow_file: list[str] | None = None,
        ci_provider: str | None = None,
        copyright_head: str | None = None,
        enable_cython: bool | None = None,
        enable_uv: bool | None = None,
        github_harden_runner: bool | None = None,
        strict: bool | None = None,
        verify_email: bool | None = None,
        check_package_exists: bool | None = None,
        update_wrapfile: bool | None = None,
    ) -> None:
        self.allow_file = allow_file
        self.ci_provider = ci_provider
        self.copyright_head = copyright_head
        self.enable_cython = enable_cython if enable_cython is not None else False
        self.enable_uv = enable_uv if enable_uv is not None else False
        self.github_harden_runner = (
            github_harden_runner if github_harden_runner is not None else False
        )
        self.strict = strict if strict is not None else True
        self.verify_email = verify_email if verify_email is not None else False
        self.check_package_exists = (
            check_package_exists if check_package_exists is not None else True
        )
        self.update_wrapfile = update_wrapfile if update_wrapfile is not None else False
        TRANSLATION.locale = asdict(read_user_config())['interactive']['language']

    def __call__(self: Project) -> list[str]:  # noqa: C901  # pragma: no cover
        """Start the interactive prompt."""
        if (
            admonition_dialog(
                title=TRANSLATION('new-dlg-title'),
                heading_label=TRANSLATION('adm-disclaimer-title'),
                text=TRANSLATION('adm-disclaimer-text'),
            ).run()
            is None
        ):
            return []

        prefix: dict[str, str] = {}
        output: dict[str, list[str]] = {}
        project_name = '""'

        result, output, prefix = self.name(output, prefix)
        if isinstance(result, list):
            return result
        if isinstance(result, str):
            project_name = result

        for i in ('summary', 'keywords', 'author', 'author_email'):
            result, output, prefix = getattr(self, i)(project_name, output, prefix)
            if isinstance(result, list):
                return result

        result, output, prefix = self.license_(project_name, output, prefix)
        if isinstance(result, list):
            return result
        _license = result if result else ''

        result, output, prefix = self.license_expression(
            project_name,
            _license,
            output,
            prefix,
        )
        if isinstance(result, list):
            return result

        if yes_no_dialog(
            title=TRANSLATION('new-dlg-title'),
            text=TRANSLATION('adm-maintainers', project_name=project_name),
            style=_style,
            yes_text=MenuButton.YES._str,
            no_text=MenuButton.NO._str,
        ).run():
            result, output, prefix = self.maintainer(project_name, output, prefix)
            if isinstance(result, list):
                return result

            result, output, prefix = self.maintainer_email(project_name, output, prefix)
            if isinstance(result, list):
                return result

        result, output, prefix = self.requires_dist(project_name, output, prefix)
        if isinstance(result, list):
            return result

        while not admonition_dialog(
            title=TRANSLATION('new-dlg-title'),
            heading_label=TRANSLATION('adm-confirm'),
            text='\n'.join(prefix.values()),
            ok_text=MenuButton.OK._str,
            cancel_text=MenuButton.MENU._str,
        ).run():
            result, output, prefix = main_menu(self, output, prefix)
            if isinstance(result, list):
                return result

        ret_args = ['project']

        for k, v in output.items():
            for i in v:
                if len(i) > 0:
                    ret_args += [k, i]
        return ret_args

    def _check_package_exists(self: Project) -> Validator:
        if self.check_package_exists:
            return NotReservedValidator(ProjectNameValidator())
        else:
            return ProjectNameValidator()

    def name(
        self: Project,
        output: dict[str, list[str]],
        prefix: dict[str, str],
    ) -> tuple[None | list[str] | str | bool, dict[str, list[str]], dict[str, str]]:
        while True:
            result, output, prefix = self.header_input(
                'Name',
                output,
                prefix,
                TRANSLATION('pro-name'),
                validator=DynamicValidator(self._check_package_exists),
            )
            if result is True:
                return prefix.get('Name', '').replace('Name', '').strip(': '), output, prefix
            if isinstance(result, list):
                return result, output, prefix

    def summary(
        self: Project,
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
        self: Project,
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
        self: Project,
        project_name: str,
        output: dict[str, list[str]],
        prefix: dict[str, str],
    ) -> tuple[None | list[str] | str | bool, dict[str, list[str]], dict[str, str]]:
        while True:
            result = radiolist_dialog(
                values=(('LICENSE.txt', 'LICENSE.txt'),),
                title=TRANSLATION('new-dlg-title'),
                text=TRANSLATION('pro-license-file', projectname=project_name),
                style=_style,
                default='LICENSE.txt',
                ok_text=MenuButton.OK._str,
                cancel_text=MenuButton.BACK._str,
            ).run()
            if result is not None:
                output.update(
                    {'--license-file': [result] if isinstance(result, str) else []},
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

    def author(
        self: Project,
        project_name: str,
        output: dict[str, list[str]],
        prefix: dict[str, str],
    ) -> tuple[None | list[str] | str | bool, dict[str, list[str]], dict[str, str]]:
        while True:
            config = asdict(read_user_config())
            key = config['new']['author']
            output['--author'] = [key] if key is not None else []
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
        self: Project,
        project_name: str,
        output: dict[str, list[str]],
        prefix: dict[str, str],
    ) -> tuple[None | list[str] | str | bool, dict[str, list[str]], dict[str, str]]:
        while True:
            config = asdict(read_user_config())
            key = config['new']['author_email']
            output['--author-email'] = [key] if key is not None else []
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
        self: Project,
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
                title=TRANSLATION('new-dlg-title'),
                text=TRANSLATION('pro-license', projectname=project_name),
                style=_style,
                default=_default,
                cancel_text=MenuButton.MENU._str,
                ok_text=MenuButton.OK._str,
            ).run()
            if license_ is None:
                result, output, prefix = main_menu(self, output, prefix)
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
                    title=TRANSLATION('new-dlg-title'),
                    text=TRANSLATION(
                        'msg-invalid-input',
                        value=license_ if license_ and isinstance(license_, str) else '',
                        errmsg='',
                    ),
                    ok_text=MenuButton.OK._str,
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
        self: Project,
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
                    title=TRANSLATION('new-dlg-title'),
                    text=TRANSLATION(
                        'pro-license-expression-input',
                        license=_license,
                        projectname=project_name,
                    ),
                    default=_default[0],
                    style=_style,
                    cancel_text=MenuButton.SKIP._str,
                ).run()
            elif len(possible_spdx) == 1:
                _license_expression = input_dialog(
                    title=TRANSLATION('new-dlg-title'),
                    text=TRANSLATION(
                        'pro-license-expression-input',
                        license=_license,
                        projectname=project_name,
                    ),
                    default=_default[0],
                    style=_style,
                    cancel_text=MenuButton.SKIP._str,
                    ok_text=MenuButton.OK._str,
                ).run()
            else:
                license_id = radiolist_dialog(
                    values=sorted(zip(possible_spdx, possible_spdx)),
                    title=TRANSLATION('new-dlg-title'),
                    text=TRANSLATION(
                        'pro-license-expression-radio',
                        license=_license,
                        projectname=project_name,
                    ),
                    style=_style,
                    cancel_text=MenuButton.MENU._str,
                    ok_text=MenuButton.OK._str,
                ).run()
                if license_id is None:
                    output.update({'--license-expression': _default})
                    result, output, prefix = main_menu(self, output, prefix)
                    if isinstance(result, list):
                        return result, output, prefix
                else:
                    _license_expression = input_dialog(
                        title=TRANSLATION('new-dlg-title'),
                        text=TRANSLATION(
                            'pro-license-expression-input',
                            license=_license,
                            projectname=project_name,
                        ),
                        default=license_id,
                        style=_style,
                        cancel_text=MenuButton.SKIP._str,
                        ok_text=MenuButton.OK._str,
                    ).run()
                    if validate_message(license_id if license_id else '', LengthValidator())[
                        0
                    ]:
                        break
                    else:
                        message_dialog(
                            style=_style,
                            title=TRANSLATION('new-dlg-title'),
                            text=TRANSLATION(
                                'msg-invalid-input',
                                value=license_id,
                                errmsg='',
                            ),
                            ok_text=MenuButton.OK._str,
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
        self: Project,
        project_name: str,
        output: dict[str, list[str]],
        prefix: dict[str, str],
    ) -> tuple[None | list[str] | str | bool, dict[str, list[str]], dict[str, str]]:
        while True:
            config = asdict(read_user_config())
            key = config['new']['maintainer']
            output['--maintainer'] = [key] if key is not None else []
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
        self: Project,
        project_name: str,
        output: dict[str, list[str]],
        prefix: dict[str, str],
    ) -> tuple[None | list[str] | str | bool, dict[str, list[str]], dict[str, str]]:
        while True:
            config = asdict(read_user_config())
            key = config['new']['maintainer_email']
            output['--maintainer-email'] = [key] if key is not None else []
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
        self: Project,
        project_name: str,
        output: dict[str, list[str]],
        prefix: dict[str, str],
    ) -> tuple[list[str] | str | bool | None, dict[str, list[str]], dict[str, str]]:
        _requires_dist: list[str] = []
        output.setdefault('--requires-dist', [])
        while True:
            match button_dialog(
                title=TRANSLATION('new-dlg-title'),
                text='\n'.join(
                    (
                        'Requires-Dist:',
                        '\n'.join(_requires_dist),
                        '\n',
                        TRANSLATION('pro-requires-dist', projectname=project_name),
                    ),
                ),
                buttons=[
                    MenuButton.ADD._tuple,
                    MenuButton.REMOVE._tuple,
                    MenuButton.OK._tuple,
                    MenuButton.MENU._tuple,
                ],
                style=_style,
            ).run():
                case MenuButton.ADD.value:
                    requirement = input_dialog(
                        title=TRANSLATION('new-dlg-title'),
                        text=TRANSLATION('pro-requires-dist-search'),
                        validator=PackageValidator(),
                        style=_style,
                        cancel_text=MenuButton.BACK._str,
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
                case MenuButton.REMOVE.value:
                    if len(_requires_dist) != 0:
                        del_requirement = checkboxlist_dialog(
                            title=TRANSLATION('new-dlg-title'),
                            text=TRANSLATION('pro-requires-dist-cbl-remove'),
                            values=list(zip(_requires_dist, _requires_dist)),
                            style=_style,
                            cancel_text=MenuButton.BACK._str,
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
                            title=TRANSLATION('new-dlg-title'),
                            text=TRANSLATION('pro-requires-dist-msg-remove-no-requirements'),
                            style=_style,
                            ok_text=MenuButton.OK._str,
                        ).run()
                case MenuButton.OK.value:
                    break
                case MenuButton.MENU.value:
                    result, output, prefix = main_menu(self, output, prefix)
                    if result is not None:
                        return result, output, prefix
        return None, output, prefix

    def readme_type(
        self: Project,
        project_name: str,
        output: dict[str, list[str]],
        prefix: dict[str, str],
    ) -> tuple[str | list[str], dict[str, list[str]], dict[str, str]]:
        config = asdict(read_user_config())
        key = config['new']['readme_type']
        _default = output.setdefault('--readme-type', [key] if key is not None else [])
        readme_type = radiolist_dialog(
            values=(
                ('rst', 'ReStructuredText'),
                ('md', 'Markdown'),
                ('txt', 'Plaintext'),
            ),
            title=TRANSLATION('new-dlg-title'),
            text=TRANSLATION('pro-readme-type', projectname=project_name),
            style=_style,
            default=_default,
            ok_text=MenuButton.OK._str,
            cancel_text=MenuButton.BACK._str,
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
        self: Project,
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
            title=TRANSLATION('new-dlg-title'),
            text=TRANSLATION('pro-typing', projectname=project_name),
            style=_style,
            ok_text=MenuButton.OK._str,
            default=_default,
            cancel_text=MenuButton.BACK._str,
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
        self: Project,
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
                        'Changelog',
                        TRANSLATION('pro-project-urls-cbl-changelog'),
                    ),
                    (
                        'Documentation',
                        TRANSLATION('pro-project-urls-cbl-documentation'),
                    ),
                    (
                        'Bug Report',
                        TRANSLATION('pro-project-urls-cbl-bug-report'),
                    ),
                    (
                        'Funding',
                        TRANSLATION('pro-project-urls-cbl-funding'),
                    ),
                    (
                        'Source',
                        TRANSLATION('pro-project-urls-cbl-source'),
                    ),
                ),
                title=TRANSLATION('new-dlg-title'),
                text=TRANSLATION('pro-project-urls-cbl', projectname=project_name),
                style=_style,
                ok_text=MenuButton.OK._str,
                cancel_text=MenuButton.BACK._str,
            ).run()
            if result is not None:
                for i in result:
                    urltype = f'pro-project-urls-cbl-{"-".join(map(str.lower, i.split()))}'
                    url = input_dialog(
                        title=TRANSLATION('new-dlg-title'),
                        text=TRANSLATION(
                            'pro-project-urls-input',
                            urltype=TRANSLATION(urltype),
                            projectname=project_name,
                        ),
                        ok_text=MenuButton.OK._str,
                        cancel_text=MenuButton.BACK._str,
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
        self: Project,
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
            title=TRANSLATION('new-dlg-title'),
            text='\n'.join(args),
            validator=validator,
            default=_default[0] if len(_default) > 0 else '',
            style=_style,
            cancel_text=MenuButton.MENU._str,
            ok_text=MenuButton.OK._str,
        ).run()
        if header is None:
            output.update(
                {
                    f'--{label.lower()}': _default if len(_default) > 0 else [],
                },
            )
            result, output, prefix = main_menu(self, output, prefix)
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
                    title=TRANSLATION('new-dlg-title'),
                    text=TRANSLATION('msg-input-invalid', value=header, errmsg=errmsg),
                    style=_style,
                    ok_text=MenuButton.OK._str,
                ).run()
            output.update(
                {f'--{label.lower()}': _default if len(_default) > 0 else []},
            )
        return None, output, prefix
