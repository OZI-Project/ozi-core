from dataclasses import asdict
from dataclasses import dataclass
from dataclasses import field
from importlib.metadata import PackageNotFoundError
from importlib.metadata import version
from pathlib import Path

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


@dataclass(kw_only=True)
class OziInteractiveConfig:
    """General config options for dialog-based CLI."""

    language: str | None = None


@dataclass(kw_only=True)
class OziFixConfig:
    """Persistent ``ozi-fix interactive`` settings."""

    copyright_head: str | None = None
    pretty: bool | None = None
    strict: bool | None = None


@dataclass(kw_only=True)
class OziNewConfig:
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
    verify_email: bool | None = None


@dataclass(kw_only=True)
class OziConfig:
    """Persistent ``ozi-* interactive`` settings."""

    fix: OziFixConfig = field(default_factory=OziFixConfig)
    new: OziNewConfig = field(default_factory=OziNewConfig)
    interactive: OziInteractiveConfig = field(default_factory=OziInteractiveConfig)


def read_user_config() -> OziConfig:  # pragma: defer to E2E
    conf = Path(user_config_dir('OZI')) / 'config.yml'
    conf.touch(exist_ok=True)
    conf.parent.mkdir(exist_ok=True)
    data = yaml.safe_load(conf.read_text())
    if data is not None:
        return OziConfig(**data)
    else:
        return OziConfig()


def write_user_config(  # pragma: defer to E2E
    data: OziConfig,
) -> None:
    (Path(user_config_dir('OZI')) / 'config.yml').write_text(
        HEADER + yaml.safe_dump(data=asdict(data), allow_unicode=True),
        encoding='utf-8',
    )
