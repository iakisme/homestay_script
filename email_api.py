# -*- coding: UTF-8 -*-
import requests
from bs4 import BeautifulSoup
import json
import re

url = "https://10minutemail.net"
header_data = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch, br',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'referer': "https://10minutemail.net/error-due.html",
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36'
}


class email():
    session = None

    def __init__(self):
        global session
        session = requests.session()

    # self.get_emailaddress()#第一个函数，直接return 邮箱地址
    # self.get_content()
    # self.vertify_email()
    def get_emailaddress(self):  # 获取新的邮箱地址
        global session
        global header_data
        global url
        r = session.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        self.save_cookies()
        print(soup.findAll('title'))
        return soup.input["value"]  # 返回邮箱地址

    def get_content_by_craigslist(self):
        global session
        global header_data
        global url
        letterurl = url
        self.read_cookies()
        r = session.get(letterurl)
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, 'html.parser')
        mail_contect = ''
        print('email:' + soup.input["value"])
        soup.findAll('a', href=re.compile("readmail.html"))
        content = ''
        for x in soup.findAll('a', href=re.compile("readmail.html")):
            if 'craigslist.org' in str(x):
                print(x['href'])
                content = x['href']
        print('conent=' + content)
        if content:
            letterurl = url + '/' + content
            self.read_cookies()
            print('letterurl:' + letterurl)
            r = session.get(letterurl)
            soup = BeautifulSoup(r.text, 'html.parser')
            for x in soup.find_all('a',
                                   href=re.compile("https://accounts.craigslist.org/pass")):  # will give you all a tag
                print('pass:' + x['href'])
                return x['href']

    def save_cookies(self):  # 保存cookie
        global session, path_for
        with open('./' + "emailcookiefile", 'w')as f:
            json.dump(session.cookies.get_dict(), f)

    def read_cookies(self):  # 使用cookie
        global session, path_for
        # _session.cookies.load()
        # _session.headers.update(header_data)
        with open('./' + 'emailcookiefile')as f:
            cookie = json.load(f)
            session.cookies.update(cookie)
