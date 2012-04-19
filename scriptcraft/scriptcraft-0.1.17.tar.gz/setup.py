#!/usr/bin/env python
#-*- coding:utf-8 -*-

from setuptools import setup, find_packages
import os

PROJECT_NAME = 'scriptcraft'

def _fullsplit(path, result=None):
    """
    Split a pathname into components (the opposite of os.path.join) in a
    platform-neutral way.
    """
    if result is None:
        result = []
    head, tail = os.path.split(path)
    if head == '':
        return [tail] + result
    if head == path:
        return result
    return _fullsplit(head, [tail] + result)

def _find_packages_and_data_files():
    packages = []
    data_files = []
    for dirpath, dirnames, filenames in os.walk(PROJECT_NAME):
        for i, dirname in enumerate(dirnames):
            if dirname.startswith('.'): del dirnames[i]
        if '__init__.py' in filenames:
            packages.append('.'.join(_fullsplit(dirpath)))
        elif filenames:
            data_files.append([dirpath, [os.path.join(dirpath, f) for f in filenames]])
    return packages, data_files

if __name__ == "__main__":
    packages, _ = _find_packages_and_data_files()
    setup(
        name=PROJECT_NAME,
        version='0.1.17',
        install_requires = [
            'PIL==1.1.7',
        ],
        packages = packages,
        include_package_data = True,
        author = "Krzysztof Medrela",
        author_email = "krzysiumed@gmail.com",
        description = "scriptcraft game",
        license = "GPLv3",
        keywords = [PROJECT_NAME, 'game'],
        url = "http://github.com/krzysiumed/scriptcraft",
        entry_points = {
            'gui_scripts': [
                'scriptcraft = scriptcraft.client:run',
            ],
        }
    )
