# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class descItem(scrapy.Item):
    table_name = scrapy.Field()
    # table = 'desc'
    # table_name = scrapy.Field()
    # define the fields for your item here like:
    id = scrapy.Field()
    description = scrapy.Field()
    created_at = scrapy.Field()
    pass

