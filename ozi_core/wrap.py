import os
from configparser import ConfigParser
from pathlib import Path
from shutil import rmtree

from ozi_templates.filter import get_ozi_tarball_sha256  # pyright: ignore


def create_subproject_symlink(target: Path | str, version: str) -> None:
    wrapfile = Path(target, 'subprojects', 'ozi.wrap')
    subproject = '..' / wrapfile.parent / f'OZI-{version}'
    if (wrapfile.parent / 'ozi').is_symlink():
        (wrapfile.parent / 'ozi').unlink()  # pragma: defer to E2E
    elif (wrapfile.parent / 'ozi').exists():
        rmtree(wrapfile.parent / 'ozi', ignore_errors=True)  # pragma: defer to E2E
    (wrapfile.parent / 'ozi').symlink_to(subproject, target_is_directory=True)


def update_wrapfile(target: Path | str, version: str) -> None:
    """Update a project :file:`subprojects/ozi.wrap` and symlink to the latest OZI version.

    :param version: release to search for
    :type version: str
    """
    config = ConfigParser()
    ozi_wrap = Path(target, 'subprojects', 'ozi.wrap')
    config.read(ozi_wrap)
    if 'wrap-file' not in config:  # pragma: defer to E2E
        config.add_section('wrap-file')
    if config.remove_section('wrap-git'):  # pragma: defer to E2E
        config.remove_section('provide')
    wrap_file = config['wrap-file']
    wrap_file['directory'] = f'OZI-{version}'
    if 'PYTEST_CURRENT_TEST' not in os.environ:  # pragma: defer to E2E
        wrap_file['source_url'], wrap_file['source_hash'] = get_ozi_tarball_sha256(version)
    else:
        wrap_file['source_url'], wrap_file['source_hash'] = 'pytest', 'pytest'
    wrap_file['source_filename'] = f'OZI-{version}.tar.gz'
    if 'provide' not in config:  # pragma: defer to E2E
        config.add_section('provide')
    provide = config['provide']
    provide['dependency_names'] = f'ozi, ozi-{version}'
    with ozi_wrap.open('w', encoding='utf-8') as f:
        config.write(f)
    create_subproject_symlink(target, version)
