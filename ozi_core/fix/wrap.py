from configparser import ConfigParser
from pathlib import Path

from ozi_templates.filter import get_ozi_tarball_sha256


def update_wrapfile(version: str) -> None:
    """Update a project :file:`subprojects/ozi.wrap` and symlink to the latest OZI version.

    :param version: release to search for
    :type version: str
    """
    config = ConfigParser()
    ozi_wrap = Path('subprojects') / 'ozi.wrap'
    config.read(ozi_wrap)
    if not 'wrap-file' in config:
        config.add_section('wrap-file')
    if config.remove_section('wrap-git'):
        config.remove_section('provide')
    wrap_file = config['wrap-file']
    wrap_file['directory'] = f'OZI-{version}'
    wrap_file['source_url'], wrap_file['source_hash'] = get_ozi_tarball_sha256(version)
    wrap_file['source_filename'] = f'OZI-{version}.tar.gz'
    if not 'provide' in config:
        config.add_section('provide')
    provide = config['provide']
    provide['dependency_names'] = f'ozi, ozi-{version}'
    with ozi_wrap.open('w', encoding='utf-8') as f:
        config.write(f)
    if (ozi_wrap.parent / 'ozi').is_symlink():
        (ozi_wrap.parent / 'ozi').unlink()
    (ozi_wrap.parent / 'ozi').symlink_to(
        '..' / ozi_wrap.parent / f'OZI-{version}', target_is_directory=True
    )

