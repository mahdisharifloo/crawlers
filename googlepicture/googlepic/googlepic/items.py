# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GooglepicItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    host= scrapy.Field()
    s=scrapy.Field()
    src_link = scrapy.Field()
    pass

