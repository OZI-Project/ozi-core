# ozi/ui/meson.build
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
configure_file(
    input: 'web.py',
    output: 'web.py',
    install: true,
    install_dir: 'ozi_core'/'ui',
    configuration: configuration_data({
        'WEBUI_PROMPT_1_HTML': fs.read(meson.project_source_root() / 'ozi_core' / 'ui' / 'ozi-new.html'),
        'WEBUI_PROMPT_CSS': fs.read(meson.project_source_root() / 'ozi_core' / 'ui' / 'style.css'),
        'WEBUI_I18N_CSS': fs.read(meson.project_source_root() / 'ozi_core' / 'ui' / 'brand' / 'css' / 'fonts-en.css'),
        'WEBUI_LOGO': fs.read(meson.project_source_root() / 'ozi_core' / 'ui' / 'brand' / 'images' / 'ozi_logo_v2.svg'),
    }),
)
fs.copyfile('brand/fonts/atkinsonhyperlegible/AtkinsonHyperlegible-Bold.ttf', install: true, install_dir: '.')
fs.copyfile('brand/fonts/atkinsonhyperlegible/AtkinsonHyperlegible-BoldItalic.ttf', install: true, install_dir: '.')
fs.copyfile('brand/fonts/atkinsonhyperlegible/AtkinsonHyperlegible-Italic.ttf', install: true, install_dir: '.')
fs.copyfile('brand/fonts/atkinsonhyperlegible/AtkinsonHyperlegible-Regular.ttf', install: true, install_dir: '.')
fs.copyfile('brand/fonts/martianmono/MartianMono[wdth,wght].ttf', install: true, install_dir: '.')
fs.copyfile('brand/fonts/notoserifhk/NotoSerifHK[wght].ttf', install: true, install_dir: '.')
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
