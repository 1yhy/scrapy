# -*- coding: utf-8 -*-
import re

import scrapy
import uuid
from urllib import parse as urlparse
from tutorial import ImoocCourseItem
from tutorial.chapterItem import chapterItem
from tutorial.desc import descItem
from tutorial.VideoItem import VideoItem


# 慕课网爬取
class ImoocSpider(scrapy.Spider):
    # spider的名字定义了Scrapy如何定位(并初始化)spider，所以其必须是唯一的
    name = "imooc"

    # URL列表
    start_urls = ['https://www.imooc.com/course/list']
    #  域名不在列表中的URL不会被爬取。
    allowed_domains = ['www.imooc.com']

    def parse(self, response):
        # 课程类型
        directions = response.css('div.direction.js-direction ul li')
        for key in range(len(directions)):
            if key == 0:
                continue
            course_direction = directions[key].css('a::text').extract_first()
            # 类型的url
            direction_url = directions[key].css('a::attr(href)').extract_first()
            item = ImoocCourseItem()
            item['table_name'] = 'tech_courses'
            item['course_direction'] = course_direction
            # print (item)
            yield scrapy.Request(
                url=urlparse.urljoin(response.url, direction_url),
                callback=self.parse_by_direction,
                meta=item)

    def parse_by_direction(self, response):
        item = response.meta

        # 课程类型
        types = response.css('div.sort.js-sort ul li')
        for key in range(len(types)):
            if key == 0:
                continue
            course_type = types[key].css('a::text').extract_first()
            # 类型的url
            type_url = types[key].css('::attr(href)').extract_first()
            item['course_type'] = course_type
            # print (item)
            yield scrapy.Request(
                url=urlparse.urljoin(response.url, type_url),
                callback=self.parse_by_type,
                meta=item)


    # 按课程类型爬取
    def parse_by_type(self, response):
        item = response.meta
        # print(item)
        learn_nodes = response.css('a.item.free')
        # 遍历该页上所有课程列表
        for learn_node in learn_nodes:
            item['id'] = learn_node.css("::attr(data-cid)").extract_first()
            course_url = learn_node.css("::attr(href)").extract_first()
            # 拼接课程详情页地址
            course_url = urlparse.urljoin(response.url, course_url)
            # 课程地址
            item['course_url'] = course_url
            # # 课程图片
            # # regBackgroundUrl = / url\("?'?.*"?'?\)/g;
            # # regReplace = / "|'|url|\(|\)/g;
            img = learn_node.css("div.img::attr(style)").extract_first()
            url = self.Find(img)
            item['image'] = 'https:' + url[0]
            # 进入课程详情页面
            yield scrapy.Request(
                url=course_url, callback=self.parse_learn, meta=item)

        # 下一页地址
        next_page_url = response.css(
            u'div.page a:contains("下一页")::attr(href)').extract_first()
        if next_page_url:
            yield scrapy.Request(
                url=urlparse.urljoin(response.url, next_page_url),
                callback=self.parse_by_type,
                meta=item)

    # def parse(self, response):
    #     learn_nodes = response.css('a.item.free')
    #
    #     item = ImoocCourseItem()
    #     # 遍历该页上所有课程列表
    #     for learn_node in learn_nodes:
    #         course_url = learn_node.css("::attr(href)").extract_first()
    #         # 拼接课程详情页地址
    #         course_url = urlparse.urljoin(response.url, course_url)
    #         # 课程地址
    #         item['course_url'] = course_url
    #         # # 课程图片
    #         # # regBackgroundUrl = / url\("?'?.*"?'?\)/g;
    #         # # regReplace = / "|'|url|\(|\)/g;
    #         img = learn_node.css("div.img::attr(style)").extract_first()
    #         item['image'] = self.Find(img)
    #         # 进入课程详情页面
    #         yield scrapy.Request(
    #             url=course_url, callback=self.parse_learn, meta=item)
    #
    #     # 下一页地址
    #     next_page_url = response.css(
    #         u'div.page a:contains("下一页")::attr(href)').extract_first()
    #     if next_page_url:
    #         yield scrapy.Request(
    #             url=urlparse.urljoin(response.url, next_page_url),
    #             callback=self.parse)

    def parse_learn(self, response):
        item = response.meta
        # 课程标题
        item['title'] = response.xpath(
            '//h2[@class="l"]/text()').extract_first()
        yield item

        desc = descItem()
        # 课程简介
        desc['table_name'] = 'desc'
        desc['id'] = item['id']
        desc['description'] = response.xpath(
            '//div[@class="course-description course-wrap"]/text()').extract_first()
        yield desc

        chapter = chapterItem()
        chapter['table_name'] = 'chapter'
        chapter_nodes = response.css('div.course-chapters div.chapter')
        for chapter_node in chapter_nodes:
            chapter['id'] = ''.join(str(uuid.uuid1()).split('-'))
            chapter['course_id'] = item['id']
            chapter['title'] = chapter_node.css("h3::text").extract_first()
            yield chapter

            video = VideoItem()
            video['table_name'] = 'video'
            video_nodes = chapter_node.css('ul.video li')
            for video_node in video_nodes:
                video['id'] = video_node.css("::attr(data-media-id)").extract_first()
                video['course_id'] = item['id']
                video['chapter_id'] = chapter['id']
                content = video_node.css('a.J-media-item::text').extract()[2]
                video['title'] = self.getTitle(content)
                url = video_node.css("a::attr(href)").extract_first()
                video['video_source_id'] = urlparse.urljoin(response.url, url)
                video['video_original_name'] = self.getTitle(content)
                video['play_count'] = 0
                video['duration'] = self.getDuration(content)[0]
                yield video



    def Find(self,string):
        # findall() 查找匹配正则表达式的字符串
        p1 = re.compile('[(]\'(.*?)\'[)]', re.S)
        url = re.findall(p1, string)
        # url = re.findall('//(?:[-\w.]|(?:%[\da-fA-F]{2}))+', string)
        return url

    def getTitle(self, string):
        # findall() 查找匹配正则表达式的字符串
        title = re.sub("\\(.*?\\)", "", string)
        return title

    def getDuration(self, string):
        # findall() 查找匹配正则表达式的字符串
        p1 = re.compile('[(](.*?)[)]', re.S)
        duration = re.findall(p1, string)
        return duration