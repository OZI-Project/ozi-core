from dataclasses import dataclass
from pathlib import Path

from ozi_core import __version__ as __version__

core_version: str
HEADER: str
CONF_PATH: Path

@dataclass(kw_only=True)
class OziInteractiveConfig:
    """General config options for dialog-based CLI."""

    language: str | None = ...

@dataclass(kw_only=True)
class OziFixConfig:
    """Persistent ``ozi-fix interactive`` settings."""

    copyright_head: str | None = ...
    pretty: bool | None = ...
    strict: bool | None = ...

@dataclass(kw_only=True)
class OziNewConfig:
    """Persistent ``ozi-new interactive`` settings."""

    allow_file: list[str] | None = ...
    author: str | None = ...
    author_email: str | None = ...
    ci_provider: str | None = ...
    check_package_exists: bool | None = ...
    copyright_head: str | None = ...
    enable_cython: bool | None = ...
    enable_uv: bool | None = ...
    github_harden_runner: bool | None = ...
    maintainer: str | None = ...
    maintainer_email: str | None = ...
    language: list[str] | None = ...
    readme_type: str | None = ...
    strict: bool | None = ...
    verify_email: bool | None = ...

@dataclass(kw_only=True)
class OziConfig:
    """Persistent ``ozi-* interactive`` settings."""

    fix: OziFixConfig = ...
    new: OziNewConfig = ...
    interactive: OziInteractiveConfig = ...

def read_user_config() -> OziConfig: ...
def write_user_config(data: OziConfig) -> None: ...
