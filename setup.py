#!/usr/bin/env python

# Copyright 2011-2012 Eric Wendelin
#
# This is free software, licensed under the Apache License, Version 2.0,
# available in the accompanying LICENSE.txt file.

from distutils.core import setup
import sys

sys.path.append('lcov_cobertura')
import lcov_cobertura

setup(name='lcov_cobertura',
    version='1.0',
    description='LCOV to Cobertura XML converter',
    author='Eric Wendelin',
    author_email='me@eriwen.com',
    url='http://eriwen.github.com/lcov-to-cobertura-xml/',
    download_url='https://github.com/eriwen/lcov-to-cobertura-xml/downloads',
    long_description=lcov_cobertura.LcovCobertura.__doc__,
    package_dir={'': 'lcov_cobertura'},
    provides=['lcov_cobertura'],
    py_modules=['lcov_cobertura'],
    classifiers=['Development Status :: 5 - Production/Stable',
                 'Intended Audience :: Developers',
                 'Natural Language :: English',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python :: 2',
                 'License :: OSI Approved :: Apache Software License',
                 'Topic :: Software Development :: Testing',
                 'Topic :: Software Development :: Quality Assurance'
    ],
    keywords='lcov cobertura',
    license='Apache License, Version 2.0'
)