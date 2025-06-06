# ozi/meson.build
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
source_files = [
  '__init__.py',
  '__init__.pyi',
  '__main__.py',
  '__main__.pyi',
  '_i18n.py',
  '_i18n.pyi',
  '_logging.py',
  '_logging.pyi',
  'actions.py',
  'actions.pyi',
  'comment.py',
  'comment.pyi',
  'config.py',
  'config.pyi',
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
  'validate.py',
  'wrap.py',
]
foreach file : files(source_files)
    fs.copyfile(file)
    if not meson.is_subproject() or get_option('install-subprojects').enabled()
        python.install_sources(file, pure: true, subdir: 'ozi_core')
    endif
endforeach

subdir('fix')
subdir('new')
subdir('ui')
subdir('data')
subdir('vendor')
source_children = ['ozi.phony']
foreach child : source_children
    if child != 'ozi.phony'
        subdir(child)
    endif
endforeach
if false
    executable('source_files', source_files)
    executable('ext_files', ext_files)
    executable('source_children', source_children)
endif