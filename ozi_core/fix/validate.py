from __future__ import annotations

from argparse import Action
from argparse import ArgumentParser
from argparse import Namespace
from typing import TYPE_CHECKING
from typing import Any
from typing import Sequence

from prompt_toolkit.validation import ValidationError  # pyright: ignore
from prompt_toolkit.validation import Validator

from ozi_core._i18n import TRANSLATION

if TYPE_CHECKING:
    from prompt_toolkit.document import Document  # pyright: ignore


def _copy_items(items: list[str] | None) -> list[str]:  # pragma: defer to python
    """Copied from the argparse module."""
    if items is None:
        return []
    # The copy module is used only in the 'append' and 'append_const'
    # actions, and it is needed only when the default value isn't a list.
    # Delay its import for speeding up the common case.
    if type(items) is list:
        return items[:]
    import copy

    return copy.copy(items)


def valid_rewrite_command_target(target: str) -> bool:  # pragma: defer to E2E
    return len(target.rstrip('/').split('/')) == 1


class AppendRewriteCommandTarget(Action):
    def __call__(  # pragma: defer to E2E
        self: AppendRewriteCommandTarget,
        parser: ArgumentParser,
        namespace: Namespace,
        values: str | Sequence[Any] | None,
        option_string: str | None = None,
    ) -> None:
        if not valid_rewrite_command_target(values):  # type: ignore
            parser.error(f'Nested paths are not yet supported. Path: {values}')
        items = getattr(namespace, self.dest, None)
        items = _copy_items(items)
        items.append(values)  # type: ignore
        setattr(namespace, self.dest, [values])


class RewriteCommandTargetValidator(Validator):
    """Validate that a target name is valid."""

    def validate(  # pragma: defer to E2E
        self,  # noqa: ANN101,RUF100
        document: Document,
    ) -> None:  # pragma: no cover
        if len(document.text) == 0:
            raise ValidationError(0, TRANSLATION('err-no-empty'))
        if not valid_rewrite_command_target(document.text):
            raise ValidationError(
                len(document.text),
                TRANSLATION('err-no-nested-fix-support'),
            )
