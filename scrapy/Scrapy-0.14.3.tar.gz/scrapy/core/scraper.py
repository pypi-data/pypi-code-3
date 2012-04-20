"""This module implements the Scraper component which parses responses and
extracts information from them"""

from collections import deque

from twisted.python.failure import Failure
from twisted.internet import defer

from scrapy.utils.defer import defer_result, defer_succeed, parallel, iter_errback
from scrapy.utils.spider import iterate_spider_output
from scrapy.utils.misc import load_object
from scrapy.utils.signal import send_catch_log, send_catch_log_deferred
from scrapy.exceptions import CloseSpider, DropItem
from scrapy import signals
from scrapy.http import Request, Response
from scrapy.item import BaseItem
from scrapy.core.spidermw import SpiderMiddlewareManager
from scrapy import log
from scrapy.stats import stats


class Slot(object):
    """Scraper slot (one per running spider)"""

    MIN_RESPONSE_SIZE = 1024

    def __init__(self, max_active_size=5000000):
        self.max_active_size = max_active_size
        self.queue = deque()
        self.active = set()
        self.active_size = 0
        self.itemproc_size = 0
        self.closing = None

    def add_response_request(self, response, request):
        deferred = defer.Deferred()
        self.queue.append((response, request, deferred))
        if isinstance(response, Response):
            self.active_size += max(len(response.body), self.MIN_RESPONSE_SIZE)
        else:
            self.active_size += self.MIN_RESPONSE_SIZE
        return deferred

    def next_response_request_deferred(self):
        response, request, deferred = self.queue.popleft()
        self.active.add(request)
        return response, request, deferred

    def finish_response(self, response, request):
        self.active.remove(request)
        if isinstance(response, Response):
            self.active_size -= max(len(response.body), self.MIN_RESPONSE_SIZE)
        else:
            self.active_size -= self.MIN_RESPONSE_SIZE

    def is_idle(self):
        return not (self.queue or self.active)

    def needs_backout(self):
        return self.active_size > self.max_active_size

class Scraper(object):

    def __init__(self, crawler):
        self.slots = {}
        self.spidermw = SpiderMiddlewareManager.from_crawler(crawler)
        itemproc_cls = load_object(crawler.settings['ITEM_PROCESSOR'])
        self.itemproc = itemproc_cls.from_crawler(crawler)
        self.concurrent_items = crawler.settings.getint('CONCURRENT_ITEMS')
        self.crawler = crawler

    @defer.inlineCallbacks
    def open_spider(self, spider):
        """Open the given spider for scraping and allocate resources for it"""
        assert spider not in self.slots, "Spider already opened: %s" % spider
        self.slots[spider] = Slot()
        yield self.itemproc.open_spider(spider)

    def close_spider(self, spider):
        """Close a spider being scraped and release its resources"""
        assert spider in self.slots, "Spider not opened: %s" % spider
        slot = self.slots[spider]
        slot.closing = defer.Deferred()
        slot.closing.addCallback(self.itemproc.close_spider)
        self._check_if_closing(spider, slot)
        return slot.closing

    def is_idle(self):
        """Return True if there isn't any more spiders to process"""
        return not self.slots

    def _check_if_closing(self, spider, slot):
        if slot.closing and slot.is_idle():
            del self.slots[spider]
            slot.closing.callback(spider)

    def enqueue_scrape(self, response, request, spider):
        slot = self.slots[spider]
        dfd = slot.add_response_request(response, request)
        def finish_scraping(_):
            slot.finish_response(response, request)
            self._check_if_closing(spider, slot)
            self._scrape_next(spider, slot)
            return _
        dfd.addBoth(finish_scraping)
        dfd.addErrback(log.err, 'Scraper bug processing %s' % request, \
            spider=spider)
        self._scrape_next(spider, slot)
        return dfd

    def _scrape_next(self, spider, slot):
        while slot.queue:
            response, request, deferred = slot.next_response_request_deferred()
            self._scrape(response, request, spider).chainDeferred(deferred)

    def _scrape(self, response, request, spider):
        """Handle the downloaded response or failure trough the spider
        callback/errback"""
        assert isinstance(response, (Response, Failure))

        dfd = self._scrape2(response, request, spider) # returns spiders processed output
        dfd.addErrback(self.handle_spider_error, request, response, spider)
        dfd.addCallback(self.handle_spider_output, request, response, spider)
        return dfd

    def _scrape2(self, request_result, request, spider):
        """Handle the diferent cases of request's result been a Response or a
        Failure"""
        if not isinstance(request_result, Failure):
            return self.spidermw.scrape_response(self.call_spider, \
                request_result, request, spider)
        else:
            # FIXME: don't ignore errors in spider middleware
            dfd = self.call_spider(request_result, request, spider)
            return dfd.addErrback(self._log_download_errors, \
                request_result, request, spider)

    def call_spider(self, result, request, spider):
        dfd = defer_result(result)
        dfd.addCallbacks(request.callback or spider.parse, request.errback)
        return dfd.addCallback(iterate_spider_output)

    def handle_spider_error(self, _failure, request, response, spider):
        exc = _failure.value
        if isinstance(exc, CloseSpider):
            self.crawler.engine.close_spider(spider, exc.reason or 'cancelled')
            return
        log.err(_failure, "Spider error processing %s" % request, spider=spider)
        send_catch_log(signal=signals.spider_error, failure=_failure, response=response, \
            spider=spider)
        stats.inc_value("spider_exceptions/%s" % _failure.value.__class__.__name__, \
            spider=spider)

    def handle_spider_output(self, result, request, response, spider):
        if not result:
            return defer_succeed(None)
        it = iter_errback(result, self.handle_spider_error, request, response, spider)
        dfd = parallel(it, self.concurrent_items,
            self._process_spidermw_output, request, response, spider)
        return dfd

    def _process_spidermw_output(self, output, request, response, spider):
        """Process each Request/Item (given in the output parameter) returned
        from the given spider
        """
        if isinstance(output, Request):
            send_catch_log(signal=signals.request_received, request=output, \
                spider=spider)
            self.crawler.engine.crawl(request=output, spider=spider)
        elif isinstance(output, BaseItem):
            self.slots[spider].itemproc_size += 1
            dfd = self.itemproc.process_item(output, spider)
            dfd.addBoth(self._itemproc_finished, output, response, spider)
            return dfd
        elif output is None:
            pass
        else:
            log.msg("Spider must return Request, BaseItem or None, got %r in %s" % \
                (type(output).__name__, request), log.ERROR, spider=spider)

    def _log_download_errors(self, spider_failure, download_failure, request, spider):
        """Log and silence errors that come from the engine (typically download
        errors that got propagated thru here)
        """
        if spider_failure is download_failure:
            log.msg("Error downloading %s: %s" % \
                (request, spider_failure.getErrorMessage()), log.ERROR, spider=spider)
            return
        return spider_failure

    def _itemproc_finished(self, output, item, response, spider):
        """ItemProcessor finished for the given ``item`` and returned ``output``
        """
        self.slots[spider].itemproc_size -= 1
        if isinstance(output, Failure):
            ex = output.value
            if isinstance(ex, DropItem):
                log.msg(log.formatter.dropped(item, ex, response, spider), \
                    level=log.WARNING, spider=spider)
                return send_catch_log_deferred(signal=signals.item_dropped, \
                    item=item, spider=spider, exception=output.value)
            else:
                log.err(output, 'Error processing %s' % item, spider=spider)
        else:
            log.msg(log.formatter.scraped(output, response, spider), \
                log.DEBUG, spider=spider)
            return send_catch_log_deferred(signal=signals.item_scraped, \
                item=output, response=response, spider=spider)

