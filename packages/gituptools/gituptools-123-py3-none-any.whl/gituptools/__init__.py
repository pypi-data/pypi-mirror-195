"""
=====================
Welcome To Gituptools
=====================

|PyPiV| |CircleCi|

|Pipeline| |CodeCov| |QGStatus| 

|Vuln| |Sec| |Bugs| |Rating| |Nlines| 

|PyPiStatus| |PyPiVersion| |PyPiLicence|

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

This is the optional `pyproject.toml` you can use.

.. code-block:: toml

    [build-system]
    requires = ["gituptools"]

Then you can use a regular build job in your `.gitlab-ci.yml` file.

.. code-block:: yaml

    image: python:latest

    stages:
        - Build
        - Publish

    PyPackage:
        stage: Build
        artifacts:
            paths: [dist/*]
        script:
            # option 1: with a pyproject.toml
            - python -m install -U build
            - python -m build
            # option 2: just do it the old way
            - python setup.py sdist bdist_wheel

    PyPi:
        stage: Publish
        needs:
            - job: PyPackage
              artifacts: true
        script:
            - python -m install twine
            - >
                twine upload
                --username $YOUR_USERNAME
                --password $YOUR_PASSWORD
                --verbose
                --non-interactive
                dist/*

|Sonar| 

|QualityGate|

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

.. |CircleCi| image:: https://dl.circleci.com/status-badge/img/circleci/AtZu7a1zFfSHi3o4tjrgvt/Tp7h24z2BnpkTr4MkTYEvh/tree/main.svg?style=svg&circle-token=7523b0cd8ab68680c5642442518ae1bae9368272
   :target: https://dl.circleci.com/status-badge/redirect/circleci/AtZu7a1zFfSHi3o4tjrgvt/Tp7h24z2BnpkTr4MkTYEvh/tree/main

.. |Sonar| image:: https://sonarcloud.io/images/project_badges/sonarcloud-orange.svg
   :target: https://sonarcloud.io/summary/new_code?id=sol-courtney_gituptools

.. |QualityGate| image:: https://sonarcloud.io/api/project_badges/quality_gate?project=sol-courtney_gituptools
   :target: https://sonarcloud.io/summary/new_code?id=sol-courtney_gituptools

.. |QGStatus| image:: https://sonarcloud.io/api/project_badges/measure?project=sol-courtney_gituptools&metric=alert_status
   :target: https://sonarcloud.io/summary/new_code?id=sol-courtney_gituptools

""" # noqa
__all__ = ('setup', 'Gitlab', 'is_canonical_version')


import setuptools

from . import utils
from .gitlab import Gitlab
from .utils import * # noqa


def setup(_dryrun: bool = False, **kwargs):
    """Gituptools setup wrapper."""
    classifiers = kwargs.pop('classifiers', [])
    if Gitlab: # noqa
        kwargs = {
            **kwargs,
            **Gitlab.kwargs
            }
    if 'packages' not in kwargs:
        kwargs['packages'] = setuptools.find_packages(
            exclude=['tests*']
            )
    kwargs['classifiers'] = sorted(set(classifiers + kwargs['classifiers']))
    utils.dump_env_file(kwargs)
    return kwargs if _dryrun else setuptools.setup(**kwargs)
