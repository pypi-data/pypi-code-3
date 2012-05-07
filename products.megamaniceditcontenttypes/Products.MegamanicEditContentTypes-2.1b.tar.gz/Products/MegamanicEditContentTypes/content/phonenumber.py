"""Definition of the Contact phone number content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-

from Products.MegamanicEditContentTypes.interfaces import IPhonenumber
from Products.MegamanicEditContentTypes.config import PROJECTNAME

PhonenumberSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    atapi.StringField(
        name='phone',
        required=1,
        searchable=1,
        default='',
        validators=('isInternationalPhoneNumber',),
        size=40,
    )

))

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

PhonenumberSchema['title'].storage = atapi.AnnotationStorage()
PhonenumberSchema['title'].widget.visible = {'edit' : 'invisible', 'view':'visible'}
PhonenumberSchema['description'].storage = atapi.AnnotationStorage()


schemata.finalizeATCTSchema(
    PhonenumberSchema,
    folderish=True,
    moveDiscussion=False
)

from MegamanicEdit.MegamanicEdit import MegamanicEditable, tools

from AccessControl import ClassSecurityInfo
from Globals import InitializeClass

class Phonenumber(folder.ATFolder, MegamanicEditable.MegamanicEditable):
    """Description of the Example Type"""
    implements(IPhonenumber)

    meta_type = "Phonenumber"
    schema = PhonenumberSchema

    security = ClassSecurityInfo()

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-

    security.declarePublic('getMegamanicEditableFields')
    def getMegamanicEditableFields(self):
        """Returns names of the fields we can edit."""
        return ('phone', 'description')

    security.declarePublic('validateMainField')
    def validateMainField(self, phone=''):
        """Validates that the value given is acceptable."""
        return not self.schema['phone'].validate(phone, self)

    def Title(self):
        """Returns a proper title."""
        return 'Phone number'

InitializeClass(Phonenumber)
atapi.registerType(Phonenumber, PROJECTNAME)
tools.setup(Phonenumber)
