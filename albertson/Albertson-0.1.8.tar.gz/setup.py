#!/usr/bin/env python
try:
    from setuptools import setup
except ImportError, err:
    from distutils.core import setup

setup(
    name='Albertson',
    version="0.1.8",
    description="Easy to use, scalable, counters powered by Amazon's DynamoDB",
    author="Sean O'Connor",
    author_email="sean@focuslab.io",
    url="https://github.com/FocusLab/Albertson",
    packages=['albertson', 'albertson.dynamodb_utils'],
    license="BSD",
    long_description=open('README.md').read(),
    install_requires=['boto>=2.2.2'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    test_suite='nose.collector',
)
