from geoserver.support import atom_link, xml_property, write_bool, ResourceInfo
import string

def workspace_from_index(catalog, node):
    name = node.find("name")
    return Workspace(catalog, name.text)

class Workspace(ResourceInfo): 
    resource_type = "workspace"

    def __init__(self, catalog, name):
        super(Workspace, self).__init__()
        self.catalog = catalog
        self.name = name

    @property
    def href(self):
        return "%s/workspaces/%s.xml" % (self.catalog.service_url, self.name)

    @property
    def coveragestore_url(self):
        return "%s/workspaces/%s/coveragestores.xml" % (self.catalog.service_url, self.name)

    @property
    def datastore_url(self):
        return "%s/workspaces/%s/datastores.xml" % (self.catalog.service_url, self.name)

    enabled = xml_property("enabled", lambda x: string.lower(x) == 'true')
    writers = dict(
        enabled = write_bool("enabled")
    )

    def __repr__(self):
        return "%s @ %s" % (self.name, self.href)
