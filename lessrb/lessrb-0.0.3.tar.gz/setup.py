# -*- coding: utf-8 -
#


import os
from setuptools import setup, find_packages
import sys


setup(
    name="lessrb",
    version="0.0.3",
    description="Wrapper for ruby less so that it's in a virtualenv.",
    author="Michael Axiak",
    author_email="mike@axiak.net",
    license="Apache 2",
    include_package_data=True,
    zip_safe=False,
    packages=['lessrb'],
    entry_points={
        'console_scripts':
            ['lessc=lessrb:run'],
        }
    )
