# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter
import codecs
import json
import pymysql
import pymysql.cursors
from twisted.enterprise import adbapi


class MyspiderPipeline(object):
    def process_item(self, item, spider):
        return item


class MysqlPipeline(object):
    """
    同步存储数据到Mysql中，效率低
    """
    def __init__(self):
        self.conn = pymysql.connect("localhost", "root", "122317#*xyq", "scrapy", charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql, params = item.get_insert_sql()
        self.cursor.execute(insert_sql, params)
        self.conn.commit()


class MysqlTwistedPipeline(object):
    """
    异步存储数据到Mysql
    """
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host=settings["MYSQL_HOST"],
            user=settings["MYSQL_USER"],
            password=settings["MYSQL_PASSWORD"],
            db=settings["MYSQL_DBNAME"],
            charset="utf8",
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True
        )
        dbpool = adbapi.ConnectionPool("pymysql", **dbparms)
        return cls(dbpool)

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider)

    def handle_error(self, failure, item, spider):
        print(failure)

    def do_insert(self, cursor, item):
        insert_sql, params = item.get_insert_sql()
        cursor.execute(insert_sql, params)


class JsonWithEncodingPipeline(object):
    """

    """

    def __init__(self):
        self.file = codecs.open("aticle.json", "w", encoding="utf-8")

    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False)
        self.file.write(lines)
        return item

    def spider_close(self, spider):
        self.file.close()


class JsonExporterPipeline(object):
    """
    调用scrapy提供的json export导出json文件
    """

    def __init__(self):
        self.file = open("aticleexporter.json", "wb")
        self.exporter = JsonItemExporter(self.file, encoding="utf-8", ensure_ascii=False)
        self.exporter.start_exporting()

    def clsoe_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


class MyImagesPipeline(ImagesPipeline):
    """
    重写ImagesPipeline方法，使保存的图片名称和路径自定义
    """
    def get_media_requests(self, item, info):
        for img_url in item["img_urls"]:
            yield scrapy.Request(img_url, meta={"item": item})

    def file_path(self, request, response=None, info=None):
        item = request.meta.get("item", "")
        img_title = item["img_name"]
        return 'full/%s.jpg' % img_title
