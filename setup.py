#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')


requirements = [
    'sphinx',
    'docopt',
    'python-magic',
    'pdfminer.six',
    'six',
    'ezodf',
    'lxml'
]


# To install, run:
# sudo PYTHONPATH=/usr/local/lib/python/ LD_LIBRARY_PATH=/usr/local/lib/ make install
# because tulip puts its python modules and its libraries in /usr/local/lib
try:
    import tulip
except Exception as e:
    requirements.extend([
        'tulip-python',
        'tulipgui-python'])

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='poulpe',
    version='0.0.5',
    description="Automatic criminal analysis graph generator",
    long_description=readme + '\n\n' + history,
    author="Edouard Klein",
    author_email='edou -at- rdklein.fr',
    url='https://github.com/edouardklein/poulpe',
    packages=[
        'poulpe',
    ],
    package_dir={'poulpe':
                 'poulpe'},
    entry_points={'console_scripts': ['poulpe = poulpe.main:main'],},
    include_package_data=True,
    # Only require tulip if 'pip install tulip' works on the system
    # (currently (End of 2015), only MacOSX and Windows are supported)
    install_requires=requirements,
    license='AGPL',
    zip_safe=False,
    keywords='poulpe',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: MacOS X',
        'Environment :: X11 Applications',
        'Intended Audience :: Legal Industry',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Telecommunications Industry',
        'License :: OSI Approved :: ISC License (ISCL)',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.5',
        'Operating System :: POSIX',
        'Topic :: Scientific/Engineering :: Visualization',
        'Topic :: Security',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
