# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ImoocCourseItem(scrapy.Item):
    # define the fields for your item here like:
    # table_name = 'tech_courses'
    id = scrapy.Field()
    table_name = scrapy.Field()
    title = scrapy.Field()
    # cate = scrapy.Field()
    image = scrapy.Field()
    # desc = scrapy.Field()
    course_direction = scrapy.Field()
    course_type = scrapy.Field()
    # cate = scrapy.Field()
    course_url = scrapy.Field()
    created_at = scrapy.Field()
    pass

