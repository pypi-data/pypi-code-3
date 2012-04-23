import os
from setuptools import setup, find_packages


version = '1.0.2'
mainainter = 'Mathias Leimgruber'

tests_require = ['plone.app.testing',
                 'plone.mocktestcase']

setup(name='ftw.tooltip',
      version=version,
      description="Apply tooltips dynamically",
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='4teamwork GmbH',
      author_email='mailto:info@4teamwork.ch',
      url='http://plone.org/products/ftw.tooltip/',
      license='GPL2',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['ftw', ],
      include_package_data=True,
      zip_safe=False,
      tests_require=tests_require,
      extras_require=dict(tests=tests_require),
      install_requires=[
          'setuptools',
      ],
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
