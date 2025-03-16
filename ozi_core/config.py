from __future__ import annotations

from dataclasses import asdict
from dataclasses import dataclass
from dataclasses import field
from dataclasses import fields
from importlib.metadata import PackageNotFoundError
from importlib.metadata import version
from pathlib import Path
from typing import Self

import yaml
from platformdirs import user_config_dir

from ozi_core import __version__

try:
    core_version = version('ozi-core')
except PackageNotFoundError:
    core_version = 'git-dev'


HEADER = '\n'.join(
    [
        f'# {Path(user_config_dir("OZI")) / "config.yml"}',
        f'# OZI version: {__version__}',
        f'# ozi-core version: {core_version}\n',
    ]
)
CONF_PATH = Path(user_config_dir('OZI')) / 'config.yml'


@dataclass(init=False, kw_only=True)
class ConfigBase:
    def __init__(  # pragma: no cover
        self: Self, **kwargs: dict[str, str | list[str] | bool | None]
    ) -> None:
        names = {f.name for f in fields(self)}
        for k, v in kwargs.items():
            if k in names:
                setattr(self, k, v)


@dataclass(init=False, kw_only=True)
class OziInteractiveConfig(ConfigBase):
    """General config options for dialog-based CLI."""

    language: str | None = None

    def __init__(  # pragma: no cover
        self: Self, **kwargs: dict[str, str | list[str] | bool | None]
    ) -> None:
        super().__init__(**kwargs)


@dataclass(init=False, kw_only=True)
class OziFixConfig(ConfigBase):
    """Persistent ``ozi-fix interactive`` settings."""

    copyright_head: str | None = None
    pretty: bool | None = None
    strict: bool | None = None
    update_wrapfile: bool | None = None

    def __init__(  # pragma: no cover
        self: Self, **kwargs: dict[str, str | list[str] | bool | None]
    ) -> None:
        super().__init__(**kwargs)


@dataclass(init=False, kw_only=True)
class OziNewConfig(ConfigBase):
    """Persistent ``ozi-new interactive`` settings."""

    allow_file: list[str] | None = None
    author: str | None = None
    author_email: str | None = None
    ci_provider: str | None = None
    check_package_exists: bool | None = None
    copyright_head: str | None = None
    enable_cython: bool | None = None
    enable_uv: bool | None = None
    github_harden_runner: bool | None = None
    maintainer: str | None = None
    maintainer_email: str | None = None
    language: list[str] | None = None
    readme_type: str | None = None
    strict: bool | None = None
    update_wrapfile: bool | None = None
    verify_email: bool | None = None

    def __init__(  # pragma: no cover
        self: Self, **kwargs: dict[str, str | list[str] | bool | None]
    ) -> None:
        super().__init__(**kwargs)


@dataclass(kw_only=True)
class OziConfig:
    """Persistent ``ozi-* interactive`` settings."""

    fix: OziFixConfig = field(default_factory=OziFixConfig)
    new: OziNewConfig = field(default_factory=OziNewConfig)
    interactive: OziInteractiveConfig = field(default_factory=OziInteractiveConfig)


def read_user_config() -> OziConfig:  # pragma: defer to E2E
    CONF_PATH.parent.mkdir(exist_ok=True)
    CONF_PATH.touch(exist_ok=True)
    data = yaml.safe_load(CONF_PATH.read_text())
    if data is not None:
        return OziConfig(**data)
    else:
        return OziConfig()


def write_user_config(  # pragma: defer to E2E
    data: OziConfig,
) -> None:
    CONF_PATH.write_text(
        HEADER + yaml.safe_dump(data=asdict(data), allow_unicode=True),
        encoding='utf-8',
    )
