# ozi/meson.build
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
custom_target(
    '_locales.py',
    input: 'generate_locales.py',
    output: '_locales.py',
    command: [python, '@INPUT@'],
    build_by_default: true,
    install: true,
    install_dir: python.get_install_dir() / 'ozi_core',
)
source_files = [
    '__init__.py',
    '__init__.pyi',
    '_i18n.py',
    '_i18n.pyi',
    '_locales.pyi',
    'actions.py',
    'actions.pyi',
    'comment.py',
    'comment.pyi',
    'generate_locales.py',
    'generate_locales.pyi',
    'meson.py',
    'meson.pyi',
    'pkg_extra.py',
    'pkg_extra.pyi',
    'py.typed',
    'render.py',
    'render.pyi',
    'spdx.py',
    'spdx.pyi',
    'trove.py',
    'trove.pyi',
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
    'ui',
]
foreach child: source_children
    subdir(child)
endforeach
