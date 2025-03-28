# ozi/ui/meson.build
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
configure_file(
    input: 'web.py',
    output: 'web.py',
    install: true,
    install_dir: python.get_install_dir() / 'ozi_core' / 'ui',
    configuration: configuration_data({
        'OZI_NEW_HTML': fs.read(meson.project_source_root() / 'ozi_core' / 'ui' / 'ozi-new.html'),
        'OZI_LOGO_SVG': fs.read(meson.project_source_root() / 'ozi_core' / 'ui' / 'brand' / 'images' / 'ozi_logo_v2.svg'),
    }),
)
python.install_sources('style.css', subdir: 'ozi_core' / 'ui' / 'css')
python.install_sources('brand/css/fonts-en.css', subdir: 'ozi_core' / 'ui' / 'brand' / 'css')
python.install_sources('brand/fonts/atkinsonhyperlegible/AtkinsonHyperlegible-Bold.ttf', subdir: 'ozi_core' / 'ui' / 'brand' / 'fonts' / 'atkinsonhyperlegible')
python.install_sources('brand/fonts/atkinsonhyperlegible/AtkinsonHyperlegible-BoldItalic.ttf', subdir: 'ozi_core' / 'ui' / 'brand' / 'fonts' / 'atkinsonhyperlegible')
python.install_sources('brand/fonts/atkinsonhyperlegible/AtkinsonHyperlegible-Italic.ttf', subdir: 'ozi_core' / 'ui' / 'brand' / 'fonts' / 'atkinsonhyperlegible')
python.install_sources('brand/fonts/atkinsonhyperlegible/AtkinsonHyperlegible-Regular.ttf', subdir: 'ozi_core' / 'ui' / 'brand' / 'fonts' / 'atkinsonhyperlegible')
python.install_sources('brand/fonts/martianmono/MartianMono[wdth,wght].ttf', subdir: 'ozi_core' / 'ui' / 'brand' / 'fonts' / 'martianmono')
python.install_sources('brand/fonts/notoserifhk/NotoSerifHK[wght].ttf', subdir: 'ozi_core' / 'ui' / 'brand' / 'fonts' / 'notoserifhk')
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
