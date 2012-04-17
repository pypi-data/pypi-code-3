from abjad.tools.abctools.AbjadObject import AbjadObject


class ImmutableDictionary(dict, AbjadObject):
    '''.. versionadded:: 2.0
    
    Immutable dictionary::

        abjad> from abjad.tools import datastructuretools

    ::

        abjad> dictionary = datastructuretools.ImmutableDictionary({'color': 'red', 'number': 9})

    ::

        abjad> dictionary
        {'color': 'red', 'number': 9}

    ::

        abjad> dictionary['color']
        'red'

    ::

        abjad> dictionary.size = 'large' # doctest: +SKIP
        AttributeError: ImmutableDictionary objects are immutable.

    ::

        abjad> dictionary['size'] = 'large' # doctest: +SKIP
        AttributeError: ImmutableDictionary objects are immutable.

    Return immutable dictionary.
    '''

    __slots__ = ()

    ### SPECIAL METHODS ###

    def __delitem__(self, *args):
        raise AttributeError('{} objects are immutable.'.format(self._class_name))

    def __setitem__(self, *args):
        raise AttributeError('{} objects are immutable.'.format(self._class_name))
