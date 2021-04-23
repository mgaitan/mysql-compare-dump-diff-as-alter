#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from setuptools import setup


version = "0.1.0"

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

def get_requirements(filename):
    f = open(filename).read()
    reqs = [
            # loop through list of requirements
            x.strip() for x in f.splitlines()
                # filter out comments and empty lines
                if not x.strip().startswith('#')
            ]
    return reqs

setup(
    name='mysql-diff',
    version=version,
    description="""Compare two mysql dumps and output diffs of tables as CREATE TABLE, diff of fields as ALTER""",
    long_description=readme + '\n\n' + history,
    author='Martín Gaitán',
    author_email='gaitan@gmail.com',
    url='https://github.com/mgaitan/mysql-compare-dump-diff-as-alter',
    include_package_data=True,
    py_modules=['mysql-diff'],
    install_requires=get_requirements('requirements.txt'),
    license="BSD",
    zip_safe=False,
    keywords='mysql-diff',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
    ],

    entry_points={
        'console_scripts': [
            'mysql-diff = mysql_diff:main',
        ]
    },

)
