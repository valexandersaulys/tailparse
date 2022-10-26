#!/usr/bin/env python3

from distutils.core import setup
import setuptools

setup(
    name="tailparser",
    entry_points={
        "console_scripts": ["tailparser=tailparser.cli:cli"],
    },
    version="0.1",
    description="Log Parser for Nginx logs",
    author="Vincent A. Saulys",
    author_email="vincent@saulys.me",
    url="https://github.com/valexandersaulys/logparser",
    packages=setuptools.find_packages(),
)
