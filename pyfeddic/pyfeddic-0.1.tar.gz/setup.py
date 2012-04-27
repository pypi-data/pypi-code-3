"""
Python Federal Reserve E-Payments Routing Directory Library

See ``README.mkd`` for usage advice.

"""
import os
import re

try:
    import setuptools
except ImportError:
    import distutils.core
    setup = distutils.core.setup
else:
    setup = setuptools.setup


def _get_version():
    path = os.path.join(PATH_TO_FILE, 'pyfeddic', '__init__.py')
    version_re = r".*__version__ = '(.*?)'"
    fo = open(path)
    try:
        return re.compile(version_re, re.S).match(fo.read()).group(1)
    finally:
        fo.close()


def _get_long_description():
    path = os.path.join(PATH_TO_FILE, 'README.mkd')
    fo = open(path)
    try:
        return fo.read()
    finally:
        fo.close()


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

PATH_TO_FILE = os.path.dirname(__file__)
VERSION = _get_version()
LONG_DESCRIPTION = _get_long_description()


setup(
    name='pyfeddic',
    version=VERSION,
    description='Python Federal Reserve E-Payments Routing Directory Library',
    author='Marshall Jones',
    author_email='marshall@poundpay.com',
    url='https://github.com/mjallday/pyfeddic',
    install_requires=parse_requirements('requirements.txt'),
    dependency_links=parse_dependency_links('requirements.txt'),
    packages=['pyfeddic'],
    include_package_data=True,
    test_suite='nose.collector',
    entry_points={},
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],
)
