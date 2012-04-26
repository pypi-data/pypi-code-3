#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup

f = open('README.rst')
long_description = f.read().strip()
long_description = long_description.split('split here', 1)[1]
f.close()

# Ridiculous as it may seem, we need to import multiprocessing and
# logging here in order to get tests to pass smoothly on python 2.7.
try:
    import multiprocessing
    import logging
except Exception:
    pass

setup(
    name='fedmsg',
    version='0.1.1',
    description="Fedora Messaging Client API",
    long_description=long_description,
    author='Ralph Bean',
    author_email='rbean@redhat.com',
    url='http://github.com/ralphbean/fedmsg/',
    license='LGPLv2+',
    install_requires=[
        'pyzmq',
        'simplejson',
        'fabulous',
        'moksha>=0.7.1',
    ],
    tests_require=['nose'],
    test_suite='nose.collector',
    packages=[
        'fedmsg',
        'fedmsg.commands',
        'fedmsg.consumers',
        'fedmsg.producers',
    ],
    include_package_data=True,
    zip_safe=False,
    entry_points = {
        'console_scripts': [
            "fedmsg-logger=fedmsg.commands.logger:logger",
            "fedmsg-status=fedmsg.commands.status:status",
            "fedmsg-tail=fedmsg.commands.tail:tail",
            "fedmsg-hub=fedmsg.commands.hub:hub",
            "fedmsg-relay=fedmsg.commands.relay:relay",
            "fedmsg-config=fedmsg.commands.config:config",
        ],
        'moksha.consumer': [
            "fedmsg-relay=fedmsg.consumers.relay:RelayConsumer",
        ],
        'moksha.producer': [
            "heartbeat=fedmsg.producers.heartbeat:HeartbeatProducer",
        ],
    }
)
