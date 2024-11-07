# OZI 0.4 meson.build:root_files,root_children
# Part of ozi-core.
# See LICENSE.txt in the project root for details.
# DO NOT EDIT BY HAND - This file was generated for use with OZI tools.
# ozi-fix -> meson rewrite is the standard editing pipeline.
project(
    'ozi-core',
    default_options: ['warning_level=3'],
    license: 'Apache-2.0 WITH LLVM-exception',
    license_files: ['LICENSE.txt'],
    meson_version: '>=1.1.0',
    version: run_command(
        'python3',
        [
            '-c',
            'from setuptools_scm import get_version;print(get_version(normalize=False))',
        ],
        check: true,
    ).stdout().strip(),
)
fs = import('fs')
pymod = import('python')
python_dependencies = get_option('python-dependencies')
python = pymod.find_installation()
project_name = meson.project_name()
root_files = [
    'README',
    'CHANGELOG.md',
    'LICENSE.txt',
    'pyproject.toml',
    '.gitignore',
]
pyproject_config = configuration_data()
pyproject_config.set('VCS_TAG', '@VCS_TAG@')
pyproject_config.set(
    'PYTHON_VERSION_DIST',
    'py'+''.join(python.language_version().split('.'))
)
configure_file(
    input: 'pyproject.toml',
    output: 'pyproject.toml',
    configuration: pyproject_config
)
vcs_tag(input: 'pyproject.toml', output: 'pyproject.orig.toml')

foreach source : root_files
    if source not in ['pyproject.toml', 'requirements.in', '.gitignore', 'README', 'CHANGELOG.md']
        fs.copyfile(source)
    elif source == 'README'
        fs.copyfile(source, 'README.rst')
    endif
endforeach
subdir('ozi_core')
subdir('tests')
root_children = []
foreach child: root_children
    subdir(child)
endforeach
if false
    executable('root_files', root_files)
    executable('root_children', root_children)
endif
if not meson.is_subproject()
    dev = subproject('ozi')
    foreach var : get_option('variables')
        name = var.replace('-', '_')
        set_variable(name, dev.get_variable(name))
    endforeach
    meson.add_dist_script(dev.get_variable('pip'), 'install', 'tomli>=2.0.0')
    meson.add_dist_script(python, '-c', dev.get_variable('meson_dist_setuptools_scm'))
    deps = run_command(python, '-c', dev.get_variable('install_dependencies'), check: true).stdout().strip().split('$$')
    if deps[0] != ''
        meson.add_postconf_script(dev.get_variable('pip'), 'install', deps)
    endif
endif
