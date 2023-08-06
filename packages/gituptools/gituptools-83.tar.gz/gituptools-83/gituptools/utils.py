"""Gituptools utilities module."""
__all__ = ('is_canonical_version',)

import functools
import os
import re
import typing

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
