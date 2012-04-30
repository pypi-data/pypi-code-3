from Products.CMFCore.utils import getToolByName
from ftw.pdfgenerator.html2latex import subconverter
import os.path


class HyperlinkConverter(subconverter.SubConverter):

    pattern = r'<a.*?href="(.*?)".*?>(.*?)</a>'

    def __call__(self):
        context = self.get_context()

        url, label = self.match.groups()
        label = self.converter.convert(label)

        is_relative = '://' not in url and not url.startswith('mailto:')

        if is_relative:
            url = os.path.join(context.absolute_url(), url)

        url = self.resolve_uid(url)

        url = url.replace('&amp;', '&')
        url = url.replace(' ', '%20').replace('%', '\%')

        self.get_layout().use_package('hyperref')
        self.replace_and_lock(self.latex_link(url, label))

    def latex_link(self, url, label):
        href = r'\href{%s}{%s}'
        footnote = r'\footnote{%s}' % href % (url, url)
        return href % (url, label + footnote)

    def resolve_uid(self, url):
        if '/' not in url:
            return url

        parts = url.split('/')
        if parts[-2] == 'resolveuid':
            context = self.converter.converter.context
            reference_catalog = getToolByName(context, 'reference_catalog')

            uid = parts[-1]
            obj = reference_catalog.lookupObject(uid)

            if obj is not None:
                url = obj.absolute_url()

        return url
