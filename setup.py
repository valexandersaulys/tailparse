#!/usr/bin/env python3

from distutils.core import setup
import setuptools


setup(
    name="tailparse",
    entry_points={
        "console_scripts": ["tailparse=tailparse.cli:cli"],
    },
    version=0.2,
    description="Log Parser for Nginx logs",
    author="Vincent A. Saulys",
    author_email="vincent@saulys.me",
    url="https://github.com/valexandersaulys/tailparse",
    packages=setuptools.find_packages(),
)
