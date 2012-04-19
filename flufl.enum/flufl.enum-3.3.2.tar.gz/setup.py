# Copyright (C) 2004-2012 by Barry A. Warsaw
#
# This file is part of flufl.enum.
#
# flufl.enum is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.
#
# flufl.enum is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License
# for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with flufl.enum.  If not, see <http://www.gnu.org/licenses/>.

import distribute_setup
distribute_setup.use_setuptools()

from setup_helpers import (
    description, get_version, long_description, require_python)
from setuptools import setup, find_packages


require_python(0x20600f0)
__version__ = get_version('flufl/enum/__init__.py')


setup(
    name='flufl.enum',
    version=__version__,
    namespace_packages=['flufl'],
    packages=find_packages(),
    include_package_data=True,
    maintainer='Barry Warsaw',
    maintainer_email='barry@python.org',
    description=description('README.rst'),
    long_description=long_description('README.rst', 'flufl/enum/NEWS.rst'),
    license='LGPLv3',
    url='http://launchpad.net/flufl.enum',
    download_url='https://launchpad.net/flufl.enum/+download',
    test_suite='flufl.enum.tests',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: '
            'GNU Lesser General Public License v3 or later (LGPLv3+)',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ]
    )
