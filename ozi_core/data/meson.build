# ozi/data/meson.build
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
source_data_files = [
    'en.yml',
    'zh.yml',
]
foreach file : files(source_data_files)
    fs.copyfile(file)
    if not meson.is_subproject() or get_option('install-subprojects').enabled()
        python.install_sources(file, pure: true, subdir: 'ozi_core' / 'data')
    endif
endforeach
source_data_children = []
foreach child: source_data_children
    subdir(child)
endforeach
if false
    executable('source_data_files', source_data_files)
    executable('source_data_children', source_data_children)
endif
