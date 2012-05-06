#!/usr/bin/env python

from setuptools import setup, find_packages
 
setup (
    name='django-ical',
    version='1.0',
    description="iCal feeds for Django based on Django's syndication feed framework.",
    author='Ian Lewis',
    author_email='IanMLewis@gmail.com',
    license='MIT License',
    url='https://bitbucket.org/IanLewis/django-ical',
    classifiers=[
      'Development Status :: 3 - Alpha',
      'Environment :: Plugins',
      'Framework :: Django',
      'Intended Audience :: Developers',
      'License :: OSI Approved :: BSD License',
      'Programming Language :: Python',
      'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires = [
        'Django>=1.1',
        'icalendar>=2.0.1',
    ],
    packages=find_packages(),
    test_suite='tests.main',
)
