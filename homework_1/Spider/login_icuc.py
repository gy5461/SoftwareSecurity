# -*- coding: utf-8 -*-

# 登录数字中传，并跳转到“个人信息”页。

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


class icuc_spider:
    driver = None
    main_page_url = 'http://i.cuc.edu.cn'
    main_page_title = '数字中传身份认证'
    login_error_mark = '用户名和密码输入有误'
    login_succeed_title = '数字中传 | Digitalized CUCDCP'

    base_url = 'http://i.cuc.edu.cn/cucdcp/'
    portal_url = 'http://i.cuc.edu.cn/cucdcp/forward.action?path=/portal/portal&p=oaemail&ac=1'

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/51.0.2704.63 Safari/537.36'}
    cookies = None
    request_session = None

    def __init__(self):

        if platform.system() == 'Windows':
            self.chrome_driver_path = "chromedriver.exe"
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
    def login(self):
        self.driver.get(self.main_page_url)
        time.sleep(1)
        if self.driver.title != self.main_page_title:
            print('不是期望的主页Title，网页改版了？')
            return False
        elem_user = self.driver.find_element_by_id('un')
        elem_pwd = self.driver.find_element_by_id('pd')
        elem_user.send_keys("201711143031")
        elem_pwd.send_keys("584034912guoyi")
        elem_pwd.send_keys(Keys.RETURN)

        time.sleep(1)
        '//*[@id="casYhm_text"]'
        '//*/div/div[2]/div[1]'
        if (self.driver.find_elements_by_xpath("//*[contains(text(), '" + self.login_error_mark + "')]") != None) \
                and (self.driver.title != self.login_succeed_title):
            print('登录错误')
            return False
        self.cookies = self.driver.get_cookies()
        self.request_session = requests.Session()
        for cookie in self.cookies:
            self.request_session.cookies.set(cookie['name'], cookie['value'])
        return True

    def jumpto_personal_info_index_page(self):

        '//*[@id="appMenuWidget-content"]/div/div[4]/ul/li[2]/a'
        x_path_per_info = "//a[@class='left_tab_core']/font[text()='个人信息']"

        link_to_per_info = self.driver.find_element_by_xpath(x_path_per_info)
        link_to_per_info.click()
        time.sleep(1)

        return


if __name__ == "__main__":
    icuc = icuc_spider()
    if icuc.login():
        icuc.jumpto_personal_info_index_page()
