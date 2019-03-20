import pymysql
import requests


class HandleProxy(object):
        """
        extract_proxy()  从数据库中提取代理数据
        delete_proxy()   定义SQL语句从数据库中删除无用代理

        """
        def __init__(self):
            self.headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
            }
            self.conn = pymysql.connect(host="localhost", user="root", passwd="122317#*xyq", db="scrapy", charset="utf8")
            self.cursor = self.conn.cursor()
            self.conn_url = "http://www.baidu.com"

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
    handle = HandleProxy()
    handle.extract_proxy()
