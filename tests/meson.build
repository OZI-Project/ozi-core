# OZI 0.4 meson.build:test_files,test_children
# Part of ozi-core.
# See LICENSE.txt in the project root for details.
# DO NOT EDIT BY HAND - This file was generated for use with OZI tools.
# ozi-fix -> meson rewrite is the standard editing pipeline.
test_files = ['test_actions.py', 'test_ozi_fix.py', 'test_ozi_new.py']
foreach file: test_files
    fs.copyfile(file)
    if not meson.is_subproject() or get_option('install-subprojects').enabled()
        python.install_sources(file, subdir: 'ozi_core' / 'tests')
    endif
endforeach
test_children = []
foreach child: test_children
    subdir(child)
endforeach
if false
    executable('test_files', test_files)
    executable('test_children', test_children)
endif
