__author__ = 'yablokoff'

class ExistingReferencesError(Exception):
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return repr(self.msg)