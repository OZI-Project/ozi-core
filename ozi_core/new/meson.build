# ozi/new/meson.build
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
config_files = [
    '__init__.py',
    '__init__.pyi',
    'defaults.py',
    'defaults.pyi',
    'parser.py',
    'parser.pyi',
    'validate.py',
    'validate.pyi',
]
foreach file: config_files
    if not meson.is_subproject() or get_option('install-subprojects').enabled()
        python.install_sources(file, subdir: 'ozi_core'/'new')
    endif
    fs.copyfile(file)
endforeach
source_child_new_children = [
    'interactive'
]
foreach child: source_child_new_children
    subdir(child)
endforeach