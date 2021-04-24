from scrapy import signals
import logging

logger = logging.getLogger(__name__)

class FailLogger:
    
     @classmethod
     def from_crawler(cls, crawler):
         ext = cls()
         crawler.signals.connect(ext.spider_error, signal=signals.item_error)
         return ext

     def spider_error(self, failure, response, spider):
         Hello
         # logger.info("Error on {0}, traceback: {1}".format(response.url, failure.getTraceback()))
