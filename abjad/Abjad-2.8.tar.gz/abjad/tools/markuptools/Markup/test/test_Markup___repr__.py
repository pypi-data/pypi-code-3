from abjad import *


def test_Markup___repr___01():

    markup = markuptools.Markup('foo bar')
    assert repr(markup) == "Markup('foo bar')"


def test_Markup___repr___02():

    markup = markuptools.Markup('foo bar', direction='up')
    assert repr(markup) == "Markup('foo bar', direction='^')"


def test_Markup___repr___03():

    markup = markuptools.Markup('foo bar', direction='up', markup_name='foo')
    assert repr(markup) == "Markup('foo bar', direction='^', markup_name='foo')"


def test_Markup___repr___04():

    markup = markuptools.Markup('foo bar', direction='up', markup_name='foo', style_string='scheme')
    assert repr(markup) == "Markup('foo bar', direction='^', markup_name='foo', style_string='scheme')"
