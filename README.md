# 代理地址爬取程序（crawl_poroxy目录下）
此程序将会爬取网络上公开的代理`ip`地址信息并保存到`Mysql`数据库中。


# 如何启动
## 数据库配置
* 导入`pymysql`模块中配置`mysql`数据库的链接信息:
    ```python3
        host = '127.0.0.1'  
        user = ''
        passwd = ''
        db = ''
    ```

* 新建一个connect，并使用cursor``：
    ```python3
        conn = pymysql.connect()
        cursor = conn.cursor()
    ```

## 程序启动
在`crawl_proxy`目录中，执行如下命令启动程序：

```python3
    python xxxx.py
```

# 如何处理页面反爬
* `crawl_gbj_proxy.py`爬取的公开代理`ip`地址页面地址是: `http://www.goubanjia.com/`。
* 此页面拥有反爬措施:
    1. 访问页面的时候，网页显示的公开代理地址列表中的所有端口号与真实的response响应中的端口号不一样的，。
    2. 猜想该网页会执行一个js文件，将response响应中错误的端口转换成正确的端口并刷新到浏览器的`html`页面中。
    3. 单单简单的直接使用`requests`或者`scrapy`进行爬取，只会得到错误的response，无法执行`js`文件，得到正确代理地址。
* solution:
    使用`selenium`模拟浏览器行为发起请求，在`.page_source`方法中会返回正确端口的页面`html`数据。

# 如何验证代理地址的正确性

## 定义`handle_proxy.py`程序

此程序将保存在`Mysql`数据库中的数据协议`procotol`，`ip`地址，端口号`port`提取出来提取出来做验证。

* 通过requests方法的`paoxies`参数传入一个字典形式的代理地址，验证返回的response中的`statu_code`是否为200，
  从而达到验证代理地址的正确性
* 定义`SQL`语句对数据库的内容进行删除


# `srapy`爬虫（`Myspider`目录下）
### 在`myspider`中是一个`scrapy`框架完成的爬虫。
* `spiders`文件夹中：
* `csdn.py`通过`scrapy`中的`crawlspider`模板创建，通过匹配正确的`LinkExtractor(allow=r'https://blog.csdn.net/\w+/article/details/\d+')`网址，全站爬取`csdn`网站上的文章和招聘信息；
* `jobbole.py`抓取伯乐在线的文章内容，此爬虫中使用定义`ItemLoader`，达到在`spider`中简化程序，将数据在`items`中定义函数处理的效果；
* `ddebook.py`爬取当当网电子图书，当当网在多次请求后就会返回`302`的重定向的错误界面，此时可使用随机UA及IP代理池抽取IP代理的方法达到反爬的效果，另外在`scrapy.Request`中传递数据时使用`deepcopy`方法使得`item`的数据不会重复和混乱。

#### items中定义SQL语句
#### pipelines与Mysql交互
#### middlewares中定义了随机UA方法，代理方法，selenium自动化方法


# check_express.py
### requests, Tkinter
    使用requests模块的post方法发送query_data调用快递查询网站的数据，实现查询快递信息的功能，
    使用自带Tkinter的GUI模块，制作简易的图形界面
