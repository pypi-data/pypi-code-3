""" Views exhibit configuration interfaces
"""
from zope.interface import Interface
from zope.schema import TextLine

class IVisualizationView(Interface):
    """ Access / update exhibit view configuration
    """
    label = TextLine(title=u'Label for exhibit view')
    section = TextLine(title=u"Section of this view, e.g. Exhibit, Google, etc")

class IViewDirective(Interface):
    """
    Register a daviz view
    """
    name = TextLine(
        title=u"The name of the view.",
        description=u"The name shows up in URLs/paths. For example 'daviz.map'",
        required=True,
        default=u'',
        )

class IVisualizationViews(Interface):
    """ Utility to get available visualization views
    """
