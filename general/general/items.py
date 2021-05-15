# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
# import json
# from collections import OrderedDict
#
# class OrderedItem(scrapy.Item):
#     def __init__(self, *args, **kwargs):
#         self._values = OrderedDict()
#         if args or kwargs:
#             for k, v in six.iteritems(dict(*args, **kwargs)):
#                 self[k] = v
#
#     def __repr__(self):
#         return json.dumps(OrderedDict(self),ensure_ascii = False)
#         #ensure_ascii = False ,it make characters show in cjk appearance.


class GeneralItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    Name = scrapy.Field()
    designation = scrapy.Field()
    designation_detail = scrapy.Field()
    major_area = scrapy.Field()
    contact = scrapy.Field()
    email = scrapy.Field()
    education = scrapy.Field()
    University = scrapy.Field()
    address = scrapy.Field()
    image = scrapy.Field()
    Phone_No = scrapy.Field()
    # name = scrapy.Field()


'''
Name
University Name
Email
address
Designation
Designation Details
Department Name
Major Area
DOB
Mobile No.
Image Url
Type --> PHD student
'''
