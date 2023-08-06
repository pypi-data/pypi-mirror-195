"""Gitlab specific metadata gathering logic."""
__all__ = ('Gitlab',)

import json
import os
import typing

from . import utils

# --------------------------------------------------------------------------- #


class EnvAttrs(type):

    """Route attributes to the environment."""

    def __getattr__(self, attr: str) -> typing.Union[str, None]:
        """Reroute attributes to the environment."""
        return os.getenv(attr)

    def __bool__(self) -> bool:
        """Is this a Gitlab CICD pipeline runtime?"""
        return self.GITLAB_CI is not None

    def dump(cls) -> None:
        """Make a json dump file."""
        with open('gitlab-kwargs.json', 'w') as f:
            json.dump(cls.kwargs, f, indent=4)

    @property
    def package_name(cls) -> str:
        """Re-case project name."""
        name = cls.PACKAGE or cls.CI_PROJECT_NAME
        return utils.norm_package_name(name)

    @property
    def docs_url(cls) -> str:
        """Determine the documentation url."""
        return utils.has_rtd_site(cls.package_name) or cls.CI_PAGES_URL

    @property
    def kwargs(cls) -> dict:
        """Extract Gitlab CI variables into kwargs for setuptools.setup()."""
        return {
            'author': cls.GITLAB_USER_NAME,
            'maintainer': cls.GITLAB_USER_NAME,
            'author_email': cls.GITLAB_USER_EMAIL,
            'maintainer_email': cls.GITLAB_USER_EMAIL,
            'description': cls.CI_PROJECT_DESCRIPTION,
            'name': cls.package_name,
            'url': cls.CI_PROJECT_URL,
            'download_url': cls.CI_PROJECT_URL,
            'project_urls': {
                'Documentation': cls.docs_url,
                'Gitlab Pages': cls.CI_PAGES_URL,
                'Source Code': cls.CI_PROJECT_URL,
                'Tracker': f'{cls.CI_PROJECT_URL}/-/issues',
                },
            **utils.get_general_kwargs(cls.package_name),
            }


@utils.attribution(file='gitlab')
class Gitlab(metaclass=EnvAttrs):

    """Helper class to access Gitlab environment vars."""

    pass
