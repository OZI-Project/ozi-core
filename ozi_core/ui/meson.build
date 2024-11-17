# ozi/ui/meson.build
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
source_ui_files = [
    '__init__.py',
    'menu.py',
    'menu.pyi',
    'defaults.py',
    'defaults.pyi',
    'dialog.py',
    'dialog.pyi',
    '_style.py',
    '_style.pyi',
]
foreach file: source_ui_files
    if not meson.is_subproject() or get_option('install-subprojects').enabled()
        python.install_sources(file, subdir: 'ozi_core'/'ui')
    endif
    fs.copyfile(file)
endforeach
source_ui_children = []
foreach child: source_ui_children
    subdir(child)
endforeach
if false
    executable('source_ui_files', source_ui_files)
    executable('source_ui_children', source_ui_children)
endif
