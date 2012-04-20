

class DocType(object):

    def __init__(self, name, extensions, requires_conversion=True):
        self.name = name
        self.extensions = extensions
        self.requires_conversion = requires_conversion


CONVERTABLE_TYPES = {
    'pdf': DocType(u'PDF', ('pdf',), False),
    'word': DocType(u'Word Document', ('doc', 'docx', 'odt', 'sxw')),
    'excel': DocType(u'Excel File', ('xls', 'xlsx', 'xlt', 'ods')),
    'ppt': DocType(u'Powerpoint', ('ppt', 'pptx', 'pps', 'ppa', 'pwz',
                                  'odp', 'sxi')),
    'html': DocType(u'HTML File', ('htm', 'html', 'xhtml')),
    'rft': DocType(u'RTF', ('rtf',))
}

EXTENSION_TO_ID_MAPPING = {}

for id, doc in CONVERTABLE_TYPES.items():
    for ext in doc.extensions:
        EXTENSION_TO_ID_MAPPING[ext] = id


GROUP_VIEW_DISPLAY_TYPES = (
    'Folder',
    'Large Plone Folder',
    'Plone Site',
    'Topic'
)
