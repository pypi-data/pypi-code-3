import os.path
from setuptools import setup, find_packages


_long_description = """"""

setup(
    name='django-bootstrap-static-files',
    version='2.0.2',  # mapped to Twitter's bootstrap version
    description='Twitter bootstrap static files for Django.',
    long_desctiption=_long_description,
    author='Ash Christopher',
    author_email='ash.christopher@gmail.com',
    url='https://github.com/ashchristopher/django-bootstrap-static-files',
    packages=find_packages(),
    license='Apache License 2.0',
    include_package_data=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    zip_safe=False,
)

