#!python3
#encoding: ascii
from setuptools import setup
import sys
import io

with io.open('README.md', encoding='ascii') as fp:
    long_description = fp.read()

setup(
    name='CoffeeScript',
    version="1.0.2",
    author='OMOTO Kenji',
    description='A bridge to the JS CoffeeScript compiler',
    
    packages=['coffeescript'],
    package_dir={'coffeescript': 'coffeescript'},
    package_data={
        'coffeescript': ['coffee-script.js'],
    },
    
    long_description=long_description,
    url='https://github.com/doloopwhile/Python-CoffeeScript',
    author_email='doloopwhile@gmail.com',
    license="MIT License",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3.2',
        'Programming Language :: JavaScript',
    ],
    install_requires="PyExecJS".split(),
    test_suite="test_coffeescript",
)
