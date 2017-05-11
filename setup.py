#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mithril
# @Date:   2016-01-20 09:22:44
# @Last Modified by:   mithril
# @Last Modified time: 2017-05-11 15:20:25

from __future__ import unicode_literals, print_function, absolute_import
import sys
from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), "r", encoding='utf-8') as f:
    long_description = f.read()


install_requires = [
]


setup(
    name='sqlqueue',
    version='1.0.1',

    description='A simple queue lib base on sqlite3',
    long_description=long_description,

    author='Mithril',
    author_email='eromoe@users.noreply.github.com',

    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',

        'Intended Audience :: Developers',
        'Operating System :: OS Independent',

        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',

        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Object Brokering',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],

    keywords='sql sqlite3 local file queue',
    install_requires=install_requires,

    py_modules=['sqlqueue'],

)
