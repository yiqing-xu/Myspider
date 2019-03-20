# -*- coding: "utf-8" -*-
__author__ = "xyq"

from collections import deque
import requests
from scrapy.selector import Selector
import pymysql


class GetProxy(object):
    """
    完成下载中间件的IP代理功能
    """

    def __init__(self):
        self.conn = pymysql.connect(host="localhost", user="root", passwd="122317#*xyq", db="scrapy", charset="utf8")
        self.cursor = self.conn.cursor()
        self.conn_url = "http://blog.jobbole.com/all-posts/"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/72.0.3626.109 Safari/537.36",
        }

    def parse_proxy(self):
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


if __name__ == '__main__':
    parse = GetProxy()
    parse.parse_proxy()
