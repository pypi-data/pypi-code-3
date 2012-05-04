#!/usr/bin/python

import os
from distutils.core import setup

def get_name_version():
    basedir = os.path.dirname(__file__)
    with open(os.path.join(basedir, 'monupco_openshift_python/version.py')) as f:
        (name, version) = (None, None)
        exec(f.read())
        return (name, version)
    raise RuntimeError('No version info found.')

with open('README.txt') as file:
    long_description = file.read()

(name, version) = get_name_version()

setup(
    name=name,
    version=version,
    description='monupco.com registration agent for OpenShift / Python applications',
    author='Alexander Todorov',
    author_email='atodorov@nospam.otb.bg',
    url = 'http://github.com/monupco/monupco-openshift-python',
    packages=['monupco_openshift_python'],
    scripts=['monupco-openshift-python'],
    keywords = ['openshift', 'monupco', 'updates', 'cloud'],
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: 5 - Production/Stable",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Topic :: System",
        "Topic :: System :: Monitoring",
        "Topic :: System :: Systems Administration",
        ],
    long_description = long_description,
     )
