"""
=====================
Welcome To Gituptools
=====================

|Pipeline| |CodeCov| |PyPiStatus| |PyPiVersion| |PyPiV| |PyPiLicence|

Gituptools is a helper that unpacks as much of the metadata from a Gitlab
CICD runtime environment into the standard :py:func:`setuptools.setup` call.

Gituptools is **100% standard library Python** with no 3rd party dependencies.

============
Installation
============
gituptools is available on the public pypi.

..  code-block:: shell

    python -m pip install gituptools

===========
Quick Start
===========
To use gituptools, you can simply place this snippet into your `setup.py` file.

..  code-block:: python

    import gituptools

    if __name__ == '__main__':
        gituptools.setup()

.. |PyPiStatus| image:: https://img.shields.io/pypi/status/gituptools.svg
   :target: https://pypi.python.org/pypi/gituptools/

.. |PyPiVersion| image:: https://img.shields.io/pypi/pyversions/gituptools.svg
   :target: https://pypi.python.org/pypi/gituptools/

.. |PyPiV| image:: https://img.shields.io/pypi/v/gituptools.svg
   :target: https://pypi.python.org/pypi/gituptools/

.. |PyPiLicence| image:: https://img.shields.io/pypi/l/gituptools.svg
   :target: https://pypi.python.org/pypi/gituptools/

.. |CodeCov| image:: https://codecov.io/gl/sol-courtney:python-packages/gituptools/branch/develop/graph/badge.svg
   :target: https://codecov.io/gl/sol-courtney:python-packages/gituptools

.. |Pipeline| image:: https://gitlab.com/sol-courtney/python-packages/gituptools/badges/main/pipeline.svg
   :target: https://gitlab.com/sol-courtney/python-packages/gituptools

""" # noqa
__all__ = ('setup', 'Gitlab', 'is_canonical_version')

import setuptools

from .gitlab import Gitlab
from .utils import * # noqa


def setup(_dryrun: bool = False, **kwargs):
    """Gituptools setup wrapper."""
    if Gitlab: # noqa
        kwargs = {**Gitlab.kwargs, **kwargs}
    if 'packages' not in kwargs:
        kwargs['packages'] = setuptools.find_packages()
    return kwargs if _dryrun else setuptools.setup(**kwargs)
