# ozi/new/meson.build
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
source_new_files = [
    '__init__.py',
    '__init__.pyi',
    'parser.py',
    'parser.pyi',
    'validate.py',
    'validate.pyi',
]
foreach file: source_new_files
    if not meson.is_subproject() or get_option('install-subprojects').enabled()
        python.install_sources(file, subdir: 'ozi_core'/'new')
    endif
    fs.copyfile(file)
endforeach
source_new_children = [
    'interactive'
]
foreach child: source_new_children
    subdir(child)
endforeach
if false
    executable('source_new_files', source_new_files)
    executable('source_new_children', source_new_children)
endif
