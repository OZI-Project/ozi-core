"""
This type stub file was generated by pyright.
"""

from argparse import Namespace
from typing import TYPE_CHECKING
from typing import Any
from typing import Sequence
from typing import TypeAlias

from pyparsing import ParseResults

from ozi_core.vendor.email_validator import ValidatedEmail

"""ozi-new input validation."""
if TYPE_CHECKING:
    Composable: TypeAlias = ...
_CLASSIFIERS = ...
def valid_classifier(classifier: str) -> None:
    """Validate a classifier string"""
    ...

def valid_project_url(project_url: Sequence[str]) -> None:
    """Validate a list of project urls strings of the format ``name,url``."""
    ...

def valid_home_page(home_page: str) -> None:
    """Validate a project homepage url"""
    ...

def valid_summary(summary: str) -> None:
    """Validate project summary length."""
    ...

def valid_contact_info(author: str, maintainer: str, author_email: Sequence[str], maintainer_email: Sequence[str]) -> None:
    """Validate project contact info metadata.

    :param author: comma-separated author names
    :type author: str
    :param maintainer: comma-separated maintainer names
    :type maintainer: str
    :param author_email: author email addresses
    :type author_email: Sequence[str]
    :param maintainer_email: maintainer email addresses
    :type maintainer_email: Sequence[str]
    """
    ...

def valid_license(_license: str, license_expression: str) -> str:
    """Validate license and check against license expression."""
    ...

def valid_copyright_head(copyright_head: str, project_name: str, license_file: str) -> str:
    """Validate a copyright header.

    :param copyright_head: the header text in full
    :type copyright_head: str
    :param project_name: the project name
    :type project_name: str
    :param license_file: the license filename
    :type license_file: str
    """
    ...

def valid_project_name(name: str | ParseResults) -> None:
    """Validate a project name."""
    ...

def valid_spdx(expr: Any | ParseResults) -> None:
    """Validate a SPDX license expression."""
    ...

def valid_email(email: str, verify: bool = ...) -> ValidatedEmail | None:
    """Validate a single email address."""
    ...

def valid_emails(author_email: list[str], maintainer_email: list[str], verify: bool) -> tuple[list[str], list[str]]:
    """Validate lists of author and maintainer emails."""
    ...

def preprocess_arguments(project: Namespace) -> Namespace:
    """Preprocess (validate) arguments for project namespace."""
    ...

def postprocess_arguments(project: Namespace) -> Namespace:
    """Postprocess (normalize) arguments for project namespace."""
    ...
