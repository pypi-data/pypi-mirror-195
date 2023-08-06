[![PyPi Latest](https://img.shields.io/pypi/v/gituptools.svg)](https://pypi.org/project/gituptools/)
[![Build](https://gitlab.com/sol-courtney/python-packages/gituptools/badges/main/pipeline.svg)](https://gitlab.com/sol-courtney/python-packages/gituptools)
[![Codecov](https://codecov.io/gl/sol-courtney:python-packages/gituptools/branch/develop/graph/badge.svg)](https://codecov.io/gl/sol-courtney:python-packages/gituptools)
[![Docs](https://readthedocs.org/projects/gituptools/badge/?version=latest)](https://gituptools.readthedocs.io)
[![CircleCI](https://dl.circleci.com/status-badge/img/circleci/AtZu7a1zFfSHi3o4tjrgvt/Tp7h24z2BnpkTr4MkTYEvh/tree/main.svg?style=svg&circle-token=7523b0cd8ab68680c5642442518ae1bae9368272)](https://dl.circleci.com/status-badge/redirect/circleci/AtZu7a1zFfSHi3o4tjrgvt/Tp7h24z2BnpkTr4MkTYEvh/tree/main)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=sol-courtney_gituptools&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=sol-courtney_gituptools)

[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=sol-courtney_gituptools&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=sol-courtney_gituptools)
[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=sol-courtney_gituptools&metric=vulnerabilities)](https://sonarcloud.io/summary/new_code?id=sol-courtney_gituptools)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=sol-courtney_gituptools&metric=bugs)](https://sonarcloud.io/summary/new_code?id=sol-courtney_gituptools)
[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=sol-courtney_gituptools&metric=reliability_rating)](https://sonarcloud.io/summary/new_code?id=sol-courtney_gituptools)
[![Lines of Code](https://sonarcloud.io/api/project_badges/measure?project=sol-courtney_gituptools&metric=ncloc)](https://sonarcloud.io/summary/new_code?id=sol-courtney_gituptools)

[![Package Status](https://img.shields.io/pypi/status/gituptools.svg)](https://pypi.org/project/gituptools/)
[![PyVersions](https://img.shields.io/pypi/pyversions/gituptools.svg)](https://pypi.org/project/gituptools/)
[![PyPI Downloads](https://img.shields.io/pypi/dm/gituptools.svg?label=PyPI%20downloads)](https://pypi.org/project/gituptools/)

[![License](https://img.shields.io/pypi/l/gituptools.svg)](https://gitlab.com/sol-courtney/python-packages/gituptools/-/blob/main/LICENSE)

# Welcome to Gituptools

Gituptools is a helper for packing Python on Gitlab CICD runners.  It basically gets as much from the runtime environment as it can to fill in all the packaging metadata that a typical `setup.py` file needs.

Gituptools is **100% standard library**.  No 3rd party dependencies.

See the [Documentation](https://gituptools.readthedocs.io) for more help.

## Installation

From [PyPI](https://pypi.org/project/gituptools/) directly:

```
pip install gituptools
```

## Examples

```py
import gituptools

if __name__ == '__main__':
    gituptools.setup()
```

---

[![SonarCloud](https://sonarcloud.io/images/project_badges/sonarcloud-orange.svg)](https://sonarcloud.io/summary/new_code?id=sol-courtney_gituptools)
[![Quality gate](https://sonarcloud.io/api/project_badges/quality_gate?project=sol-courtney_gituptools)](https://sonarcloud.io/summary/new_code?id=sol-courtney_gituptools)

