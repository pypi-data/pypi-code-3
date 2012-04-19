from setuptools import setup, find_packages
import sys, os

version = '0.7.7'

setup(name='libacr',
      version=version,
      description="TurboGears2 Content Management Framework",
      long_description="""\
ACR is an open source Python content management system library for  Turbogears
It provides a set of tools to implement CMS functions inside any Turbogears2 application and comes with ACRCms which is a simple and free web content management system implemented with ACR as an example of how to use the library.

ACR divides pages in Slices, which define what should be placed, where it should be placed and how it should be displayed
Each Content can be used in more then one Slice and Slices can be rendered in both complete and preview mode.
Using this interaction you can produce behaviours like having your blog post in its own page and a preview of it inside your main page, or have a photo/video and a preview of it inside your media gallery. ACR already supports previews of HTML documents, images and videos by generating thumbnails for the last two.

ACR currently supports:

    * Multilanguage Content Support
    * Automatic translation using Google when translating content to a new language
    * Content versioning and revert
    * Image Galleries
    * Video Galleries
    * News/Blog? Sections
    * Users permissions
    * Autogenerated Vertical/Horizontal? Menus
    * Internal Search Engine
    * File Attachments
    * Remote Disk to upload and manage files
    * RSS Integration
    * Twitter Integration
    * Static and Dynamic Google Maps
    * Comments by users
    * Automatic Forms generation with email submission of data
""",
      classifiers=[
          "Development Status :: 4 - Beta",
          "Environment :: Web Environment",
          "Framework :: TurboGears",
          "License :: OSI Approved :: GNU General Public License (GPL)",
          "Operating System :: OS Independent",
          "Programming Language :: Python",
          "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
          "Topic :: Software Development :: Libraries :: Python Modules",
      ],
      keywords='turbogears2.extension cms cmf web',
      author='AXANT',
      author_email='acr@axantlabs.com',
      url='http://www.acrcms.org',
      license='LGPL',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      package_data = {'':['*.html', '*.js', '*.css', '*.png', '*.gif', 'plugins/*/static/*.*']},
      zip_safe=False,
      install_requires=[
        "feedparser",
        "tw.jquery",
        "tw.tinymce",
        "tw.dynforms",
        "BeautifulSoup",
        "PIL",
        "sprox",
        "turbomail",
        "TurboGears2 >= 2.0b7",
        "Babel >=0.9.4",
        "zope.sqlalchemy >= 0.4 ",
        "repoze.tm2 >= 1.0a4",
        "repoze.what-quickstart >= 1.0",
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
