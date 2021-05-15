import scrapy
from ..items import QuoteItem

class QuoteSpider(scrapy.Spider):
    name = 'quotes'
    page_num = 2
    start_urls = [
    'https://quotes.toscrape.com/',
    ]

    def parse(self, response):
        items = QuoteItem()

        all_quotes = response.css('div.quote')

        for quote in all_quotes:
            title = quote.css('.text::text').extract()
            author = quote.css('.author::text').extract()
            tags = quote.css('.tag::text').extract()

            items['title'] = title
            items['author'] = author
            items['tags'] = tags

            yield items

        next_page = 'https://quotes.toscrape.com/page/'+ str(QuoteSpider.page_num)

        if QuoteSpider.page_num < 11:
            QuoteSpider.page_num += 1
            yield response.follow(next_page, callback=self.parse)
