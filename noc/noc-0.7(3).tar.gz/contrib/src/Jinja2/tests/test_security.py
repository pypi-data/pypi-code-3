# -*- coding: utf-8 -*-
"""
    unit test for security features
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2009 by the Jinja Team.
    :license: BSD, see LICENSE for more details.
"""
from jinja2 import Environment
from jinja2.sandbox import SandboxedEnvironment, \
     ImmutableSandboxedEnvironment, unsafe
from jinja2 import Markup, escape
from jinja2.exceptions import SecurityError, TemplateSyntaxError


from nose.tools import assert_raises

class PrivateStuff(object):

    def bar(self):
        return 23

    @unsafe
    def foo(self):
        return 42

    def __repr__(self):
        return 'PrivateStuff'


class PublicStuff(object):
    bar = lambda self: 23
    _foo = lambda self: 42

    def __repr__(self):
        return 'PublicStuff'


def test_unsafe():
    '''
>>> env = SandboxedEnvironment()
>>> env.from_string("{{ foo.foo() }}").render(foo=PrivateStuff())
Traceback (most recent call last):
    ...
SecurityError: <bound method PrivateStuff.foo of PrivateStuff> is not safely callable
>>> env.from_string("{{ foo.bar() }}").render(foo=PrivateStuff())
u'23'

>>> env.from_string("{{ foo._foo() }}").render(foo=PublicStuff())
Traceback (most recent call last):
    ...
SecurityError: access to attribute '_foo' of 'PublicStuff' object is unsafe.
>>> env.from_string("{{ foo.bar() }}").render(foo=PublicStuff())
u'23'

>>> env.from_string("{{ foo.__class__ }}").render(foo=42)
u''
>>> env.from_string("{{ foo.func_code }}").render(foo=lambda:None)
u''
>>> env.from_string("{{ foo.__class__.__subclasses__() }}").render(foo=42)
Traceback (most recent call last):
    ...
SecurityError: access to attribute '__class__' of 'int' object is unsafe.
'''


def test_restricted():
    env = SandboxedEnvironment()
    assert_raises(TemplateSyntaxError, env.from_string,
                  "{% for item.attribute in seq %}...{% endfor %}")
    assert_raises(TemplateSyntaxError, env.from_string,
                  "{% for foo, bar.baz in seq %}...{% endfor %}")


def test_immutable_environment():
    '''
>>> env = ImmutableSandboxedEnvironment()
>>> env.from_string('{{ [].append(23) }}').render()
Traceback (most recent call last):
    ...
SecurityError: access to attribute 'append' of 'list' object is unsafe.
>>> env.from_string('{{ {1:2}.clear() }}').render()
Traceback (most recent call last):
    ...
SecurityError: access to attribute 'clear' of 'dict' object is unsafe.
'''


def test_markup_operations():
    # adding two strings should escape the unsafe one
    unsafe = '<script type="application/x-some-script">alert("foo");</script>'
    safe = Markup('<em>username</em>')
    assert unsafe + safe == unicode(escape(unsafe)) + unicode(safe)

    # string interpolations are safe to use too
    assert Markup('<em>%s</em>') % '<bad user>' == \
           '<em>&lt;bad user&gt;</em>'
    assert Markup('<em>%(username)s</em>') % {
        'username': '<bad user>'
    } == '<em>&lt;bad user&gt;</em>'

    # an escaped object is markup too
    assert type(Markup('foo') + 'bar') is Markup

    # and it implements __html__ by returning itself
    x = Markup("foo")
    assert x.__html__() is x

    # it also knows how to treat __html__ objects
    class Foo(object):
        def __html__(self):
            return '<em>awesome</em>'
        def __unicode__(self):
            return 'awesome'
    assert Markup(Foo()) == '<em>awesome</em>'
    assert Markup('<strong>%s</strong>') % Foo() == \
           '<strong><em>awesome</em></strong>'

    # escaping and unescaping
    assert escape('"<>&\'') == '&#34;&lt;&gt;&amp;&#39;'
    assert Markup("<em>Foo &amp; Bar</em>").striptags() == "Foo & Bar"
    assert Markup("&lt;test&gt;").unescape() == "<test>"


def test_template_data():
    env = Environment(autoescape=True)
    t = env.from_string('{% macro say_hello(name) %}'
                        '<p>Hello {{ name }}!</p>{% endmacro %}'
                        '{{ say_hello("<blink>foo</blink>") }}')
    escaped_out = '<p>Hello &lt;blink&gt;foo&lt;/blink&gt;!</p>'
    assert t.render() == escaped_out
    assert unicode(t.module) == escaped_out
    assert escape(t.module) == escaped_out
    assert t.module.say_hello('<blink>foo</blink>') == escaped_out
    assert escape(t.module.say_hello('<blink>foo</blink>')) == escaped_out


def test_attr_filter():
    env = SandboxedEnvironment()
    tmpl = env.from_string('{{ 42|attr("__class__")|attr("__subclasses__")() }}')
    assert_raises(SecurityError, tmpl.render)
