from codecs import open
from os import path

from setuptools import setup, find_packages

from memodrop.__about__ import *

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md')) as f:
    long_description = f.read()

setup(
    name=__name__,
    version=__version__,
    description=__description__,
    long_description=long_description,
    url=__url__,
    author=__author__,
    python_requires='~=3.6',
    packages=find_packages(exclude=['docs']),
    include_package_data=True,
    install_requires=[
        'Django==1.11.10',
        'django-bootstrap4==0.0.6',
        'django-fa==1.0.0',
        'django-markdown-deux==1.0.5',
        'djangorestframework==3.7.7',
        'markdown2==2.3.5',
        'numpy==1.14.1',
        'pytz==2018.3',
    ],
    extras_require={
        'dev': [
            'coverage==4.5.1',
            'PyYAML==3.12',
            'setuptools==39.0.1',
            'flake8==3.5.0',
        ],
    },
)
