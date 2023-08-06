'''Gituptools setup file.'''
import os
import setuptools

# --------------------------------------------------------------------------- #

rtd_url = 'https://gituptools.readthedocs.io'
status = '4 - Beta'
version = os.getenv('CI_PIPELINE_IID')
url = os.getenv('CI_PROJECT_URL')

with open('README.md') as f:
    long_description = f.read()

# --------------------------------------------------------------------------- #

if __name__ == '__main__':
    setuptools.setup(
        name='gituptools',
        install_requires=[],
        extras_require={},
        version=version,
        author='Sol Courtney',
        author_email='sol.courtney@gmail.com',
        maintainer='Sol Courtney',
        maintainer_email='sol.courtney@gmail.com',
        description='Setuptools helper for packaging Python from Gitlab.',
        long_description=long_description,
        long_description_content_type='text/markdown',
        license='GPLV3',
        license_files=['LICENCE'],
        include_package_data=True,
        packages=['gituptools', 'gituptools.static'],
        package_dir={'gituptools': 'gituptools'},
        package_data={'gituptools': ['static/*']},
        keywords=['Gitlab', 'DevOps', 'CICD', 'Packaging'],
        python_requires='>=3.8',
        url=url,
        download_url='https://pypi.org/project/gituptools/#files',
        project_urls={
            'Documentation': rtd_url,
            'Gitlab Pages': os.getenv('CI_PAGES_URL'),
            'Source Code': url,
            'Tracker': f'{url}/-/issues',
            },
        entry_points={
            'console_scripts': [],
            'gui_scripts': []
            },
        zip_safe=True,
        platforms=['Windows', 'Linux', 'Solaris', 'Mac OS-X', 'Unix'],
        classifiers=[
            'Development Status :: %s' % status,
            'Topic :: Utilities',
            'Topic :: Software Development :: Libraries',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'Topic :: System :: Archiving :: Packaging',
            'Framework :: Setuptools Plugin',
            'Intended Audience :: Developers',
            'Intended Audience :: Information Technology',
            'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
            'Operating System :: OS Independent',
            'Typing :: Typed',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3 :: Only',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Programming Language :: Python :: 3.10',
            'Programming Language :: Python :: 3.11',
            ]
        )
