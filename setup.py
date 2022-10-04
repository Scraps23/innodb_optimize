#!/usr/bin/env python
from setuptools import setup

def read(filename):
    with open(filename, encoding='utf8', errors='ignore') as file:
        return file.read()

setup(
    name="innodb_optimize",
    version='0.1.4',
    description="Automated optimizer for MySQL InnoDB configurations",
    long_description=read("README.rst"),
    author="Ben Nassif",
    author_email="bennassif@gmail.com",
    maintainer="Ben Nassif",
    maintainer_email="bennassif@gmail.com",
    url="https://www.linkedin.com/in/ben-nassif/",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
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
)
