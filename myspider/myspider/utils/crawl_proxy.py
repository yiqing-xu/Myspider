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
        self.conn = pymysql.connect(host="localhost", user="root", passwd="122317#*xyq", db="scrapy", charset="utf8", )
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

    def extract_proxy(self):
        # 从数据库抽取可用代理
        random_sql = """
            SELECT ip, port, protocol FROM proxy ORDER BY speed ASC LIMIT 1
        """
        result = self.cursor.execute(random_sql)
        for proxy_info in self.cursor.fetchall():
            ip = proxy_info[0]
            port = proxy_info[1]
            protocol = proxy_info[2].lower()
            judge_re = self.judge_ip(ip, port, protocol)
            if judge_re:
                proxy = "{0}://{1}:{2}".format(protocol, ip, port)
                return proxy
            else:
                return self.extract_proxy()

    def delete_proxy(self, ip):
        # 从数据库中删除无效的ip
        delete_sql = """
            delete from proxy where ip='{0}'
        """.format(ip)
        self.cursor.execute(delete_sql)
        self.conn.commit()
        return True

    def judge_ip(self, ip, port, protocol):
        # 判断ip是否可用
        proxy_url = "{0}://{1}:{2}".format(protocol, ip, port)
        try:
            proxy_dict = {
                protocol: proxy_url,
            }
            response = requests.get(self.conn_url, proxies=proxy_dict)
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
    parse = GetProxy()
    parse.parse_proxy()
