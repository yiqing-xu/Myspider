# Myspider
### 在myspider中是一个scrapy框架完成的爬虫项目。
    spiders文件夹中：
        csdn.py通过scrapy中的crawlspider模板创建，全站爬取csdn网站上的文章和招聘信息；
        jobbole.py抓取伯乐在线的文章内容；
        ddebook.py爬取当当网电子图书。
#### items中定义SQL语句
#### pipelines与Mysql交互
#### middlewares中定义了随机UA方法，代理方法，selenium自动化方法


# check_express.py
### requests, Tkinter
    使用requests模块的post方法发送query_data调用快递查询网站的数据，实现查询快递信息的功能，
    使用自带Tkinter的GUI模块，制作简易的图形界面
