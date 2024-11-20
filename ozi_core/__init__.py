# ozi/__init__.py
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
"""Core OZI packaging management plane module.

.. versionremoved:: 1.2
   The module ``filters`` was moved to ``blastpipe.ozi_templates.filters``

.. versionchanged:: 1.12

   The ozi_templates module was moved out of blastpipe.
"""
from importlib.metadata import PackageNotFoundError
from importlib.metadata import version


def current_version() -> str:
    """Returns the currently installed version of OZI.

    .. versionchanged:: 1.14

      Previously was part of the ozi.spec submodule.

    """
    try:
        version_ = version('OZI')
    except PackageNotFoundError:  # pragma: no cover
        version_ = '1.25'
    return version_


__version__ = current_version()
__author__ = 'Eden Ross Duff MSc'
__all__ = ('__version__', '__author__', '__doc__')
