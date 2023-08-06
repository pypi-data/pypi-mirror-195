"""
=====================
Welcome To Gituptools
=====================

|PyPiV| |Pipeline| |CodeCov|

|Nlines| |Bugs| |Vuln| |Sec| |Rating|

|PyPiStatus| |PyPiVersion| 

|PyPiLicence|

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

Then you can use a regular build job in your `.gitlab-ci.yml` file.

.. code-block:: yaml

    PyPackage:
        script: python -m build

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

.. |Nlines| image:: https://sonarcloud.io/api/project_badges/measure?project=sol-courtney_gituptools&metric=ncloc
   :target: https://sonarcloud.io/summary/new_code?id=sol-courtney_gituptools

.. |Vuln| image:: https://sonarcloud.io/api/project_badges/measure?project=sol-courtney_gituptools&metric=vulnerabilities
   :target: https://sonarcloud.io/summary/new_code?id=sol-courtney_gituptools

.. |Sec| image:: https://sonarcloud.io/api/project_badges/measure?project=sol-courtney_gituptools&metric=security_rating
   :target: https://sonarcloud.io/summary/new_code?id=sol-courtney_gituptools

.. |Bugs| image:: https://sonarcloud.io/api/project_badges/measure?project=sol-courtney_gituptools&metric=bugs
   :target: https://sonarcloud.io/summary/new_code?id=sol-courtney_gituptools

.. |Rating| image:: https://sonarcloud.io/api/project_badges/measure?project=sol-courtney_gituptools&metric=reliability_rating
   :target: https://sonarcloud.io/summary/new_code?id=sol-courtney_gituptools

""" # noqa
__all__ = ('setup', 'Gitlab', 'is_canonical_version')


import setuptools

from . import utils
from .gitlab import Gitlab
from .utils import * # noqa


def setup(_dryrun: bool = False, **kwargs):
    """Gituptools setup wrapper."""
    if Gitlab: # noqa
        kwargs = {
            **Gitlab.kwargs,
            **kwargs
            }
    if 'packages' not in kwargs:
        kwargs['packages'] = setuptools.find_packages(
            exclude=['tests/', 'docs/']
            )
    utils.dump_env_file(kwargs)
    return kwargs if _dryrun else setuptools.setup(**kwargs)
