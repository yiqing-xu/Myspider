# -*- coding: utf-8 -*-
import scrapy
from urllib import parse
from myspider.items import MyItemLoader, JobboleItem
from myspider.utils.common import get_md5
import datetime
from scrapy.loader import ItemLoader


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):

        parse_nodes = response.css('#archive .floated-thumb .post-thumb a')

        for parse_node in parse_nodes:
            img_url = parse_node.css('img::attr(src)').extract_first("")
            parse_url = parse_node.css('::attr(href)').extract_first("")
            yield scrapy.Request(url=parse.urljoin(response.url, parse_url), meta={"front_img": img_url}, callback=self.parse_detail)

        next_url = response.css('.next.page-numbers::attr(href)').extract_first("")
        if next_url:
            yield scrapy.Request(url=parse.urljoin(response.url, next_url), callback=self.parse)

    def parse_detail(self, response):

        # aticle_item = AticleSpider()

        # xpath提取数据
        # title = response.xpath('//*[@id="post-114610"]/div[1]/h1/text()').extract()[0]
        # praise_num = response.xpath('//*[@id="114610votetotal"]/text()').extract_first("")
        # collection = response.xpath('//*[@id="post-114610"]/div[3]/div[3]/span[2]/text()').extract()[0]
        # collection_num = re.match(".*(\d+).*", collection)
        # if collection_num:
        #     collection = collection_num.group(1)
        # tag_list = response.xpath('//*[@id="post-114610"]/div[2]/p/a/text()').extract()
        # tag_list = [element for element in tag_list if not element.strip().endswith("职场")]
        # tags = ",".join(tag_list)
        # content = response.xpath('//*[@id="post-114610"]/div[3]')

        # css选择器
        # title = response.css('.entry-header h1::text').extract()[0]
        # with open("123.txt", "a", encoding="utf-8") as f:
        #     f.write(title)
        #     f.write("\n")
        # praise_num = response.css(".vote-post-up h10::text").extract()[0]
        # collection_num = response.css('.bookmark-btn::text').extract()[0]
        # collection = re.match(".*(\d+).*", collection_num)
        # if collection:
        #     collection_num = collection.group(1)
        # else:
        #     collection_num = 0
        # date = response.css('.entry-meta-hide-on-mobile::text').extract()[0].strip().replace("·", "")
        # tag_list = response.css('.entry-meta-hide-on-mobile a::text').extract()
        # # tag_list = [i for i in tag_list if not i.endswith("微软")]
        # tags = ",".join(tag_list)
        # content = response.css('div.entry').extract()[0]
        #
        # aticle_item["front_img_url"] = [front_img_url]
        # aticle_item["url"] = response.url
        # aticle_item["url_object_id"] = get_md5(response.url)
        # aticle_item["title"] = title
        # aticle_item["praise_num"] = praise_num
        # aticle_item["collection_num"] = collection_num
        # try:
        #     date = datetime.datetime.strptime(date, "%y/%m/%d").date()
        # except Exception as e:
        #     date = datetime.datetime.now().date()
        # aticle_item["date"] = date
        # aticle_item["tags"] = tags
        # aticle_item["content"] = content

        # 通过Itemloader加载item
        front_img_url = response.meta.get("front_img", "")
        item_loader = MyItemLoader(item=JobboleItem(), response=response)
        item_loader.add_value("front_img_url", [front_img_url])
        item_loader.add_css("title", '.entry-header h1::text')
        item_loader.add_value("url", response.url)
        item_loader.add_value("url_object_id", get_md5(response.url))
        item_loader.add_css("praise_num", ".vote-post-up h10::text")
        item_loader.add_css("collection_num", '.bookmark-btn::text')
        item_loader.add_css("date", '.entry-meta-hide-on-mobile::text')
        item_loader.add_css("tags", '.entry-meta-hide-on-mobile a::text')
        item_loader.add_css("content", 'div.entry')

        aticle_item = item_loader.load_item()
        yield aticle_item


