#!/usr/bin/env python
#This file is part of Tryton.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.

from setuptools import setup, find_packages
import re

info = eval(file('__tryton__.py').read())

requires = ['egenix-mx-base']
for dep in info.get('depends', []):
    if not re.match(r'(ir|res|workflow|webdav)(\W|$)', dep):
        requires.append('trytond_' + dep)

major_version, minor_version, _ = info.get('version', '0.0.1').split('.', 2)
requires.append('trytond >= %s.%s' % (major_version, minor_version))
requires.append('trytond < %s.%s' % (major_version, int(minor_version) + 1))

setup(name='trytond_account_invoice',
    version=info.get('version', '0.0.1'),
    description=info.get('description', ''),
    author=info.get('author', ''),
    author_email=info.get('email', ''),
    url=info.get('website', ''),
    download_url="http://downloads.tryton.org/" + \
            info.get('version', '0.0.1').rsplit('.', 1)[0] + '/',
    package_dir={'trytond.modules.account_invoice': '.'},
    packages=[
        'trytond.modules.account_invoice',
    ],
    package_data={
        'trytond.modules.account_invoice': info.get('xml', []) \
                + info.get('translation', []) \
                + ['invoice.odt'],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'Intended Audience :: Legal Industry',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Natural Language :: English',
        'Natural Language :: French',
        'Natural Language :: German',
        'Natural Language :: Spanish',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Office/Business',
        'Topic :: Office/Business :: Financial :: Accounting',
    ],
    license='GPL-3',
    install_requires=requires,
    zip_safe=False,
    entry_points="""
    [trytond.modules]
    account_invoice = trytond.modules.account_invoice
    """,
)
