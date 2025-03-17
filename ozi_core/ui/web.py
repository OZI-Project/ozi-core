import html
import re
from dataclasses import asdict
from datetime import datetime
from functools import partial
from logging import getLogger
from typing import Callable
from urllib.parse import urlparse

from ozi_spec import METADATA  # pyright: ignore
from ozi_spec._license import SPDX_LICENSE_EXCEPTIONS  # pyright: ignore
from ozi_templates import load_environment
from webui import webui  # type: ignore

from ozi_core._i18n import TRANSLATION
from ozi_core._logging import config_logger
from ozi_core.config import OziConfig
from ozi_core.config import read_user_config
from ozi_core.config import write_user_config
from ozi_core.trove import Prefix
from ozi_core.trove import from_prefix
from ozi_core.ui.defaults import COPYRIGHT_HEAD
from ozi_core.vendor.email_validator import validate_email
from ozi_core.vendor.email_validator.exceptions_types import EmailNotValidError

config_logger()
__logger = getLogger(f'ozi_core.{__name__}')

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
    'readme-type': lambda x: x in ['rst', 'md', 'txt'],
}

label_translation: dict[str, partial[str]] = {
    'Audience': partial(
        TRANSLATION, 'pro-classifier-cbl', key=TRANSLATION('edit-menu-btn-audience')
    ),
    'Author': partial(TRANSLATION, 'pro-author'),
    'Author-email': partial(TRANSLATION, 'pro-author-email'),
    'Environment': partial(
        TRANSLATION, 'pro-classifier-cbl', key=TRANSLATION('edit-menu-btn-environment')
    ),
    'Framework': partial(
        TRANSLATION, 'pro-classifier-cbl', key=TRANSLATION('edit-menu-btn-framework')
    ),
    'Keywords': partial(TRANSLATION, 'pro-keywords'),
    'Language': partial(
        TRANSLATION, 'pro-classifier-cbl', key=TRANSLATION('edit-menu-btn-language')
    ),
    'License': partial(TRANSLATION, 'pro-license'),
    'License-Exception': partial(TRANSLATION, 'edit-menu-btn-license-exception'),
    'License-Expression': partial(TRANSLATION, 'pro-license-expression'),
    'Maintainer': partial(TRANSLATION, 'pro-maintainer'),
    'Maintainer-email': partial(TRANSLATION, 'pro-maintainer-email'),
    'Name': partial(TRANSLATION, 'pro-name'),
    'Project-URL': partial(TRANSLATION, 'pro-project-urls-cbl'),
    'Status': partial(
        TRANSLATION, 'pro-classifier-cbl', key=TRANSLATION('edit-menu-btn-status')
    ),
    'Summary': partial(TRANSLATION, 'pro-summary'),
    'Topic': partial(
        TRANSLATION, 'pro-classifier-cbl', key=TRANSLATION('edit-menu-btn-topic')
    ),
    'copyright-head': partial(TRANSLATION, 'opt-menu-copyright-head-input'),
    'allow-file': partial(TRANSLATION, 'opt-menu-allow-file-input'),
    'enable-cython': partial(TRANSLATION, 'opt-menu-enable-cython', value=''),
    'enable-uv': partial(TRANSLATION, 'opt-menu-enable-uv', value=''),
    'github-harden-runner': partial(TRANSLATION, 'opt-menu-github-harden-runner', value=''),
    'locale': partial(TRANSLATION, 'opt-menu-language-text'),
    'readme-type': partial(TRANSLATION, 'pro-readme-type'),
    'update-wrapfile': partial(TRANSLATION, 'opt-menu-update-wrapfile', value=''),
    'strict': partial(TRANSLATION, 'opt-menu-strict', value=''),
    'verify-email': partial(TRANSLATION, 'opt-menu-verify-email', value=''),
    'PKG-INFO': partial(TRANSLATION, 'adm-confirm'),
    'LicenseReader': partial(TRANSLATION, 'edit-menu-btn-license-file')
}
text_translation = {
    'AddProjectURL': partial(TRANSLATION, 'btn-add'),
    'Disclaimer-title': partial(TRANSLATION, 'adm-disclaimer-title'),
    'Ok': partial(TRANSLATION, 'btn-ok'),
    'Options': partial(TRANSLATION, 'btn-options'),
    'Page1': partial(TRANSLATION, 'web-core-metadata'),
    'Page2': partial(TRANSLATION, 'edit-menu-btn-license'),
    'Page4': partial(TRANSLATION, 'term-create-project'),
    'RefreshButton': partial(TRANSLATION, 'btn-refresh'),
    'RemoveProjectURL': partial(TRANSLATION, 'btn-remove'),
    'Reset': partial(TRANSLATION, 'btn-reset'),
    'SaveOptions': partial(TRANSLATION, 'btn-save'),
    'disclaimer-text': partial(TRANSLATION, 'adm-disclaimer-text'),
    'input-options': partial(TRANSLATION, 'term-input'),
    'locale-en': partial(TRANSLATION, 'lang-en'),
    'locale-zh': partial(TRANSLATION, 'lang-zh'),
    'output-options': partial(TRANSLATION, 'term-output'),
    'readme-type-md': partial(TRANSLATION, 'pro-readme-type-radio-md'),
    'readme-type-rst': partial(TRANSLATION, 'pro-readme-type-radio-rst'),
    'readme-type-txt': partial(TRANSLATION, 'pro-readme-type-radio-txt'),
    'user-interface-options': partial(TRANSLATION, 'term-user-interface'),
}

_validators = validators.copy()
name_valid = _validators.pop('Name')


def validate_name(e: webui.event) -> None:
    projectname = '$projectname'
    res = e.window.script(  # pyright: ignore
        f' return document.getElementById("Name").value; '
    )
    if name_valid(res.data):
        projectname = res.data
    else:
        show_error(e, 'name', TRANSLATION('web-err-invalid-input'))
    for k in validators:
        res = e.window.script(  # pyright: ignore
            f" return document.getElementById(`label-{k.lower()}`).innerHTML; "
        )
        t = label_translation[k](projectname=projectname)
        if res.data == t:
            continue
        update_label(e, k, t)


def validate_input(e: webui.event, k: str) -> None:
    res = e.window.script(  # pyright: ignore
        f' return document.getElementById("{k}").value; '
    )
    if not validators[k](res.data):
        show_error(e, k.lower(), TRANSLATION('web-err-invalid-input'))
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
    audience = e.window.script(AS_LIST_JS.format('Audience'))  # pyright: ignore
    environment = e.window.script(AS_LIST_JS.format('Environment'))  # pyright: ignore
    language = e.window.script(AS_LIST_JS.format('Language'))  # pyright: ignore
    framework = e.window.script(AS_LIST_JS.format('Framework'))  # pyright: ignore
    topic = e.window.script(AS_LIST_JS.format('Topic'))  # pyright: ignore
    allow_file = e.window.script(  # pyright: ignore
        f' return document.getElementById("allow-file").value; '
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
            label.data + TRANSLATION('sp') + TRANSLATION('web-err-invalid-input'),
        )
        return
    parsed_url = urlparse(url.data)
    match parsed_url:
        case p if p.netloc == '':
            show_error(
                e,
                'project-url',
                label.data + TRANSLATION('sp') + TRANSLATION('term-tap-empty-netloc'),
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


def update_ui_language(e: webui.event) -> None:
    locale = e.window.script(  # pyright: ignore
        ' return document.getElementById(`locale`).value; '
    )  # pyright: ignore
    interface.locale = locale.data
    for k, v in label_translation.items():
        if k in validators:
            continue
        update_label(e, k, v())
    TRANSLATION.mime_type = 'text/plain;charset=UTF-8'
    _text_translation = text_translation.copy()
    _text_translation |= {
        'Page3': partial(
            TRANSLATION,
            f'{TRANSLATION("term-classifier")}{TRANSLATION("sp")}{TRANSLATION("term-metadata")}',
        ),
    }
    for k, v in _text_translation.items():
        e.window.run(  # pyright: ignore
            f" document.getElementById(`{k}`).innerHTML = `{v()}`; "
        )
    e.window.run(  # pyright: ignore
        f"""
            document.getElementById('HideDisclaimer').checked = false;
            const tabHeading = document.getElementById("PageHeading")
            tabHeading.innerHTML = "{TRANSLATION('btn-options')}";
        """)
    TRANSLATION.mime_type = 'text/html;charset=UTF-8'



def remove_project_url(e: webui.event) -> None:
    e.window.run(  # pyright: ignore
        f"""
        var edit = document.getElementById(`EditProjectURL`);
        Array.from(edit.selectedOptions).forEach(opt => edit.remove(opt.index));
        """
    )


def change_tab(e: webui.event) -> None:
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
        title1.innerHTML = "{text_translation['Page1']()}";
        title2.innerHTML = "{text_translation['Page2']()}";
        title3.innerHTML = "{TRANSLATION("term-classifier")}{TRANSLATION("sp")}{TRANSLATION("term-metadata")}";
        title4.innerHTML = "{text_translation['Page4']()}";
        titleOptions.innerHTML = "{text_translation['Options']()}";
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


def show_prompt1(e: webui.event) -> None:
    change_tab(e)


def show_prompt2(e: webui.event) -> None:
    change_tab(e)


def show_prompt3(e: webui.event) -> None:
    change_tab(e)


def show_prompt4(e: webui.event) -> None:
    change_tab(e)
    show_pkg_info(e)


def show_options(e: webui.event) -> None:
    change_tab(e)


def close_disclaimer(e: webui.event) -> None:
    e.window.run(  # pyright: ignore
        " document.getElementById('HideDisclaimer').checked = true; "
    )


def close_application(e: webui.event) -> None:
    webui.exit()


class WebInterface:

    def __init__(self, window: webui.window) -> None:
        self.window = window
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
        self._licenses = OPTION_EMPTY + licenses
        self._audience_choices = ''.join(
            [
                (
                    OPTION_SELECTED.format(i)
                    if i in METADATA.spec.python.pkg.info.classifiers.intended_audience
                    else OPTION.format(i)
                )
                for i in sorted(from_prefix(Prefix().audience))
            ]
        )
        self._environment_choices = ''.join(
            [
                (
                    OPTION_SELECTED.format(i)
                    if i in METADATA.spec.python.pkg.info.classifiers.environment
                    else OPTION.format(i)
                )
                for i in sorted(from_prefix(Prefix().environment))
            ]
        )
        self._framework_choices = ''.join(
            [OPTION.format(i) for i in sorted(from_prefix(Prefix().framework))]
        )
        self._language_choices = ''.join(
            [
                (
                    OPTION_SELECTED.format(i)
                    if i in METADATA.spec.python.pkg.info.classifiers.language
                    else OPTION.format(i)
                )
                for i in sorted(from_prefix(Prefix().language))
            ]
        )
        self._status_choices = ''.join(
            [
                (
                    OPTION_SELECTED.format(i)
                    if i in METADATA.spec.python.pkg.info.classifiers.development_status
                    else OPTION.format(i)
                )
                for i in sorted(from_prefix(Prefix().status))
            ]
        )
        self._topic_choices = ''.join(
            [OPTION.format(i) for i in sorted(from_prefix(Prefix().topic))]
        )
        locales = [(i, TRANSLATION(f'lang-{i}')) for i in TRANSLATION.data.keys()]
        self._locale_choices = ''.join(
            [f'<option id="locale-{k}" value="{k}">{v}</option>' for k, v in sorted(locales)]
        )
        self._locale = TRANSLATION.locale
        self._disclaimer_text = None

    @property
    def licenses(self) -> str:
        return self._licenses

    @property
    def audience_choices(self) -> str:
        return self._audience_choices

    @property
    def environment_choices(self) -> str:
        return self._environment_choices

    @property
    def framework_choices(self) -> str:
        return self._framework_choices

    @property
    def language_choices(self) -> str:
        return self._language_choices

    @property
    def topic_choices(self) -> str:
        return self._topic_choices

    @property
    def status_choices(self) -> str:
        return self._status_choices

    @property
    def locale_choices(self) -> str:
        return self._locale_choices

    @property
    def disclaimer_text(self) -> str:
        # translations meant for <textarea>
        # should be text/plain;charset=UTF-8
        TRANSLATION.mime_type = 'text/plain;charset=UTF-8'
        text = TRANSLATION('adm-disclaimer-text')
        # everything else should be text/html;charset=UTF-8
        TRANSLATION.mime_type = 'text/html;charset=UTF-8'
        return text

    @property
    def locale(self) -> str:
        return self._locale

    @locale.setter
    def locale(self, value: str) -> None:
        TRANSLATION.locale = value
        self._locale = value

    @property
    def css(self) -> str:
        return (
            r"""
        @WEBUI_PROMPT_CSS@
        @WEBUI_I18N_CSS@
        """.replace(
                '../fonts/notoserifhk/', './'
            )
            .replace('../fonts/atkinsonhyperlegible/', './')
            .replace('../fonts/martianmono/', './')
        )

    def __call__(self) -> None:
        TRANSLATION.mime_type = 'text/html;charset=UTF-8'
        config = asdict(read_user_config())
        if config['interactive']['language']:
            TRANSLATION.locale = config['interactive']['language']
        self.window.show(f"""@WEBUI_PROMPT_1_HTML@""")
        self.window.run(" document.getElementById('HideDisclaimer').checked = false; ")


window = webui.window()
window.set_icon("""@WEBUI_LOGO@""", 'image/svg+xml')
window.bind('CloseDisclaimer', close_disclaimer)
window.bind('Name', validate_name)
window.bind('Summary', validate_summary)
window.bind('Keywords', validate_keywords)
window.bind('Author', validate_author)
window.bind('Author-email', validate_author_email)
window.bind('Maintainer', validate_maintainer)
window.bind('Maintainer-email', validate_maintainer_email)
window.bind('Page1', show_prompt1)
window.bind('Page2', show_prompt2)
window.bind('Page3', show_prompt3)
window.bind('Page4', show_prompt4)
window.bind('Options', show_options)
window.bind('License', load_license_expressions)
window.bind('License-Expression', load_license_exceptions)
window.bind('RefreshButton', show_license_reader)
window.bind('AddProjectURL', add_project_url)
window.bind('RemoveProjectURL', remove_project_url)
window.bind('locale', update_ui_language)
window.bind('SaveOptions', save_options)
interface = WebInterface(window)


def main() -> None:
    interface()
    # Wait until all windows are closed
    webui.wait()  # pyright: ignore
    TRANSLATION.mime_type = 'text/plain;charset=UTF-8'


if __name__ == '__main__':

    main()
