# -*- coding: utf-8 -*-
from pathlib import Path
from setuptools import setup, find_packages

def get_packages(package):
    """
    Return root package and all sub-packages.
    """
    return [str(path.parent) for path in Path(package).glob("**/__init__.py")]

try:
    long_description = open("README.rst").read()
except IOError:
    long_description = "A multi-purpose tool for interacting with Switch game files - a Switch Army Knife. Written in Python. Originally developed to remove titlerights and create multicontent NSP/XCI files, though over time has expanded to have significantly more features, specializing in batch processing and file information."

setup(
    name="nstool",
    version="1.0.5",
    description="Nintendo Switch Cleaner and Builder",
    long_description=long_description,
    license="MIT",
    author="julesontheroad",
    author_email="julesontheroad@gmail.com",
    url="https://github.com/julesontheroad/NSC_BUILDER",
    packages=get_packages('py'),
    package_data={
        'py/ztools': ['*.txt', '*.json'],
        'py/zconfig': ['*.txt', '*.json'],
        'py/zconfig/DB': ['*.txt', '*.json'],
        'py/zconfig/Regional bat': ['*.txt', '*.json'],
        'py/zconfig/Regional bat/zconfig': ['*.txt', '*.json'],
        },
    python_requires='>=3.10',
    install_requires=[
        'urllib3',
        'unidecode',
        'tqdm',
        'bs4',
        'requests',
        'image',
        'pycryptodome',
        'pykakasi',
        'httpx==0.13.3',
        'googletrans',
        'chardet',
        'eel',
        'bottle',
        'zstandard',
        'colorama',
        'google-auth-httplib2',
        'google-auth-oauthlib',
        'oauth2client',
        'comtypes',
        ],
    entry_points={"console_scripts": ["nstool=py.ztools.squirrel:main"]},
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.10",
    ]
)
