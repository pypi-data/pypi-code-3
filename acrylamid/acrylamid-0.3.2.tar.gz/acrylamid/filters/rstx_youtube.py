# License: BSD Style, 2 clauses. see acrylamid/__init__.py
# -*- encoding: utf-8 -*-

from docutils import nodes
from docutils.parsers.rst import Directive, directives

match = ['youtube', 'yt']


def align(argument):
    return directives.choice(argument, ('left', 'center', 'right'))


class YouTube(Directive):
    """reStructuredText directive that creates an embed object to display
    a video from Youtube

    Usage example::

        .. youtube:: ZPJlyRv_IGI
           :align: center
           :height: 1280
           :width: 720
    """

    required_arguments = 1
    optional_arguments = 0
    option_spec = {
        'height': directives.length_or_unitless,
        'width': directives.length_or_percentage_or_unitless,
        'border': directives.length_or_unitless,
        'align': align,
    }
    has_content = False

    def run(self):

        alignments = {
            'left': '0',
            'center': '0 auto',
            'right': '0 0 0 auto',
        }

        self.options['uri'] = 'https://www.youtube-nocookie.com/embed/' \
            + self.arguments[0]
        self.options.setdefault('width', '680')
        self.options.setdefault('height', '382px')
        self.options['align'] = alignments[self.options.get('align', 'center')]
        self.options.setdefault('border', '0')

        YT_EMBED = """<iframe width="%(width)s" height="%(height)s" src="%(uri)s" \
                      frameborder="%(border)s" style="display: block; margin: %(align)s;" \
                      class="video" allowfullscreen></iframe>"""
        return [nodes.raw('', YT_EMBED % self.options, format='html')]

def makeExtension():
    return YouTube
