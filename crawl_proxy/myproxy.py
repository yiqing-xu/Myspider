from lxml import etree
from selenium import webdriver
import pymysql
from scrapy.selector import Selector
import requests

from collections import deque
import os


class MyProxy(object):

    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
        }
        self.conn = pymysql.connect(host="localhost", user="root", passwd="122317#*xyq", db="scrapy", charset="utf8")
        self.cursor = self.conn.cursor()
        self.path = os.path.abspath(os.path.dirname(__file__))
        self.conn_url = "http://www.baidu.com"

    def crawl_gbj_page(self):
        # 爬取 http://www.goubanjia.com/ 上的代理ip
        url = "http://www.goubanjia.com/"
        broswer = webdriver.Chrome(executable_path=self.path + r"\chromedriver.exe")
        broswer.get(url)
        html = broswer.page_source
        broswer.quit()

        html = etree.HTML(html)
        tr_list = html.xpath('//table[@class="table table-hover"]/tbody//tr')
        proxy = deque([], 1)
        for tr in tr_list:
            ip_port = tr.xpath('./td[1]//*[not(name()="p")]//text()')
            protocol = tr.xpath('./td[3]/a/text()')[0]
            ip = "".join(ip_port[:-1])
            port = ip_port[-1]
            proxy.append((protocol, ip, port))
            info = proxy[0]
            self.cursor.execute("insert ignore into proxy1( protocol, ip, port)  VALUES('{0}', '{1}', '{2}')".format(info[0], info[1], info[2]))
            self.conn.commit()

    def crawl_cixi_page(self):
        # 爬取西刺代理上的ip代理
        for i in range(1, 3600):
            url = "https://www.xicidaili.com/nn/{0}".format(i)
            response = requests.get(url, headers=self.headers)
            selector = Selector(text=response.content.decode())

            td_list = selector.css(".odd")
            for td in td_list:
                speed = td.css(".bar::attr(title)").extract_first()
                speed = float(speed.split("秒")[0])

                text_list = td.css("::text").extract()
                text = [i for i in text_list if len(i.strip()) > 0]

                proxy_list = deque([], 1)

                if text[4] == "HTTPS" or text[4] == "HTTP":
                    ip = text[0]
                    port = text[1]
                    protocol = text[4]

                    proxy_list.append((ip, port, protocol, speed))

                    proxy = proxy_list[0]
                    self.cursor.execute(
                        "insert into proxy(ip, port, protocol, speed) VALUES('{0}', '{1}', '{2}', '{3}')".format(
                            proxy[0], proxy[1], proxy[2], proxy[3]
                        )
                    )
                    self.conn.commit()

    def extract_proxy(self):
        # 从数据库抽取可用代理
        random_sql = """
            SELECT ip, port, protocol FROM proxy1 LIMIT 1
        """
        result = self.cursor.execute(random_sql)
        for proxy_info in self.cursor.fetchall():
            ip = proxy_info[0]
            port = proxy_info[1]
            protocol = proxy_info[2].lower()
            judge_re = self.judge_proxy(ip, port, protocol)
            if judge_re:
                proxy = "{0}://{1}:{2}".format(protocol, ip, port)
                return proxy
            else:
                return self.extract_proxy()

    def delete_proxy(self, ip):
        # 从数据库中删除无效的ip
        delete_sql = """
            delete from proxy1 where ip='{0}'
        """.format(ip)
        self.cursor.execute(delete_sql)
        self.conn.commit()
        return True

    def judge_proxy(self, ip, port, protocol):
        # 判断ip是否可用
        proxy_url = "{0}://{1}:{2}".format(protocol, ip, port)
        try:
            proxy_dict = {
                protocol: proxy_url,
            }
            response = requests.get(self.conn_url, headers=self.headers, proxies=proxy_dict)
        except Exception as e:
            print("无效的IP和Port")
            self.delete_proxy(ip)
            return False
        else:
            if 200 <= response.status_code < 300:
                print("此代理可用")
                return True
            else:
                print("无效的IP和Port")
                self.delete_proxy(ip)
                return False


if __name__ == '__main__':
    parse = MyProxy()
    # parse.crawl_gbj_page()
    parse.crawl_cixi_page()
