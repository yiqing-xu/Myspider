# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join

import re
from w3lib.html import remove_tags


def handle_date(value):
    # try:
    #     date = datetime.datetime.strptime(value.strip().replace("·", ""), '%Y/%m/%d').date()
    # except Exception as e:
    #     date = datetime.datetime.now().date()
    # return date
    date = value.strip().replace("·", "")
    return date


def handle_collection(value):
    collection = re.match(r".*?(\d+).*", value)
    if collection:
        collection_num = collection.group(1)
    else:
        collection_num = 0
    return collection_num


def handle_tags(value):
    if "评论" in value:
        return ""
    else:
        return value


def handle_content(value):
    remove_tags(value)


def return_value(value):
    return value


class MyItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


class DdebookItem(scrapy.Item):
    category_url = scrapy.Field()
    category_title = scrapy.Field()
    second_category_url = scrapy.Field()
    second_category_title = scrapy.Field()
    book_url = scrapy.Field()
    book_url_object_id = scrapy.Field()
    # book_img = scrapy.Field()
    book_name = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
            insert into ddebook_spider(category_url, category_title, second_category_url,
             second_category_title, book_url, book_url_object_id, book_name)
            values (%s, %s, %s, %s, %s, %s, %s)

        """
        params = (self["category_url"], self["category_title"], self["second_category_url"],
                  self["second_category_title"], self["book_url"], self["book_url_object_id"], self["book_name"])
        return insert_sql, params


class JobboleItem(scrapy.Item):
    front_img_url = scrapy.Field(
        output_processor=MapCompose(return_value)
    )
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    title = scrapy.Field()
    praise_num = scrapy.Field()
    collection_num = scrapy.Field(
        input_processor=MapCompose(handle_collection)
    )
    date = scrapy.Field(
        input_processor=MapCompose(handle_date)
    )
    tags = scrapy.Field(
        input_processor=MapCompose(handle_tags),
        output_processor=Join(",")
    )
    content = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
            insert into jobbole_spider(title, date, url, url_object_id, front_img_url, praise_num,
             collection_num, tags, content)
            values (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE url_object_id=values(url_object_id)
        """
        params = (self["title"], self["date"],  self["url"], self["url_object_id"],
                  self["front_img_url"], self["praise_num"], self["collection_num"], self["tags"], self["content"])
        return insert_sql, params


class CsdnArticleItem(scrapy.Item):
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    title = scrapy.Field()
    date = scrapy.Field()
    pageview = scrapy.Field()
    author = scrapy.Field()
    content = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
            insert into csdn_article(url, url_object_id, title, date, pageview, author, content)
            values (%s, %s, %s, %s, %s, %s, %s)
        """
        params = (self["url"], self["url_object_id"], self["title"], self["date"], self["pageview"], self["author"], self["content"])

        return insert_sql, params


class CsdnJobItem(scrapy.Item):
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    title = scrapy.Field()
    min_salary = scrapy.Field()
    max_salary = scrapy.Field()
    city = scrapy.Field()
    job_cate = scrapy.Field()
    edu = scrapy.Field()
    exp = scrapy.Field()
    tags = scrapy.Field()
    date = scrapy.Field()
    des = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
            insert into csdn_job(url, url_object_id, title, min_salary, max_salary, city, job_cate, edu, exp, tags, date, des) 
            values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        params = (self["url"], self["url_object_id"], self["title"], self["min_salary"], self["max_salary"], self["city"], self["job_cate"], self["edu"],
                  self["exp"], self["tags"], self["date"], self["des"])

        return insert_sql, params
