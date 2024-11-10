# ozi/vendor/meson.build
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
source_vendor_files = [
    '__init__.py',
]
foreach file : files(source_vendor_files)
    fs.copyfile(file)
    if not meson.is_subproject() or get_option('install-subprojects').enabled()
        python.install_sources(file, pure: true, subdir: 'ozi_core' / 'vendor')
    endif
endforeach
source_vendor_children = ['email_validator']
foreach child: source_vendor_children
    subdir(child)
endforeach
if false
    executable('source_vendor_files', source_vendor_files)
    executable('source_vendor_children', source_vendor_children)
endif
