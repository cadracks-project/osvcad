#!/usr/bin/env python
# coding: utf-8**

"""setuptools based setup module"""

from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

import osvcad

here = path.abspath(path.dirname(__file__))

# Get the long description from the README_SHORT file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name=osvcad.__name__,
    version=osvcad.__release__,
    description=osvcad.__description__,
    long_description=long_description,
    url=osvcad.__url__,
    download_url=osvcad.__download_url__,
    author=osvcad.__author__,
    author_email=osvcad.__author_email__,
    license=osvcad.__license__,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Software Development',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ],
    keywords=['OpenCascade', 'PythonOCC', 'ccad', 'CAD', 'parts', 'json'],
    packages=['osvcad', ],
    install_requires=['jsonpickle', 'networkx', 'ccad'],
    # OCC, scipy and wx cannot be installed via pip
    extras_require={'dev': [], 'test': ['pytest', 'coverage'],},
    package_data={},
    data_files=[],
    entry_points={}
    )
