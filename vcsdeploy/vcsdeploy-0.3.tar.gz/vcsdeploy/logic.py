class VcsError(Exception):
    pass

class UnknownRevisionError(VcsError):
    pass

class AbstractLogic(object):
    def pull(self):
        raise NotImplementedError
    
    def get_current_version(self):
        raise NotImplementedError

    def get_current_revision(self):
        raise NotImplementedError

    def get_list_of_versions(self):
        raise NotImplementedError

    def update_to(self, version):
        raise NotImplementedError

