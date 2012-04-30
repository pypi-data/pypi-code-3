#!/usr/bin/python
# -*- coding: utf-8 -*-


VERSION = (0, 0, 1, 'alpha', 0)

def get_version():
    version = '%s.%s' % (VERSION[0], VERSION[1])
    if VERSION[2]:
        version = '%s.%s' % (version, VERSION[2])
    if VERSION[3]:
        version = '%s-%s' % (version, VERSION[3])
    return version