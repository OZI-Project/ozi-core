from prompt_toolkit.styles import Style  # pyright: ignore

_style_dict = {
    'dialog': 'bg:#030711 fg:#030711',
    'dialog.body checkbox-list': '#e1e7ef',
    'dialog.body checkbox': '#e1e7ef',
    'dialog.body checkbox-selected': 'bg:#192334',
    'dialog.body checkbox-checked': '#e1e7ef',
    'dialog.body radio-list': '#e1e7ef',
    'dialog.body radio': '#e1e7ef',
    'dialog.body radio-selected': 'bg:#192334',
    'dialog.body radio-checked': '#e1e7ef',
    'button': '#e1e7ef',
    'dialog label': '#e1e7ef',
    'frame.border': '#192334',
    'dialog.body': 'bg:#030711',
    'dialog shadow': 'bg:#192334',
}

_style = Style.from_dict(_style_dict)
