import html
import re
import sys
from datetime import datetime
from functools import partial
from logging import getLogger
from typing import Callable

from ozi_spec import METADATA  # pyright: ignore
from ozi_spec._license import SPDX_LICENSE_EXCEPTIONS  # pyright: ignore
from ozi_templates import load_environment
from webui import webui  # type: ignore

from ozi_core._i18n import TRANSLATION
from ozi_core._logging import config_logger
from ozi_core.trove import Prefix
from ozi_core.trove import from_prefix
from ozi_core.vendor.email_validator import validate_email
from ozi_core.vendor.email_validator.exceptions_types import EmailNotValidError

config_logger()
__logger = getLogger(f'ozi_core.{__name__}')
sys.modules[__name__].__dict__.update(**TRANSLATION.data)

licenses = ''.join(
    [
        f'<option value="{i}">{i}</option>'
        for i in sorted(
            set(METADATA.spec.python.pkg.license.ambiguous.keys()).intersection(
                from_prefix(Prefix().license)
            )
        )
    ]
)
licenses = '<option value=""></option>' + licenses
audience_choices = ''.join(
    [f'<option value="{i}">{i}</option>' for i in sorted(from_prefix(Prefix().audience))]
)
environment_choices = ''.join(
    [f'<option value="{i}">{i}</option>' for i in sorted(from_prefix(Prefix().environment))]
)
framework_choices = ''.join(
    [f'<option value="{i}">{i}</option>' for i in sorted(from_prefix(Prefix().framework))]
)
language_choices = ''.join(
    [f'<option value="{i}">{i}</option>' for i in sorted(from_prefix(Prefix().language))]
)
status_choices = ''.join(
    [f'<option value="{i}">{i}</option>' for i in sorted(from_prefix(Prefix().status))]
)
topic_choices = ''.join(
    [f'<option value="{i}">{i}</option>' for i in sorted(from_prefix(Prefix().topic))]
)
webui_prompt_css = """@WEBUI_PROMPT_CSS@"""
webui_prompt1 = f"""@WEBUI_PROMPT_1_HTML@"""


def _validate_email(addr: str) -> bool:
    try:
        validate_email(addr)
    except EmailNotValidError as exc:
        return False
    else:
        return True


validators: dict[str, Callable[[str], bool]] = {
    'Name': lambda x: re.match(r'^([A-Za-z]|[A-Za-z][A-Za-z0-9._-]*[A-Za-z0-9]){1,80}$', x)
    is not None,
    'Summary': lambda x: 0 < len(x) < 256,
    'Keywords': lambda x: re.match(r'^(([a-z_]*[a-z0-9],)*){2,650}$', x) is not None,
    'Author': lambda x: 0 < len(x) < 512,
    'Author-email': lambda x: all(map(_validate_email, x.split(','))),
    'Maintainer': lambda x: 0 < len(x) < 512,
    'Maintainer-email': lambda x: all(map(_validate_email, x.split(','))),
    'License': lambda _: True,
    'License-Expression': lambda _: True,
}

text_translation: dict[str, partial[str]] = {
    'Summary': partial(TRANSLATION, 'pro-summary'),
    'Keywords': partial(TRANSLATION, 'pro-keywords'),
    'Author': partial(TRANSLATION, 'pro-author'),
    'Author-email': partial(TRANSLATION, 'pro-author-email'),
    'Maintainer': partial(TRANSLATION, 'pro-maintainer'),
    'Maintainer-email': partial(TRANSLATION, 'pro-maintainer-email'),
    'License': partial(TRANSLATION, 'pro-license'),
    'License-Expression': partial(TRANSLATION, 'pro-license-expression'),
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
    for k in _validators:
        res = e.window.script(  # pyright: ignore
            f" return document.getElementById(`label-{k.lower()}`).innerHTML; "
        )
        t = text_translation[k](projectname=projectname)
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
            f'<option value="{i}">{i}</option>'
            for i in sorted(
                METADATA.spec.python.pkg.license.ambiguous.get(res.data, tuple())
            )
        ]
    )
    spdx = '<option value=""></option>' + spdx
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
        document.getElementById(`err-{_id}`).innerHTML = `[ ! ] {message}`;
        """
    )


def load_license_exceptions(e: webui.event) -> None:
    license_expr = e.window.script(  # pyright: ignore
        " return document.getElementById(`License-Expression`).value; "
    )
    exceptions = '<option value=""></option>' + ''.join(
        [
            f'<option value="{i}">{i}</option>'
            for i in sorted(
                tuple(
                    k
                    for k, v in SPDX_LICENSE_EXCEPTIONS.items()  # type: ignore
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


def show_prompt1(e: webui.event) -> None:
    e.window.run(  # pyright: ignore
        f"""
        document.getElementById(`HidePage1Contents`).checked = false; 
        document.getElementById(`HidePage2Contents`).checked = true;
        document.getElementById(`HidePage3Contents`).checked = true;
        """
    )


def show_prompt2(e: webui.event) -> None:
    e.window.script(  # pyright: ignore
        f"""
        document.getElementById(`HidePage1Contents`).checked = true;
        document.getElementById(`HidePage2Contents`).checked = false;
        document.getElementById(`HidePage3Contents`).checked = true;
        """
    )


def show_prompt3(e: webui.event) -> None:
    e.window.script(  # pyright: ignore
        f"""
        document.getElementById(`HidePage1Contents`).checked = true;
        document.getElementById(`HidePage2Contents`).checked = true;
        document.getElementById(`HidePage3Contents`).checked = false;
        """
    )


def close_disclaimer(e: webui.event) -> None:
    e.window.run(
        " document.getElementById('HideDisclaimer').checked = true; "
    )  # pyright: ignore


def close_application(e: webui.event) -> None:
    webui.exit()


def main() -> None:
    # Create a window object
    win = webui.window()  # pyright: ignore
    # Bind am HTML element ID with a python function
    win.set_runtime(webui.runtime.deno)
    win.bind('CloseDisclaimer', close_disclaimer)
    win.bind('', validate_name)
    win.bind('Summary', validate_summary)
    win.bind('Keywords', validate_keywords)
    win.bind('Author', validate_author)
    win.bind('Author-email', validate_author_email)
    win.bind('Maintainer', validate_maintainer)
    win.bind('Maintainer-email', validate_maintainer_email)
    win.bind('Page1', show_prompt1)
    win.bind('Page2', show_prompt2)
    win.bind('Page3', show_prompt3)
    win.bind('License', load_license_expressions)
    win.bind('License-Expression', load_license_exceptions)
    win.bind('RefreshButton', show_license_reader)
    # Show the window
    win.show(webui_prompt1)
    win.run(
        """
    document.getElementById('HideDisclaimer').checked = false; 
    """
    )

    # Wait until all windows are closed
    webui.wait()  # pyright: ignore


if __name__ == '__main__':
    main()
