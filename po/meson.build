i18n = import('i18n')
# define GETTEXT_PACKAGE
xgettext_args = [
  '--from-code=utf-8',
  '--package-name=ozi-core',
]
i18n.gettext(meson.project_name(), install_dir: python.get_install_dir() / '@0@-@1@.data'.format(meson.project_name().underscorify().to_lower(), meson.project_version()) / 'data' / get_option('localedir'), install: true, args: xgettext_args)
