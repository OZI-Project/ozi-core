"""This script generates locales based on ozi_core/data files."""

import glob  # pragma: no cover
import os  # pragma: no cover
import pprint  # pragma: no cover
from pathlib import Path  # pragma: no cover

import yaml  # pragma: no cover


def load_locale_data() -> dict[str, str]:  # pragma: no cover
    data = {}
    files = glob.glob(os.path.join(Path(__file__).parent / 'data', '*.yml'))
    for f in files:
        loc = os.path.splitext(os.path.basename(f))[0]
        with open(f, 'r', encoding='utf8') as fh:
            data[loc] = yaml.safe_load(fh)
    return data


if __name__ == '__main__':
    text = f"""# This file was generated at build time. DO NOT EDIT
data = {pprint.pformat(load_locale_data(), width=100)}"""
    print(text)
