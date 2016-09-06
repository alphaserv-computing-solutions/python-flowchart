#!/usr/bin/env python
"""
flowchart

Flowchart

Copyright 2016 AlphaServ Computing Solutions
"""

from __future__ import print_function

import os

from setuptools import setup, find_packages


with open('requirements.txt') as req_file:
    requirements = []
    for line in req_file:
        line = line.split('#', 1)[0].strip()
        if line:
            requirements.append(line)


__version__ = '0.1.0'  # Overwritten below
with open('flowchart/version.py') as handle:
    exec(handle.read())  # pylint: disable=exec-used

setup(
    name='flowchart',
    version=__version__,
    description='Flowchart',
    url='https://github.com/alphaserv-computing-solutions/flowchart',
    author='Alpha',
    author_email='alpha@alphaservcomputing.solutions',
    license='Other/Proprietary License',
    install_requires=requirements,
    packages=find_packages(),
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'License :: Other/Proprietary License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ]
)
