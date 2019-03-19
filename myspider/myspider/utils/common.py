# -*- coding: "utf-8" -*-
__author__ = "xyq"

import hashlib
import logging
import datetime
import time


def get_md5(url):
    # 定义函数将url地址进行hash加密
    if isinstance(url, str):
        url = url.encode("utf-8")
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()


def write_log():
    """
    scrapy中通过top中import logging
    logger =logging.getLogger(__name__)
    即可在下面的对象中调用logger.warning("this is a log")
    """
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(thread)d %(threadName)s %(filename)s[line:%(lineno)d]'
                               ' %(levelname)s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S'
                        )  # 定义日志格式
    logger = logging.getLogger(__name__)  # 输出log执行的py文件位置
    # 通过logger可以打印()中的内容到控制台，并显示执行的py文件位置，可修改warning
    # 可以在settings中写LOG_FILE = "./log.log"将log文件写入到本地
    logger.warning("this is log")
    return


def from_unix_timestamp(unix_ts):
    # 定义函数将普通时间转换为UNIX时间戳
    normal_time = datetime.datetime.fromtimestamp(unix_ts)
    return normal_time


def to_unix_timestamp(normal_time):
    # 定义函数将UNIX时间戳转换为普通时间
    unix_ts = time.mktime(normal_time.timetuple())
    return unix_ts
