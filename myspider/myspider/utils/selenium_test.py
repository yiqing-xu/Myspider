# -*- coding: "utf-8" -*-
__author__ = "xyq"

from selenium import webdriver
from scrapy.selector import Selector
import time


# 模拟登陆微博
browser = webdriver.Chrome(executable_path=r"D:\Webdrive\chromedriver.exe")
browser.get("https://weibo.com/")
time.sleep(30)
browser.find_element_by_css_selector("#loginname").send_keys("")
browser.find_element_by_css_selector(".info_list.password input[name='password']").send_keys("")
browser.find_element_by_css_selector("div[node-type='normal_form'] .info_list.login_btn a").click()
# selector = Selector(text=browser.page_source)
# selector.css()
# browser.quit()


# 设置chromedrive不加载图片
chrome_opt = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images": 2}
chrome_opt.add_experimental_option("prefs", prefs)
browser = webdriver.Chrome(executable_path=r"D:\Webdrive\chromedriver.exe", chrome_options=chrome_opt)
browser.get("https://www.taobao.com/")


# phantomjs,无界面的浏览器,多进程情况下性能会下降很严重,多用于无界面的操作系统
browser = webdriver.PhantomJS(executable_path="D:/Webdrive/phantomjs-2.1.1-windows/bin/phantomjs.exe")
browser.get("https://www.taobao.com")
print(browser.page_source)
browser.quit()

