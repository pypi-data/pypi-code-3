#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" distribute- and pip-enabled setup.py for pywaveclus """

from distribute_setup import use_setuptools
use_setuptools()
from setuptools import setup, find_packages

import re


def parse_requirements(file_name):
    requirements = []
    for line in open(file_name, 'r').read().split('\n'):
        if re.match(r'(\s*#)|(\s*$)', line):
            continue
        if re.match(r'\s*-e\s+', line):
            requirements.append(re.sub(r'\s*-e\s+.*#egg=(.*)$', r'\1', line))
        elif re.match(r'\s*-f\s+', line):
            pass
        else:
            requirements.append(line)

    return requirements


def parse_dependency_links(file_name):
    dependency_links = []
    for line in open(file_name, 'r').read().split('\n'):
        if re.match(r'\s*-[ef]\s+', line):
            dependency_links.append(re.sub(r'\s*-[ef]\s+', '', line))

    return dependency_links

def get_version():
    import pywaveclus
    return pywaveclus.__version__

setup(
    name='pywaveclus',
    
    packages = ['pywaveclus','pywaveclus/cluster','pywaveclus/data',\
                'pywaveclus/detect','pywaveclus/dsp','pywaveclus/extract',\
                'pywaveclus/process','pywaveclus/template'],
    package_data={'pywaveclus': ['bin/*']},
    scripts=['scripts/pycluster.py'],
    version=get_version(),

    include_package_data=True,

    install_requires=parse_requirements('requirements.txt'),
    dependency_links=parse_dependency_links('requirements.txt'),

    test_suite="nose.collector",
)
