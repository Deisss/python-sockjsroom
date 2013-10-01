#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import sockjsroom

# Setup library
setup(
    # Pypi name
    name     = "sockjsroom",
    # Release version
    version  = sockjsroom.__version__,
    # Associated package
    packages = find_packages(),

    # Author
    author       = "Deisss",
    author_email = "deisss@free.fr",

    # Package description
    description      = "Sockjs-tornado multi room system",
    long_description = open('README.md').read(),

    # Require sockjs-tornado
    install_requires = ["tornado", "sockjs-tornado"],

    # Add MANIFEST.in
    include_package_data = True,

    # Github url
    url = "https://github.com/Deisss/python-sockjsroom",

    # Metadata
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.6",
        "Topic :: Communications",
    ],
)