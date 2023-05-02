# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class VideoItem(scrapy.Item):
    table_name = scrapy.Field()
    # define the fields for your item here like:
    id = scrapy.Field()
    course_id = scrapy.Field()
    chapter_id = scrapy.Field()
    title = scrapy.Field()
    video_source_id = scrapy.Field()
    video_original_name = scrapy.Field()
    play_count = scrapy.Field()
    duration = scrapy.Field()
    created_at = scrapy.Field()
    pass

