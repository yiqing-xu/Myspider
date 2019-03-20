from lxml import etree
from selenium import webdriver
import pymysql

from collections import deque
import os


class GetProxy(object):
    """
    爬取 http://www.goubanjia.com/ 上的代理IP，使用selenium自动化
    """
    def __init__(self):
        self.conn = pymysql.connect(host="localhost", user="root", passwd="122317#*xyq", db="scrapy", charset="utf8")
        self.cursor = self.conn.cursor()
        self.path = os.path.abspath(os.path.dirname(__file__))

    def crawl_page(self):
        url = "http://www.goubanjia.com/"
        broswer = webdriver.Chrome(executable_path=self.path + r"\chromedriver.exe")
        broswer.get(url)
        html = broswer.page_source
        broswer.quit()
        return html

    def anlysis_html(self):
        proxy = deque([], 1)
        html = etree.HTML(self.crawl_page())
        tr_list = html.xpath('//table[@class="table table-hover"]/tbody//tr')
        for tr in tr_list:
            ip_port = tr.xpath('./td[1]//*[not(name()="p")]//text()')
            protocol = tr.xpath('./td[3]/a/text()')[0]
            ip = "".join(ip_port[:-1])
            port = ip_port[-1]
            proxy.append((protocol, ip, port))
            info = proxy[0]
            self.cursor.execute("insert ignore into proxy1( protocol, ip, port)  VALUES('{0}', '{1}', '{2}')".format(info[0], info[1], info[2]))
            self.conn.commit()


if __name__ == '__main__':
    parse = GetProxy()
    parse.anlysis_html()
