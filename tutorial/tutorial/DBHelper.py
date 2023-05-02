# -*- coding: utf-8 -*-

import pymysql
from twisted.enterprise import adbapi
from scrapy.utils.project import get_project_settings  # 导入seetings配置
import time


class DBHelper():
    '''这个类也是读取settings中的配置，自行修改代码进行操作'''

    def __init__(self):
        settings = get_project_settings()  # 获取settings配置，设置需要的信息
        self.db = pymysql.connect(
            host=settings['MYSQL_HOST'], port=settings['MYSQL_PORT'],
            user=settings['MYSQL_USER'], password=settings['MYSQL_PASSWD'],
            database=settings['MYSQL_DBNAME'], charset='utf8mb4'
        )
        self.cursor = self.db.cursor()


    def connect(self):
        return self.dbpool

    # 创建数据库
    def insert(self, item):
        table_name = item['table_name']
        keys = list(item.keys())  # ['pcid', 'pid', 'cid', 'roles']
        values = list(item.values())  # ['333', '222', '111', '制作方']

        # 所有字段组成的字符串
        key_str = ','.join(['`%s`' % k for k in keys])
        # print(key_str)  # "`pcid`,`pid`,`cid`,`roles`"
        values_str = ','.join(["%s"] * len(values))
        update_str = ','.join(["`{}`=%s".format(k) for k in keys])
        sql = 'insert into `{}`({}) values({}) on duplicate key update {}'.format(
            table_name,
            key_str,
            values_str,
            update_str
        )
        # # 执行SQL
        self.cursor.execute(sql, values * 2)
        # # values * 2 =
        # # ['333', '222', '111', '制作方', '333', '222', '111', '制作方']
        self.db.commit()
        # print(f'----- 插入成功: {table_name} -----')


        return item
