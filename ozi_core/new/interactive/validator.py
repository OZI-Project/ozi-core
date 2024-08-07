from __future__ import annotations

import re
from functools import lru_cache

import requests  # pyright: ignore
from prompt_toolkit.document import Document  # pyright: ignore
from prompt_toolkit.validation import ThreadedValidator  # pyright: ignore
from prompt_toolkit.validation import ValidationError  # pyright: ignore
from prompt_toolkit.validation import Validator


@lru_cache
def pypi_package_exists(package: str) -> bool:  # pragma: no cover
    return (
        requests.get(
            f'https://pypi.org/simple/{package}',
            timeout=15,
        ).status_code
        == 200
    )


class ProjectNameValidator(Validator):
    def validate(
        self,  # noqa: ANN101,RUF100
        document: Document,
    ) -> None:  # pragma: no cover
        if len(document.text) == 0:
            raise ValidationError(0, 'cannot be empty')
        if not re.match(
            '^([A-Z0-9]|[A-Z0-9][A-Z0-9._-]*[A-Z0-9])$',
            document.text,
            flags=re.IGNORECASE,
        ):
            raise ValidationError(len(document.text), 'invalid project name')


class NotReservedValidator(ThreadedValidator):
    def validate(
        self,  # noqa: ANN101,RUF100
        document: Document,
    ) -> None:  # pragma: no cover
        self.validator.validate(document)
        if pypi_package_exists(document.text):
            raise ValidationError(len(document.text), 'project with that name exists')


class LengthValidator(Validator):
    def validate(
        self,  # noqa: ANN101,RUF100
        document: Document,
    ) -> None:  # pragma: no cover
        if len(document.text) == 0:
            raise ValidationError(0, 'must not be empty')
        if len(document.text) > 512:
            raise ValidationError(512, 'input is too long')


class PackageValidator(Validator):
    def validate(
        self,  # noqa: ANN101,RUF100
        document: Document,
    ) -> None:  # pragma: no cover
        if len(document.text) == 0:
            raise ValidationError(0, 'cannot be empty')
        if pypi_package_exists(document.text):
            pass
        else:
            raise ValidationError(len(document.text), 'package not found')


def validate_message(
    text: str,
    validator: Validator,
) -> tuple[bool, str]:  # pragma: no cover
    """Validate a string.

    :param text: string to validate
    :type text: str
    :param validator: validator instance
    :type validator: Validator
    :return: validation, error message
    :rtype: tuple[bool, str]
    """
    try:
        validator.validate(Document(text))
    except ValidationError as e:
        return False, e.message
    return True, ''
