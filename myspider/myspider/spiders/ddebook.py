import scrapy
import logging

from myspider.items import DdebookItem
from myspider.utils.common import get_md5
from copy import deepcopy


class DdebookSpider(scrapy.Spider):
    name = 'ddebook'
    allowed_domains = ['e.dangdang.com/']
    start_urls = ['http://e.dangdang.com/list-DZS-dd_sale-0-1.html']

    def parse(self, response):
        item = DdebookItem()
        category_a_list = response.xpath('//*[@id="nav_left"]/div/div/a')
        for category_a in category_a_list:
            item["category_url"] = category_a.xpath('./@href').extract_first()
            item["category_title"] = category_a.xpath('./h3/text()').extract_first()
            yield scrapy.Request(
                item["category_url"],
                meta={"item": deepcopy(item)},
                callback=self.parse_list,
                dont_filter=True
        )

    def parse_list(self, resposne):
        item = resposne.meta["item"]
        second_li_list = resposne.xpath('//*[@id="nav_left"]/div/div/ul/li')
        for second_li in second_li_list:
            item["second_category_url"] = second_li.xpath('./a/@href').extract_first()
            item["second_category_title"] = second_li.xpath('./a/h4/text()').extract_first()
            yield scrapy.Request(
                item["second_category_url"],
                meta={"item": deepcopy(item)},
                callback=self.parse_book,
                dont_filter=True
            )

    def parse_book(self, response):
        item = response.meta["item"]
        book_url_list = response.xpath('//*[@id="book_list"]/a/@href').extract()
        for book_url in book_url_list:
            item["book_url"] = book_url
            yield scrapy.Request(
                url=item["book_url"],
                meta={"item": deepcopy(item)},
                callback=self.parse_detail,
                dont_filter=True
            )

    def parse_detail(self, response):
        item = response.meta["item"]
        if response.url == 'http://e.dangdang.com/error_page.html':
            item = None
            yield item, write_log()
        else:
            item["book_url_object_id"] = get_md5(response.url)
            # item["book_img"] = response.xpath('/html/body/div[5]/div[2]/div[1]/div[1]/div[2]/div[1]/img/@src'
            #                                   '| //*[@id="content"]/div[1]/div[1]/img/@src').extract_first()
            item["book_name"] = response.xpath('//*[@id="productBookDetail"]/h1/span[1]/text()'
                                               '| //*[@id="content"]/div[1]/div[2]/div[1]/text()').extract_first().strip()
            yield item


def write_log():
    logger = logging.getLogger(__name__)
    logger.warning("请求出现错误！！！")
