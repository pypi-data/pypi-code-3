# -*- coding: utf-8 -*-

from zope.i18nmessageid import MessageFactory
validatorsMessageFactory = MessageFactory('collective.itvalidators')

import config

def initialize(context):
    """Initializer called when used as a Zope 2 product."""

