# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from w3lib.html import remove_tags
from myspider.items import CsdnArticleItem, CsdnJobItem
from myspider.utils.common import get_md5


class CsdnSpider(CrawlSpider):
    name = 'csdn'
    allowed_domains = ['csdn.net']
    start_urls = ['https://www.csdn.net/nav/lang', 'https://job.csdn.net/']

    rules = (
        Rule(LinkExtractor(allow=r'https://blog.csdn.net/\w+/article/details/\d+'), callback='parse_article', follow=True),
        Rule(LinkExtractor(allow=r'https://job.csdn.net/p/\d+'), callback='parse_job', follow=True),
    )

    def parse_article(self, response):
        item = CsdnArticleItem()

        item["url"] = response.url
        item["url_object_id"] = get_md5(response.url)
        item["title"] = response.css(".title-article::text").extract_first()
        item["date"] = response.css(".time::text").extract_first()
        item["pageview"] = response.css(".read-count::text").extract_first().split("：")[-1]
        item["author"] = response.css("#uid::text").extract_first()
        item["content"] = remove_tags(response.css("#content_views").extract_first())

        return item

    def parse_job(self, response):
        item = CsdnJobItem()

        item["url"] = response.url
        item["url_object_id"] = get_md5(response.url)
        item["title"] = response.css(".myj-details-top .highlight::text").extract_first()
        info = response.xpath("//ul[@class='left-top']/li/text()").extract()
        salary = info[0]
        min_salaary = salary.split("~")[0]
        max_salary = salary.split("~")[-1].split("/")[0]
        item["min_salary"] = min_salaary.split("K")[0]
        item["max_salary"] = max_salary.split("K")[0]
        item["city"] = info[2]
        item["job_cate"] = info[4]
        item["edu"] = info[6]
        item["exp"] = info[8]
        item["tags"] = ",".join(response.css(".myj-tag span::text").extract())
        item["date"] = response.css(".time span::text").extract_first().strip().split(" ")[0]
        item["des"] = ",".join(i.strip() for i in response.css(".myj-details-descrip p::text").extract())

        return item



