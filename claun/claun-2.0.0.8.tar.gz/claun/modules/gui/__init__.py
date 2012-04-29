
import os
import mimetypes
from claun.core import container


__uri__ = 'gui'
__version__ = '0.1'
__author__ = 'chadijir'
__dependencies__ = []
mapping = (
           '', 'claun.core.communication.server.RedirToRoot',
           '/(.*)', 'GuiRoot'
           )

__app__ = container.web.application(mapping, locals())

index = container.web.template.frender(os.path.join(os.path.dirname(__file__), 'templates', 'index.html'))
mimetypes.init()

class GuiRoot:
    basepath = ['']

    def GET(self, params=None):
        if str(params).strip() != '' or params is None:
            return self.static(params)
        else:
            return self.root()

    def static(self, path):
        if path.startswith('..'):
            raise container.web.badrequest()
        abspath = os.path.join(os.path.dirname(os.path.abspath(__file__)), (os.sep).join(path.split('/')))

        extension = '.%s' % abspath.split('.')[-1]
        if extension in mimetypes.types_map:
            type = mimetypes.types_map[extension]
            container.web.header("Content-Type", type)
            if type.startswith('image'):
                container.web.header("Cache-Control", "max-age=86400, must-revalidate")
        try:

            file = open(abspath, 'r')
            contents = file.read()
            file.close()
            return contents
        except IOError:
            return container.web.notfound()


    def root(self):
        container.web.header("Content-Type", "text/html;charset=utf-8")
        if 'server' in container.configuration['modules']['gui']:
            address = container.configuration['modules']['gui']['server']
        else:
            address = '%s://%s:%s/' % (container.configuration['communication']['client']['default_protocol'], container.configuration['communication']['server']['fqdn'], container.configuration['communication']['server']['port'])

        production = int(container.configuration['modules']['gui'].get('production', 1))

        if 'credentials' in container.configuration['communication']['client']:
            id = container.configuration['communication']['client']['credentials']['username']
            password = container.configuration['communication']['client']['credentials']['password']
            client_authentication = 1 # JS boolean true
            return index(address, client_authentication, id, password, production)
        return index(address, 0, '', '', production)
