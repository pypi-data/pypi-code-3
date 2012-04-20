import unittest

from scrapy.spider import BaseSpider
from scrapy.http import Request, Response
from scrapy.item import Item, Field
from scrapy.logformatter import LogFormatter


class CustomItem(Item):

    name = Field()

    def __str__(self):
        return "name: %s" % self['name']


class LoggingContribTest(unittest.TestCase):

    def setUp(self):
        self.formatter = LogFormatter()
        self.spider = BaseSpider('default')

    def test_crawled(self):
        req = Request("http://www.example.com")
        res = Response("http://www.example.com")
        self.assertEqual(self.formatter.crawled(req, res, self.spider),
            "Crawled (200) <GET http://www.example.com> (referer: None)")

        req = Request("http://www.example.com", headers={'referer': 'http://example.com'})
        res = Response("http://www.example.com", flags=['cached'])
        self.assertEqual(self.formatter.crawled(req, res, self.spider),
            "Crawled (200) <GET http://www.example.com> (referer: http://example.com) ['cached']")

    def test_dropped(self):
        item = {}
        exception = Exception(u"\u2018")
        response = Response("http://www.example.com")
        lines = self.formatter.dropped(item, exception, response, self.spider).splitlines()
        assert all(isinstance(x, unicode) for x in lines)
        self.assertEqual(lines, [u"Dropped: \u2018", '{}'])

    def test_scraped(self):
        item = CustomItem()
        item['name'] = u'\xa3'
        response = Response("http://www.example.com")
        lines = self.formatter.scraped(item, response, self.spider).splitlines()
        assert all(isinstance(x, unicode) for x in lines)
        self.assertEqual(lines, [u"Scraped from <200 http://www.example.com>", u'name: \xa3'])

if __name__ == "__main__":
    unittest.main()
