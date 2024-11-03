# ozi/fix/meson.build
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
config_files = [
    '__init__.py',
    '__init__.pyi',
    'build_definition.py',
    'build_definition.pyi',
    'interactive.py',
    'missing.py',
    'missing.pyi',
    'parser.py',
    'parser.pyi',
    'rewrite_command.py',
    'rewrite_command.pyi',
]
foreach file: config_files
    if not meson.is_subproject() or get_option('install-subprojects').enabled()
        python.install_sources(file, subdir: 'ozi_core'/'fix')
    endif
    fs.copyfile(file)
endforeach
if false
    executable('source_child_fix', config_files)
endif
