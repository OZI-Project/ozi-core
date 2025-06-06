import html
import re
from argparse import Namespace
from dataclasses import asdict
from datetime import datetime
from functools import partial
from logging import getLogger
from pathlib import Path
from typing import Any
from typing import Callable
from urllib.parse import urlparse

from ozi_spec import METADATA  # pyright: ignore
from ozi_spec._license import SPDX_LICENSE_EXCEPTIONS  # pyright: ignore
from ozi_templates import load_environment

from ozi_core._i18n import TRANSLATION
from ozi_core._logging import config_logger
from ozi_core.config import OziConfig
from ozi_core.config import read_user_config
from ozi_core.config import write_user_config
from ozi_core.trove import Prefix
from ozi_core.trove import from_prefix
from ozi_core.ui.defaults import COPYRIGHT_HEAD
from ozi_core.validate import pypi_package_exists
from ozi_core.vendor.email_validator import validate_email
from ozi_core.vendor.email_validator.exceptions_types import EmailNotValidError

# mock webui for pytest test discovery
try:
    from webui import webui  # type: ignore
except SystemExit:
    from unittest.mock import Mock
    webui = Mock()

config_logger()
__logger = getLogger(f'ozi_core.{__name__}')
_data: dict[str, str | list[str] | bool] = {}
global _
_ = TRANSLATION

OPTION_EMPTY = '<option value="" aria-hidden="true" selected disabled hidden></option>'
OPTION_SELECTED = '<option value="{0}" selected>{0}</option>'
OPTION = '<option value="{0}">{0}</option>'
AS_LIST_JS = """
    const elm = document.getElementById("{0}")
    var repr = [];
    for (const option of elm.selectedOptions) {{
        if (option.innerHTML != "") {{
            repr.push(option.innerHTML);
        }}
    }}
    return repr.join(';');
"""

def _validate_email(addr: str) -> bool:
    try:
        validate_email(addr)
    except EmailNotValidError as exc:
        return False
    else:
        return True


validators: dict[str, Callable[[str], bool]] = {
    'Name': lambda x: re.match(METADATA.spec.python.pkg.pattern.name, x) is not None,
    'Summary': lambda x: 0 < len(x) < 256,
    'Keywords': lambda x: re.match(r'^(([a-z_]*[a-z0-9],)*){2,650}$', x) is not None,
    'Author': lambda x: 0 < len(x) < 512,
    'Author-email': lambda x: all(map(_validate_email, x.split(','))),
    'Maintainer': lambda x: re.match(METADATA.spec.python.pkg.pattern.author, x) is not None,
    'Maintainer-email': lambda x: all(map(_validate_email, x.split(','))),
    'License': lambda _: True,
    'License-Expression': lambda _: True,
    'Project-URL': lambda x: True,
    'Requires-Dist': lambda x: True,
    'readme-type': lambda x: x in ['rst', 'md', 'txt'],
}

licenses = ''.join(
    [
        OPTION.format(i)
        for i in sorted(
            set(METADATA.spec.python.pkg.license.ambiguous.keys()).intersection(
                from_prefix(Prefix().license)
            )
        )
    ]
)
licenses = OPTION_EMPTY + licenses
audience_choices = ''.join(
    [
        (
            OPTION_SELECTED.format(i)
            if i in METADATA.spec.python.pkg.info.classifiers.intended_audience
            else OPTION.format(i)
        )
        for i in sorted(from_prefix(Prefix().audience))
    ]
)
environment_choices = ''.join(
    [
        (
            OPTION_SELECTED.format(i)
            if i in METADATA.spec.python.pkg.info.classifiers.environment
            else OPTION.format(i)
        )
        for i in sorted(from_prefix(Prefix().environment))
    ]
)
framework_choices = ''.join(
    [OPTION.format(i) for i in sorted(from_prefix(Prefix().framework))]
)
language_choices = ''.join(
    [
        (
            OPTION_SELECTED.format(i)
            if i in METADATA.spec.python.pkg.info.classifiers.language
            else OPTION.format(i)
        )
        for i in sorted(from_prefix(Prefix().language))
    ]
)
status_choices = ''.join(
    [
        (
            OPTION_SELECTED.format(i)
            if i in METADATA.spec.python.pkg.info.classifiers.development_status
            else OPTION.format(i)
        )
        for i in sorted(from_prefix(Prefix().status))
    ]
)
topic_choices = ''.join(
    [OPTION.format(i) for i in sorted(from_prefix(Prefix().topic))]
)
locales = [('en', _('lang-en')), ('zh', _('lang-zh'))]
locale_choices = ''.join(
    [f'<option id="locale-{k}" value="{k}">{v}</option>' for k, v in sorted(locales)]
)
 # translations meant for <textarea>
# should be text/plain;charset=UTF-8
TRANSLATION.mime_type = 'text/plain;charset=UTF-8'
disclaimer_text = _('adm-disclaimer-text')
# everything else should be text/html;charset=UTF-8
TRANSLATION.mime_type = 'text/html;charset=UTF-8'

_validators = validators.copy()
name_valid = _validators.pop('Name')


def validate_name(e: webui.event) -> None:
    projectname = '$projectname'
    res = e.window.script(  # pyright: ignore
        f' return document.getElementById("Name").value; '
    )
    _ = TRANSLATION.gettext
    if name_valid(res.data):
        projectname = res.data
    else:
        show_error(e, 'name', _('web-err-invalid-input'))
    TRANSLATION.mime_type = 'text/plain;charset=UTF-8'
    label_translation: dict[str, partial[str]] = {
        'Audience': _('pro-classifier-cbl', key=_('edit-menu-btn-audience')),
        'Author': _('pro-author', projectname=projectname),
        'Author-email': _('pro-author-email', projectname=projectname),
        'Environment': _('pro-classifier-cbl', key=_('edit-menu-btn-environment')
        ),
        'Framework': _('pro-classifier-cbl', key=_('edit-menu-btn-framework')
        ),
        'Keywords': _('pro-keywords', projectname=projectname),
        'Language': _('pro-classifier-cbl', key=_('edit-menu-btn-language')
        ),
        'License': _('pro-license'),
        'License-Exception': _('edit-menu-btn-license-exception'),
        'License-Expression': _('pro-license-expression'),
        'Maintainer': _('pro-maintainer', projectname=projectname),
        'Maintainer-email': _('pro-maintainer-email', projectname=projectname),
        'Name': _('pro-name'),
        'Project-URL': _('pro-project-urls-cbl', projectname=projectname),
        'Requires-Dist': _('pro-requires-dist', projectname=projectname),
        'Status': _('pro-classifier-cbl', key=_('edit-menu-btn-status')
        ),
        'Summary': _('pro-summary', projectname=projectname),
        'Topic': _('pro-classifier-cbl', key=_('edit-menu-btn-topic')
        ),
        'copyright-head': _('opt-menu-copyright-head-input'),
        'allow-file': _('opt-menu-allow-file-input'),
        'enable-cython': _('opt-menu-enable-cython', value=''),
        'enable-uv': _('opt-menu-enable-uv', value=''),
        'github-harden-runner': _('opt-menu-github-harden-runner', value=''),
        'locale': _('opt-menu-language-text'),
        'readme-type': _('pro-readme-type', projectname=projectname),
        'update-wrapfile': _('opt-menu-update-wrapfile', value=''),
        'strict': _('opt-menu-strict', value=''),
        'verify-email': _('opt-menu-verify-email', value=''),
        'PKG-INFO': _('adm-confirm'),
        'LicenseReader': _('edit-menu-btn-license-file')
    }
    for k in validators:
        res = e.window.script(  # pyright: ignore
            f" return document.getElementById(`label-{k.lower()}`).innerHTML; "
        )
        t = label_translation[k]
        if res.data == t:
            continue
        update_label(e, k, t)


def validate_input(e: webui.event, k: str) -> None:
    _ = TRANSLATION.gettext
    res = e.window.script(  # pyright: ignore
        f' return document.getElementById("{k}").value; '
    )
    if not validators[k](res.data):
        show_error(e, k.lower(), _('web-err-invalid-input'))
    if res.error is True:
        __logger.debug("JavaScript Error: " + res.data)


def validate_summary(e: webui.event) -> None:
    validate_input(e, 'Summary')


def validate_keywords(e: webui.event) -> None:
    validate_input(e, 'Keywords')


def validate_author(e: webui.event) -> None:
    validate_input(e, 'Author')


def validate_author_email(e: webui.event) -> None:
    validate_input(e, 'Author-email')


def validate_maintainer(e: webui.event) -> None:
    validate_input(e, 'Maintainer')


def validate_maintainer_email(e: webui.event) -> None:
    validate_input(e, 'Maintainer-email')


def load_license_expressions(e: webui.event) -> None:
    res = e.window.script(  # pyright: ignore
        f" return document.getElementById(`License`).selectedOptions[0].label "
    )
    spdx = ''.join(
        [
            OPTION.format(i)
            for i in sorted(
                METADATA.spec.python.pkg.license.ambiguous.get(res.data, tuple())
            )
        ]
    )
    spdx = OPTION_EMPTY + spdx
    e.window.script(  # pyright: ignore
        f"""
        document.getElementById(`License-Expression`).innerHTML = `{spdx}`;
        document.getElementById(`LicenseReader`).innerHTML = ``;
        """
    )


def update_label(e: webui.event, _id: str, v: str) -> None:
    e.window.run(  # pyright: ignore
        f" document.getElementById(`label-{_id.lower()}`).innerHTML = `{v}`; "
    )


def hide_error(e: webui.event, _id: str) -> None:
    e.window.run(  # pyright: ignore
        f"""
        document.getElementById(`err-{_id}`).style.display = `none`;
        document.getElementById(`err-{_id}`).innerHTML = `&nbsp;`;
        """
    )


def show_error(e: webui.event, _id: str, message: str) -> None:
    e.window.run(  # pyright: ignore
        f"""
        document.getElementById(`err-{_id}`).style.display = `contents`;
        document.getElementById(`err-{_id}`).innerHTML = `<wbr>[ ! ] {message}`;
        """
    )


def load_license_exceptions(e: webui.event) -> None:
    license_expr = e.window.script(  # pyright: ignore
        " return document.getElementById(`License-Expression`).value; "
    )
    exceptions = OPTION_EMPTY + ''.join(
        [
            OPTION.format(i)
            for i in sorted(
                tuple(
                    k
                    for k, v in SPDX_LICENSE_EXCEPTIONS.items()  # pyright: ignore
                    if license_expr.data in v
                )
            )
        ]
    )
    e.window.run(  # pyright: ignore
        f" document.getElementById(`License-Exception`).innerHTML = `{exceptions}` "
    )


def show_license_reader(e: webui.event) -> None:
    e.window.run(  # pyright: ignore
        ' document.getElementById(`LicenseReaderProgress`).style.display = "inline-block"; '
    )
    name = e.window.script(  # pyright: ignore
        f' return document.getElementById("Name").value; '
    )
    author = e.window.script(  # pyright: ignore
        f' return document.getElementById("Author").value; '
    )
    license_expr = e.window.script(  # pyright: ignore
        " return document.getElementById(`License-Expression`).value; "
    )
    license_ = e.window.script(  # pyright: ignore
        f" return document.getElementById(`License`).selectedOptions[0].label "
    )
    exception = e.window.script(  # pyright: ignore
        f" return document.getElementById(`License-Exception`).value; "
    )
    exception = exception.data if exception.data != '' else None
    jinja_env = load_environment(
        {
            'name': name.data,
            'copyright_year': str(datetime.now().year),
            'author': author.data,
            'license': license_.data,
            'license_expression': (
                license_expr.data
                if exception is None
                else f'{license_expr.data} with {exception}'
            ),
        },
        METADATA.asdict(),  # type: ignore
    )
    try:
        text = jinja_env.get_template('LICENSE.txt.j2').render()
    except Exception as exc:
        text = f'template not found: {exc}'
    license_file = html.escape(text.replace('${', '\\${').replace('`', "'"))
    e.window.run(  # pyright: ignore
        f"""
        document.getElementById(`LicenseReader`).innerHTML = `{license_file}`;
        document.getElementById(`LicenseReaderProgress`).style.display = "none";
        """
    )


def get_form_data(e: webui.event) -> dict[str, list[str]]:
    name = e.window.script(  # pyright: ignore
        f' return document.getElementById("Name").value; '
    )
    author = e.window.script(  # pyright: ignore
        f' return document.getElementById("Author").value; '
    )
    summary = e.window.script(  # pyright: ignore
        f' return document.getElementById("Summary").value; '
    )
    keywords = e.window.script(  # pyright: ignore
        f' return document.getElementById("Keywords").value; '
    )
    author_email = e.window.script(  # pyright: ignore
        f' return document.getElementById("Author-email").value; '
    )
    maintainer = e.window.script(  # pyright: ignore
        f' return document.getElementById("Maintainer").value; '
    )
    maintainer_email = e.window.script(  # pyright: ignore
        f' return document.getElementById("Maintainer-email").value; '
    )
    readme_type = e.window.script(  # pyright: ignore
        f' return document.getElementById("readme-type").value; '
    )
    status = e.window.script(  # pyright: ignore
        f' return document.getElementById("Status").value; '
    )
    copyright_head = e.window.script(  # pyright: ignore
        f' return document.getElementById("copyright-head").innerText; '
    )
    enable_cython = e.window.script(  # pyright: ignore
        f' return document.getElementById("enable-cython").checked; '
    )
    enable_uv = e.window.script(  # pyright: ignore
        f' return document.getElementById("enable-uv").checked; '
    )
    strict = e.window.script(  # pyright: ignore
        f' return document.getElementById("strict").checked; '
    )
    github_harden_runner = e.window.script(  # pyright: ignore
        f' return document.getElementById("github-harden-runner").checked; '
    )
    update_wrapfile = e.window.script(  # pyright: ignore
        f' return document.getElementById("update-wrapfile").checked; '
    )
    verify_email = e.window.script(  # pyright: ignore
        f' return document.getElementById("verify-email").checked; '
    )
    project_urls = e.window.script(AS_LIST_JS.format('EditProjectURL'))  # pyright: ignore
    requires_dist = e.window.script(AS_LIST_JS.format('EditRequiresDist'))  # pyright: ignore
    audience = e.window.script(AS_LIST_JS.format('Audience'))  # pyright: ignore
    environment = e.window.script(AS_LIST_JS.format('Environment'))  # pyright: ignore
    language = e.window.script(AS_LIST_JS.format('Language'))  # pyright: ignore
    framework = e.window.script(AS_LIST_JS.format('Framework'))  # pyright: ignore
    topic = e.window.script(AS_LIST_JS.format('Topic'))  # pyright: ignore
    allow_file = e.window.script(  # pyright: ignore
        f' return document.getElementById("allow-file").innerText; '
    )
    license_expr = e.window.script(  # pyright: ignore
        " return document.getElementById(`License-Expression`).value; "
    )
    license_ = e.window.script(  # pyright: ignore
        f" return document.getElementById(`License`).selectedOptions[0].label "
    )
    exception = e.window.script(  # pyright: ignore
        f" return document.getElementById(`License-Exception`).value; "
    )
    exception = exception.data if exception.data != '' else None
    env: dict[str, list[str]] = {}
    env |= {'maintainer': [i for i in maintainer.data.split(',')]} if maintainer.data else {}
    env |= (
        {'maintainer_email': [i for i in maintainer_email.data.split(',') if i]}
        if maintainer_email.data
        else {}
    )
    env |= {
        'name': name.data,
        'summary': summary.data,
        'keywords': [i.strip() for i in keywords.data.split(',')],
        'author': [i.strip() for i in author.data.split(',')],
        'maintainer': [i.strip() for i in maintainer.data.split(',')],
        'author_email': [i.strip() for i in author_email.data.split(',')],
        'maintainer_email': [i.strip() for i in maintainer_email.data.split(',')],
        'copyright_year': str(datetime.now().year),  # type: ignore
        'long_description_content_type': readme_type.data,
        'project_url': [i for i in project_urls.data.split(';') if i],
        'dist_requires': [i for i in requires_dist.data.split(';') if i],
        'audience': [i for i in audience.data.split(";") if i],
        'environment': [i for i in environment.data.split(";") if i],
        'language': [i for i in language.data.split(";") if i],
        'framework': [i for i in framework.data.split(";") if i],
        'topic': [i for i in topic.data.split(";") if i],
        'status': [status.data],
        'license': license_.data,
        'license_expression': (  # type: ignore
            license_expr.data
            if exception is None
            else f'{license_expr.data} with {exception}'
        ),
        'copyright_head': copyright_head.data,
        'allow_file': [i.strip() for i in allow_file.data.split(',') if i],
        'strict': strict.data == 'true',
        'enable_cython': enable_cython.data == 'true',
        'enable_uv': enable_uv.data == 'true',
        'verify_email': verify_email.data == 'true',
        'update_wrapfile': update_wrapfile.data == 'true',
        'github_harden_runner': github_harden_runner.data == 'true',
    }
    return env


def save_options(e: webui.event) -> None:
    config = asdict(read_user_config())
    new_config = get_form_data(e)
    new_config['readme_type'] = new_config.pop('long_description_content_type')
    new_config.pop('author')
    new_config.pop('author_email')
    new_config.pop('maintainer')
    new_config.pop('maintainer_email')
    config['new'].update(**new_config)
    config['interactive'].update(language=TRANSLATION.locale)
    write_user_config(OziConfig(**config))


def show_pkg_info(e: webui.event) -> None:
    jinja_env = load_environment(get_form_data(e), METADATA.asdict())  # type: ignore
    try:
        text = jinja_env.get_template('root.pyproject.toml').render()
    except Exception as exc:
        text = f'template not found: {exc}'
    text = html.escape(text.replace('${', '\\${').replace('`', "'"))
    e.window.run(  # pyright: ignore
        f"""
        document.getElementById(`PKG-INFO`).innerHTML = `{text}`;
        """
    )


def add_project_url(e: webui.event) -> None:
    _ = TRANSLATION.gettext
    url = e.window.script(  # pyright: ignore
        ' return document.getElementById(`Project-URL`).value; '
    )
    label = e.window.script(  # pyright: ignore
        ' return document.getElementById(`ProjectUrlType`).selectedOptions[0].label; '
    )
    name = e.window.script(  # pyright: ignore
        ' return document.getElementById(`ProjectUrlType`).selectedOptions[0].value; '
    )
    if label.data == '':
        show_error(
            e,
            'project-url',
            label.data + _('sp') + _('web-err-invalid-input'),
        )
        return
    parsed_url = urlparse(url.data)
    match parsed_url:
        case p if p.netloc == '':
            show_error(
                e,
                'project-url',
                label.data + _('sp') + _('term-tap-empty-netloc'),
            )
            return
    e.window.run(  # pyright: ignore
        f"""
        var edit = document.getElementById(`EditProjectURL`);
        var option = document.createElement("option");
        const optionLabels = Array.from(edit.options).map((opt) => opt.value);
        const optionText = document.createTextNode("{label.data}, {url.data}");
        option.appendChild(optionText);
        option.setAttribute('value', "{name.data}");
        const hasOption = optionLabels.includes("{name.data}");
        if (!hasOption) edit.add(option); 
        """
    )


def add_requires_dist(e: webui.event) -> None:
    _ = TRANSLATION.gettext
    requires_dist = e.window.script(  # pyright: ignore
        ' return document.getElementById(`Requires-Dist`).value; '
    )
    if requires_dist.data == '':
        show_error(
            e,
            'requires-dist',
            requires_dist.data + _('sp') + _('web-err-invalid-input'),
        )
        return
    if pypi_package_exists(requires_dist.data):
        e.window.run(  # pyright: ignore
            f"""
            var edit = document.getElementById(`EditRequiresDist`);
            var option = document.createElement("option");
            const optionLabels = Array.from(edit.options).map((opt) => opt.value);
            const optionText = document.createTextNode("{requires_dist.data}");
            option.appendChild(optionText);
            option.setAttribute('value', "{requires_dist.data}");
            const hasOption = optionLabels.includes("{requires_dist.data}");
            if (!hasOption) edit.add(option); 
            """
        )
    else:
        show_error(
            e,
            'requires-dist',
            requires_dist.data + _('sp') + _('err-pkg-not-found'),
        )


def update_ui_language(e: webui.event) -> None:
    locale = e.window.script(  # pyright: ignore
        ' return document.getElementById(`locale`).value; '
    )  # pyright: ignore
    TRANSLATION.locale = locale.data
    _ = TRANSLATION.gettext
    label_translation: dict[str, partial[str]] = {
        'Audience': _('pro-classifier-cbl', key=_('edit-menu-btn-audience')),
        'Author': _('pro-author'),
        'Author-email': _('pro-author-email'),
        'Environment': _('pro-classifier-cbl', key=_('edit-menu-btn-environment')
        ),
        'Framework': _('pro-classifier-cbl', key=_('edit-menu-btn-framework')
        ),
        'Keywords': _('pro-keywords'),
        'Language': _('pro-classifier-cbl', key=_('edit-menu-btn-language')
        ),
        'License': _('pro-license'),
        'License-Exception': _('edit-menu-btn-license-exception'),
        'License-Expression': _('pro-license-expression'),
        'Maintainer': _('pro-maintainer'),
        'Maintainer-email': _('pro-maintainer-email'),
        'Name': _('pro-name'),
        'Project-URL': _('pro-project-urls-cbl'),
        'Requires-Dist': _('pro-requires-dist'),
        'Status': _('pro-classifier-cbl', key=_('edit-menu-btn-status')
        ),
        'Summary': _('pro-summary'),
        'Topic': _('pro-classifier-cbl', key=_('edit-menu-btn-topic')
        ),
        'copyright-head': _('opt-menu-copyright-head-input'),
        'allow-file': _('opt-menu-allow-file-input'),
        'enable-cython': _('opt-menu-enable-cython', value=''),
        'enable-uv': _('opt-menu-enable-uv', value=''),
        'github-harden-runner': _('opt-menu-github-harden-runner', value=''),
        'locale': _('opt-menu-language-text'),
        'readme-type': _('pro-readme-type'),
        'update-wrapfile': _('opt-menu-update-wrapfile', value=''),
        'strict': _('opt-menu-strict', value=''),
        'verify-email': _('opt-menu-verify-email', value=''),
        'PKG-INFO': _('adm-confirm'),
        'LicenseReader': _('edit-menu-btn-license-file')
    }
    for k, v in label_translation.items():
        if k in validators:
            continue
        update_label(e, k, v)
    text_translation = {
        'AddProjectURL': _('btn-add'),
        'AddRequiresDist': _('btn-add'),
        'Disclaimer-title': _('adm-disclaimer-title'),
        'Ok': _('btn-ok'),
        'Options': _('btn-options'),
        'Options-title': _('btn-options'),
        'Page1': _('web-core-metadata'),
        'Page2': _('edit-menu-btn-license'),
        'Page4': _('term-create-project'),
        'RefreshButton': _('btn-refresh'),
        'RemoveProjectURL': _('btn-remove'),
        'RemoveRequiresDist': _('btn-remove'),
        'Reset': _('btn-reset'),
        'SaveOptions': _('btn-save'),
        'disclaimer-text': _('adm-disclaimer-text'),
        'input-options': _('term-input'),
        'locale-en': _('lang-en'),
        'locale-zh': _('lang-zh'),
        'output-options': _('term-output'),
        'readme-type-md': _('pro-readme-type-radio-md'),
        'readme-type-rst': _('pro-readme-type-radio-rst'),
        'readme-type-txt': _('pro-readme-type-radio-txt'),
        'user-interface-options': _('term-user-interface'),
        'output-options': _('term-output'),
        'label-locale': _('opt-menu-language-text'),
    }
    TRANSLATION.mime_type = 'text/plain;charset=UTF-8'
    _text_translation = text_translation.copy()
    _text_translation |= {
        'Page3': _("term-classifier")+_("sp")+_("term-metadata"),
    }
    for k, v in _text_translation.items():
        e.window.run(  # pyright: ignore
            f" document.getElementById(`{k}`).innerHTML = `{v}`; "
        )
    show_modal(e, _id='Disclaimer')
    TRANSLATION.mime_type = 'text/html;charset=UTF-8'


def remove_project_url(e: webui.event) -> None:
    e.window.run(  # pyright: ignore
        f"""
        var edit = document.getElementById(`EditProjectURL`);
        Array.from(edit.selectedOptions).forEach(opt => edit.remove(opt.index));
        """
    )


def remove_requires_dist(e: webui.event) -> None:
    e.window.run(  # pyright: ignore
        f"""
        var edit = document.getElementById(`EditRequiresDist`);
        Array.from(edit.selectedOptions).forEach(opt => edit.remove(opt.index));
        """
    )


def change_tab(e: webui.event) -> None:
    _ = TRANSLATION.gettext
    TRANSLATION.mime_type = 'text/plain;charset=UTF-8'
    e.window.run(  # pyright: ignore
        f"""
        const targetTab = document.getElementById("{e.element}");
        const tabHeading = document.getElementById("PageHeading")
        const tabTitle = targetTab.innerHTML;
        const tabList = targetTab.parentNode;
        const tabGroup = tabList.parentNode.parentNode;
        const titleSpan = document.createElement("span");
        const title1 = document.getElementById("Page1");
        const title2 = document.getElementById("Page2");
        const title3 = document.getElementById("Page3");
        const title4 = document.getElementById("Page4");
        const titleOptions = document.getElementById("Options");
        title1.innerHTML = "{_('web-core-metadata')}";
        title2.innerHTML = "{_('edit-menu-btn-license')}";
        title3.innerHTML = "{_("term-classifier")}{_("sp")}{_("term-metadata")}";
        title4.innerHTML = "{_('term-create-project')}";
        titleOptions.innerHTML = "{_('btn-options')}";
        titleSpan.innerHTML = tabTitle;
        tabHeading.innerHTML = tabTitle;
        targetTab.replaceChild(titleSpan, targetTab.childNodes[0]);
        
        // Hide all tab panels
        tabGroup
            .querySelectorAll(':scope > [role="tabpanel"]')
            .forEach((p) => p.setAttribute("hidden", true));
        tabList
            .querySelectorAll(':scope > [role="tab"]')
            .forEach((p) => p.setAttribute("tabindex", "0"));
        tabList
            .querySelectorAll(':scope > [role="tab"]')
            .forEach((p) => p.removeAttribute("aria-current"));
        tabList
            .querySelectorAll(':scope > [role="tab"]')
            .forEach((p) => p.removeAttribute("aria-disabled"));
        tabList
            .querySelectorAll(':scope > [role="tab"]')
            .forEach((p) => p.removeAttribute("aria-hidden"));
        // Show the selected panel
        tabGroup
            .querySelector(`#${{targetTab.getAttribute("aria-controls")}}`)
            .removeAttribute("hidden");
        // Set this tab as selected
        targetTab.setAttribute("aria-current", "page");
        targetTab.setAttribute("tabindex", "-1");
        targetTab.setAttribute("aria-disabled", true);
        targetTab.setAttribute("aria-hidden", true);
        """
    )
    TRANSLATION.mime_type = 'text/html;charset=UTF-8'
    validate_name(e)


def show_prompt4(e: webui.event) -> None:
    change_tab(e)
    show_pkg_info(e)


def show_modal(e: webui.event, _id: str | None = None) -> None:
    _id = _id if _id is not None else e.element
    e.window.run(  # pyright: ignore
        f"""
        const disclaimer = document.getElementById('{_id}');
        disclaimer.removeAttribute("hidden");
        disclaimer.removeAttribute("aria-hidden");
        disclaimer.classList.add("modal");
        """
    )


def hide_modal(e: webui.event, _id: str | None = None) -> None:
    _id = _id if _id is not None else e.element
    e.window.run(  # pyright: ignore
        f"""
        const disclaimer = document.getElementById('{_id}');
        disclaimer.setAttribute("hidden", true);
        disclaimer.setAttribute("aria-hidden", true);
        disclaimer.classList.remove("modal");
        """
    )


def hide_disclaimer(e: webui.event) -> None:
    hide_modal(e, _id='Disclaimer')


def hide_options(e: webui.event) -> None:
    hide_modal(e, _id='OptionsContents')


def show_options(e: webui.event) -> None:
    show_modal(e, _id='OptionsContents')


def create_project(e: webui.event) -> None:
    global _data
    _data.update(get_form_data(e))
    close_application(e)


def close_application(e: webui.event) -> None:
    webui.exit()


class WebInterface:

    def __init__(self, window: webui.window) -> None:
        window.set_root_folder(str(Path(__file__).parent.parent.resolve() / 'data'))
        self.window = window

    def __call__(self, config: dict[str, Any], show: str) -> None:
        TRANSLATION.mime_type = 'text/html;charset=UTF-8'
        if config['interactive']['language']:
            TRANSLATION.locale = config['interactive']['language']
        self.window.show(show)
        self.window.run(" document.getElementById('HideDisclaimer').checked = false; ")


def main(mode: str) -> Namespace:
    window = webui.window()
    config = asdict(read_user_config())
    if mode == 'new':
        window.bind('CloseDisclaimer', hide_disclaimer)
        window.bind('Name', validate_name)
        window.bind('Summary', validate_summary)
        window.bind('Keywords', validate_keywords)
        window.bind('Author', validate_author)
        window.bind('Author-email', validate_author_email)
        window.bind('Maintainer', validate_maintainer)
        window.bind('Maintainer-email', validate_maintainer_email)
        window.bind('Page1', change_tab)
        window.bind('Page2', change_tab)
        window.bind('Page3', change_tab)
        window.bind('Page4', show_prompt4)
        window.bind('Options', show_options)
        window.bind('AddRequiresDist', add_requires_dist)
        window.bind('RemoveRequiresDist', remove_requires_dist)
        window.bind('License', load_license_expressions)
        window.bind('License-Expression', load_license_exceptions)
        window.bind('RefreshButton', show_license_reader)
        window.bind('AddProjectURL', add_project_url)
        window.bind('RemoveProjectURL', remove_project_url)
        window.bind('locale-en', update_ui_language)
        window.bind('locale-zh', update_ui_language)
        window.bind('SaveOptions', save_options)
        window.bind('CloseOptions', hide_options)
        window.bind('Ok', create_project)
        interface = WebInterface(window)
        interface(config, f"""@OZI_NEW_HTML@""")
    elif mode == 'fix':
        interface = WebInterface(window)
        interface(config, f"""@OZI_FIX_HTML@""")
    # Wait until all windows are closed
    webui.wait()  # pyright: ignore
    TRANSLATION.mime_type = 'text/plain;charset=UTF-8'
    arg_data = _data.copy()
    for k, v in _data.items():
        if v == [] or v == [''] or v == '':
            arg_data.pop(k)
        elif isinstance(v, str):
            arg_data.update({k: v.replace('\n', r'\n')})
    return Namespace(**arg_data)


if __name__ == '__main__':

    print(main('new'))
