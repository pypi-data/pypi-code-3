"""
Content interfaces
------------------

The interfaces in this module define the various aspects a content object
must implement to be usable by membrane as a user or a group. The interfaces
are  based on the standard `PluggableAuthService` interfaces. This means that
the user will often be passed in as a parameter, even though it is already
called on the user object.

Content objects may either implement these interfaces directly, or be adaptable
to them.
"""
from zope.interface import Interface

from Products.PluggableAuthService.interfaces.authservice import \
     IPropertiedUser
from Products.PluggableAuthService.interfaces.plugins import \
     IAuthenticationPlugin
from Products.PluggableAuthService.interfaces.plugins import IGroupsPlugin
from Products.PluggableAuthService.interfaces.plugins import IRolesPlugin
from Products.PlonePAS.interfaces.plugins import IUserManagement

from Products.PlonePAS.interfaces.plugins import IMutablePropertiesPlugin


class IMembraneUser(IPropertiedUser):
    """
    A marker interface for the `MembraneUser` objects generated by the
    user factory.
    """


class IMembraneUserObject(Interface):
    """
    Needs to be implemented by anything user-related so we can easily
    determine the unique user that the object is related to.

    This is the base interface that all objects that want to provide a user via
    membrane must implement or be adaptable to.
    """

    def getUserId():
        """
        Return the unique identifier for the user that this piece of
        content relates to. Historically the Archetype UID of an
        object is used as userid.
        """

    def getUserName():
        """
        Return the name used for login. This can be the same as the userid,
        but might also be something different such as the user's email address.
        """


class IMembraneUserAuth(IMembraneUserObject, IAuthenticationPlugin):
    """
    Used for objects that can handle user authentication.
    """


class IMembraneUserProperties(IMembraneUserObject, IMutablePropertiesPlugin):
    """
    Used for objects that can provide user properties.
    """


class IMembraneUserGroups(IMembraneUserObject, IGroupsPlugin):
    """
    Used for objects that can provide user groups.
    """


class IMembraneUserRoles(IMembraneUserObject, IRolesPlugin):
    """
    Used for objects that can provide user roles.
    """


class IMembraneUserManagement(IMembraneUserObject, IUserManagement):
    """
    Used to change the password and delete objects.
    """


class IMembraneUserChanger(IMembraneUserObject):
    """
    Provide a method to change a user
    """
    def doChangeUser(login, password, **kwargs):
        """change the password for a given user"""


class IMembraneUserDeleter(IMembraneUserObject):
    """
    Used to delete member objects
    """
    def doDeleteUser(login):
        """remove the user with the id login"""
