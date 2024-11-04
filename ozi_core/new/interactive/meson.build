# ozi/new/interactive/meson.build
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
config_files = [
    '__init__.py',
    '__init__.pyi',
    'menu.py',
    'menu.pyi',
    'project.py',
    'project.pyi',
    'validator.py',
    'validator.pyi',
]
foreach file: config_files
    if not meson.is_subproject() or get_option('install-subprojects').enabled()
        python.install_sources(file, subdir: 'ozi_core'/'new'/'interactive')
    endif
    fs.copyfile(file)
endforeach
if false
    executable('source_child_new', config_files)
endif
