# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class chapterItem(scrapy.Item):
    table_name = scrapy.Field()
    id = scrapy.Field()
    # define the fields for your item here like:
    course_id = scrapy.Field()
    # cate = scrapy.Field()
    title = scrapy.Field()
    created_at = scrapy.Field()
    # desc = scrapy.Field()
    # cate = scrapy.Field()
    pass

