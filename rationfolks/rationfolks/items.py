# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RationfolksItem(scrapy.Item):
    # define the fields for your item here like:
    sno = scrapy.Field()
    title = scrapy.Field()
    weight = scrapy.Field()
    price = scrapy.Field()
    mrp = scrapy.Field()
    image = scrapy.Field()
    additional_info = scrapy.Field()
