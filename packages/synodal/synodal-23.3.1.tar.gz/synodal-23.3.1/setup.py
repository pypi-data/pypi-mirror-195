"""
A minimal Python package with metadata about the code repositories of the
Synodalsoft project.

Source code repository: https://gitlab.com/lino-framework/synodal

Usage example:

>>> from synodal import REPOS_DICT
>>> r = REPOS_DICT['synodal']
>>> print(r.git_repo)
https://gitlab.com/lino-framework/synodal

"""

from setuptools import setup

SETUP_INFO = dict(
    name='synodal',
    version='23.3.1',
    install_requires=[],
    # scripts=['synodal.py'],
    py_modules=['synodal'],
    description="Metadata about the Synodalsoft project",
    license_files=['COPYING'],
    author='Rumma & Ko Ltd',
    author_email='info@lino-framework.org')

SETUP_INFO.update(classifiers="""\
Programming Language :: Python
Programming Language :: Python :: 3
Development Status :: 4 - Beta
Intended Audience :: Developers
License :: OSI Approved :: GNU Affero General Public License v3
Natural Language :: English
Operating System :: OS Independent""".splitlines())

SETUP_INFO.update(long_description=__doc__.strip())

if __name__ == '__main__':
    setup(**SETUP_INFO)
