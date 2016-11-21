#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os.path import join
from setuptools import setup, find_packages

from ast import literal_eval
import re

def get_version(source='lib/eye_reasoner.py'):
    with open(source) as f:
        for line in f:
            if line.startswith('__version__'):
                return literal_eval(line.partition('=')[2].lstrip())
    raise ValueError("VERSION not found")

README = ''
with open('README.rst', 'r') as f:
    README = f.read()

def load_req(name):
    req = []
    with open(join('requirements.d', '%s.txt' % name), 'r') as f:
        # Get requirements depencies as written in the file
        req = [ i[:-1] for i in f if i[0] != "#" ]
    return req

setup(name = 'eye_reasoner',
      version = get_version(),
      package_dir = {'': 'lib'},
      packages = find_packages(where='lib'),
      description = 'A wrapper for the EYE reasoner',
      long_description = README,
      author='Pierre-Antoine Champin',
      author_email='pierre-antoine.champin@liris.cnrs.fr',
      license='LGPL v3',
      platforms='OS Independant',
      url='http://github.com/pchampin/eye_reasoner',
      include_package_data=True,
      install_requires = load_req('base'),
      setup_requires = load_req('setup'),
      tests_require = load_req('tests'),
      scripts=[],
    )
