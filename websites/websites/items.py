# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WebsitesItem(scrapy.Item):
    # define the fields for your item here like:

    S_No = scrapy.Field()
    Academician_Name = scrapy.Field()
    Bio = scrapy.Field()
    Email = scrapy.Field()
    Department = scrapy.Field()
    Designation = scrapy.Field()
    Detail_Designation = scrapy.Field()
    Phone = scrapy.Field()
    Web_Page = scrapy.Field()
    Image_Url = scrapy.Field()
    CV = scrapy.Field()
