from __future__ import annotations

from enum import Enum
from enum import auto
from enum import unique

from ozi_core._i18n import TRANSLATION


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
    YES = auto()
    NO = auto()
    SKIP = auto()

    @property
    def _tuple(self: MenuButton) -> tuple[str, int]:  # pragma: no cover
        """Return a tuple of text, value for prompt-toolkit buttons."""
        return TRANSLATION(f'btn-{self.name.lower()}'), self.value

    @property
    def _str(self: MenuButton) -> str:  # pragma: no cover
        """Return prompt-toolkit button text."""
        return TRANSLATION(f'btn-{self.name.lower()}')
