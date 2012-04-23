from setuptools import setup, find_packages
import os

version = open('simplelayout/types/common/version.txt').read().strip()

setup(name='simplelayout.types.common',
      version=version,
      description="simplelayout common types",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='Mathias LEIMGRUBER (4teamwork)',
      author_email='m.leimgruber@t4amwork.ch',
      url='http://plone.org/products/simplelayout.types.common',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['simplelayout', 'simplelayout.types'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
