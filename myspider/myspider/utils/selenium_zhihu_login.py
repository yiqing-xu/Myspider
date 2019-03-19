# -*- coding: "utf-8" -*-
__author__ = "xyq"

from selenium import webdriver
import time

browser = webdriver.Chrome(executable_path=r"D:\Webdrive\chromedriver.exe")
browser.get("https://www.zhihu.com/signin")
# time.sleep(2)
# browser.find_element_by_css_selector(".SignContainer-switch span").click()
# time.sleep(2)
# browser.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys("18728191137")
# time.sleep(2)
# browser.find_element_by_xpath("//*[@id='root']/div/main/div/div/div/div[2]/div[1]/form/div[2]/div/div[1]/input").send_keys("122317#*xyq")
# time.sleep(2)
# browser.find_element_by_xpath("//*[@id='root']/div/main/div/div/div/div[2]/div[1]/form/button").click()

# browser = webdriver.Chrome(executable_path=r"D:\Webdrive\chromedriver.exe")
# browser.get("https://weibo.com/")
# # time.sleep(2)
# # browser.find_element_by_css_selector(".SignContainer-switch span").click()
# time.sleep(10)
# browser.find_element_by_xpath('//*[@id="loginname"]').send_keys("18728191137")
# time.sleep(2)
# browser.find_element_by_xpath("//*[@id='pl_login_form']/div/div[3]/div[2]/div/input").send_keys("122317#*xyq")
# time.sleep(2)
# browser.find_element_by_xpath("//*[@id='pl_login_form']/div/div[3]/div[6]/a").click()
