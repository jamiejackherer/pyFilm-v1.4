#!/usr/bin/python3
# -*- coding: utf-8 -*-

# https://github.com/jamiejackherer/pyfilm/wiki

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 jamiejackherer jamiejackherer@gmail.com

from setuptools import setup, find_packages
from pyfilm import __version__, __author__, __email__, __source__, __license__

setup(
    name="pyfilm",
    version=__version__,
    description="PyFilm is the easiest way to search for and automatically download films.",
    long_description="""PyFilm is the easiest way to search for and automatically download films,
        it's written entirely in python3 and is incredibly simple to use.""",
    Keywords="films download movies tv shows",
    author=__authour__,
    author_email=__email__,
    url="https://github.com/jamiejackherer/pyfilm/wiki",
    license="New BSD License",
    classifiers=["Development Status :: 4 - Beta",
                 "Intended Audience :: End Users/Desktop",
                 "License :: OSI Approved :: New BSD License",
                 "Natural Language :: English",
                 "Operating System :: OS Independent",
                 "Programming Language :: Python :: 3",
                " Environment :: Web Environment",
                 "Topic :: Internet :: WWW/HTTP",
                 "Topic :: Multimedia :: Video"],
    install_requires=[
        "bs4>=4.4.1",
        "hurry",
        "pandas>=0.18.1",
        "pyprind>=2.9.8",
        "requests>=2.2.1"
    ]   
)
