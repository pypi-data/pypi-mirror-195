"""Gituptools utilities module."""
__all__ = (
    'get_general_kwargs',
    'has_rtd_site',
    'is_canonical_version',
    'next_version'
    )

import functools
import json
import os
import re
import sys
import typing
import urllib.request

# --------------------------------------------------------------------------- #

FOLDER: str = os.path.abspath(os.path.dirname(__file__))
STATIC: str = os.path.join(FOLDER, 'static')

klass = typing.Optional[type]
file_name = typing.Optional[str]
kallable = typing.Union[type, typing.Callable]

# --------------------------------------------------------------------------- #


@functools.lru_cache(maxsize=32)
def load_static_file(file: str) -> str:
    """Load a file from the package static folder."""
    with open(os.path.join(STATIC, file), mode='r') as f:
        return f.read().strip()


def norm_package_name(package: str) -> str:
    """Normalize a package name."""
    return package.lower().replace('_', '-').strip()


def python_version() -> tuple:
    """Get the major & minor Python version."""
    major, minor = sys.version_info.major, sys.version_info.minor
    version = '.'.join(map(str, (major, minor)))
    return major, version


def get_classifiers() -> list:
    """Get a base set of classifiers."""
    major, version = python_version()
    return [
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        f'Programming Language :: Python :: {major!s}',
        f'Programming Language :: Python :: {version!s}',
        ]


def get_license_files() -> list:
    """Collect license files."""
    return [
        f
        for f in os.listdir(os.curdir)
        if 'license' in f.lower()
        ]


def next_version(package: str) -> str:
    """Pull down the next version number."""
    try:
        pkg = norm_package_name(package)
        url = f'https://pypi.python.org/pypi/{pkg!s}/json'
        with urllib.request.urlopen(url) as f:
            data = json.loads(f.read())
            version = sorted(data.get('releases', []))[-1]
            return str(int(version) + 1)
    except urllib.request.HTTPError:
        return '1'


def get_general_kwargs(package: str) -> dict:
    """Collect vendor agnostic kwargs."""
    _, version = python_version()
    return {
        'version': next_version(package),
        'license_files': get_license_files(),
        'classifiers': get_classifiers(),
        'python_requires': f'>={version!s}',
        'keywords': ['Gitlab', 'Python'],
        }


# -------------------------------------------------------------------- < Docs >


def has_rtd_site(package: str) -> str:
    """Check to see if there is a Read The Docs page."""
    try:
        url = f'https://{norm_package_name(package)!s}.readthedocs.io'
        with urllib.request.urlopen(url):
            return url
    except urllib.request.HTTPError:
        return ''


# --------------------------------------------------- < Environment Variables >


def load_variable_file(fh: str) -> typing.List[str]:
    """Load and split a variable file into a list of slugs."""
    file: str = f'vars.{fh!s}.txt'
    return load_static_file(file).splitlines()


def attribution(cls: klass = None, file: file_name = None) -> kallable:
    """Attribute all variables in a file to a class."""
    if callable(cls) and file:
        for var in load_variable_file(file):
            setattr(cls, var, os.getenv(var))
        return cls
    return functools.partial(attribution, file=file)


# ---------------------------------------------------------------- < Versions >


@functools.lru_cache(maxsize=512)
def is_canonical_version(version: str) -> bool:
    """Verify PEP440 canonical package version schema.

    See Also
    --------
    PEP440 : `Version Identification and Dependency Specification <https://peps.python.org/pep-0440>`_

    """ # noqa
    regex_text = load_static_file('version.regex')
    regex = ''.join(regex_text.splitlines()).strip()
    return re.match(regex, version) is not None
