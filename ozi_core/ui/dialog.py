from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Any
from typing import Sequence
from typing import TypeVar

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
from prompt_toolkit.styles import BaseStyle  # pyright: ignore
from prompt_toolkit.styles import Style  # pyright: ignore
from prompt_toolkit.widgets import Button  # pyright: ignore
from prompt_toolkit.widgets import Dialog  # pyright: ignore
from prompt_toolkit.widgets import Label  # pyright: ignore
from prompt_toolkit.widgets import RadioList
from prompt_toolkit.widgets import TextArea
from prompt_toolkit.widgets.toolbars import ValidationToolbar

from ozi_core.ui._style import _style_dict
from ozi_core.ui.menu import MenuButton

if TYPE_CHECKING:  # pragma: no cover
    from prompt_toolkit.buffer import Buffer  # pyright: ignore
    from prompt_toolkit.completion import Completer  # pyright: ignore
    from prompt_toolkit.formatted_text import AnyFormattedText  # pyright: ignore
    from prompt_toolkit.key_binding.key_processor import KeyPressEvent  # pyright: ignore
    from prompt_toolkit.validation import Validator  # pyright: ignore


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
        self: Admonition,
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

    def _handle_enter(self) -> None:  # noqa: DC103,ANN101,RUF100
        pass  # pragma: no cover


def _return_none() -> None:  # pragma: no cover
    """Button handler that returns None."""
    get_app().exit()


def admonition_dialog(
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
        ok_text = MenuButton.OK._str
    if cancel_text is None:
        cancel_text = MenuButton.EXIT._str

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


def input_dialog(  # pragma: no cover
    title: AnyFormattedText = '',
    text: AnyFormattedText = '',
    ok_text: str | None = None,
    cancel_text: str | None = None,
    completer: Completer | None = None,
    validator: Validator | None = None,
    password: FilterOrBool = False,
    style: BaseStyle | None = None,
    multiline: bool = False,
    default: str = '',
) -> Application[str]:
    """
    Display a text input box.
    Return the given text, or None when cancelled.
    """
    if ok_text is None:
        ok_text = MenuButton.OK._str
    if cancel_text is None:
        cancel_text = MenuButton.BACK._str

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
        multiline=multiline,
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
