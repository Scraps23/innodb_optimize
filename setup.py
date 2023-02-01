#!/usr/bin/env python
from setuptools import setup
import re

def read(filename):
    with open(filename, encoding='utf8', errors='ignore') as file:
        return file.read()

def get_version() -> str:
    """Get the version string from the module's __init__ file."""
    with open("bootstrap/__init__.py") as init:
        version = re.search(r'[\'"]\S\d*.\d*.\d*\S*[\'"]', init.read())
        return version.group().strip('"').strip("'")

setup(
    name="innodb_optimize",
    version=get_version(),
    description="Automated optimizer for MySQL InnoDB configurations",
    long_description=read("README.rst"),
    author="Ben Nassif",
    author_email="bennassif@gmail.com",
    maintainer="Ben Nassif",
    maintainer_email="bennassif@gmail.com",
    url="https://github.com/Scraps23/innodb_optimize",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: Unix",
        "Topic :: Database :: Database Engines/Servers",
        "Topic :: System :: Systems Administration",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    license=read("LICENSE"),
    packages=['bootstrap',],
    install_requires=["fire",],
    scripts=['bootstrap/innodb-optimize',]
)
