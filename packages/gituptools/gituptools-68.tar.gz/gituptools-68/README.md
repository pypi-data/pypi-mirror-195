# Welcome to Gituptools

[![Build](https://gitlab.com/sol-courtney/python-packages/gituptools/badges/main/pipeline.svg)](https://gitlab.com/sol-courtney/python-packages/gituptools)
[![Tests](https://gitlab.com/sol-courtney/python-packages/gituptools/badges/develop/coverage.svg)](https://gitlab.com/sol-courtney/python-packages/gituptools)
[![PyPi](https://badge.fury.io/py/gituptools.svg)](https://pypi.org/project/gituptools/)
[![PyPi Latest](https://img.shields.io/pypi/v/gituptools.svg)](https://pypi.org/project/gituptools/)
[![PyVersions](https://img.shields.io/pypi/pyversions/gituptools.svg)](https://pypi.org/project/gituptools/)
[![Package Status](https://img.shields.io/pypi/status/gituptools.svg)](https://pypi.org/project/gituptools/)
[![PyPI Downloads](https://img.shields.io/pypi/dm/gituptools.svg?label=PyPI%20downloads)](https://pypi.org/project/gituptools/)
[![License](https://img.shields.io/pypi/l/gituptools.svg)](https://gitlab.com/sol-courtney/python-packages/gituptools/-/blob/main/LICENSE)
[![Docs](https://readthedocs.org/projects/gituptools/badge/?version=latest&style=plastic)](https://gituptools.readthedocs.io)
[![Codecov](https://codecov.io/gl/sol-courtney:python-packages/gituptools/branch/develop/graph/badge.svg)](https://codecov.io/gl/sol-courtney:python-packages/gituptools)

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
