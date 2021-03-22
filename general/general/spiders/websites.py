import scrapy


class WebsitesSpider(scrapy.Spider):
    name = 'websites'
    allowed_domains = ['website.com']
    start_urls = ['http://website.com/']

    def parse(self, response):
        pass
