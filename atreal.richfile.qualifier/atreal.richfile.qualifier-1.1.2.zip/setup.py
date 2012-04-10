from setuptools import setup, find_packages
import os

version = '1.1.2'

setup(name='atreal.richfile.qualifier',
      version=version,
      description="System to enrich a file content type in Plone with a marker interface regarding its mimetype.",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='plone atreal richfile qualifier',
      author='atReal',
      author_email='contact@atreal.fr',
      url='http://svn.plone.org/svn/collective/atreal.richfile.qualifier/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['atreal', 'atreal.richfile'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'atreal.filestorage.common',
          'collective.monkeypatcher',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
