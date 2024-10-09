# ozi/meson.build
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
configure_file(
    input: 'generate_locales.py',
    output: 'generate_locales.py',
    copy: true,
    install: true,
    install_dir: 'ozi_core',
)
locales = custom_target(
    '_locales.py',
    output: '_locales.py',
    capture: true,
    command: [python, meson.current_build_dir()/'generate_locales.py'],
    install: true,
    install_dir: python.get_install_dir().replace(get_option('prefix')+'/', '')/'ozi_core',
    build_by_default: true,
)
source_files = [
    '__init__.py',
    '_i18n.py',
    'actions.py',
    'comment.py',
    'meson.py',
    'pkg_extra.py',
    'py.typed',
    'render.py',
    'spdx.py',
    'trove.py',
]
foreach file : files(source_files)
    fs.copyfile(file)
    if not meson.is_subproject() or get_option('install-subprojects').enabled()
        python.install_sources(file, pure: true, subdir: 'ozi_core')
    endif
endforeach
source_children = [
    'data',
    'vendor',
    'fix',
    'new',
]
foreach child: source_children
    subdir(child)
endforeach
