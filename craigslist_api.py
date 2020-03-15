import json
import re
import time

import requests
from bs4 import BeautifulSoup

from email_api import email
from urllib.parse import urlparse


class craigslist():
    session = None
    email_ad = ''
    def __init__(self):
        global session
        session = requests.session()

    def save_cookies(self):  # 保存cookie
        global session, path_for
        with open('./' + "craigslistcookiefile", 'w')as f:
            json.dump(session.cookies.get_dict(), f)

    def read_cookies(self):  # 使用cookie
        global session, path_for
        # _session.cookies.load()
        # _session.headers.update(header_data)
        with open('./' + 'craigslistcookiefile')as f:
            cookie = json.load(f)
            session.cookies.update(cookie)

    def sign_up_and_login(self):
        e = email()
        email_address = e.get_emailaddress()
        self.email_ad = email_address
        r = session.post('https://accounts.craigslist.org/signup',
                         headers={'Content-Type': 'application/x-www-form-urlencoded',
                                  'Origin': 'https://accounts.craigslist.org',
                                  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
                                  'Referer': 'https://accounts.craigslist.org/login'}, data={
                'emailAddress': email_address,
                'rq': '/login/home',
                'rt': 'L',
                't': int(time.time())
            })
        if 'Thanks for signing up for a craigslist account!' in r.text:
            print('Thanks for signing up for a craigslist account!')
            print("_--------------------------------------------------------")

        else:
            print('sign up error')
        login_url = ''
        while True:
            print('e.get_content_by_craigslist()')
            login_url = e.get_content_by_craigslist()
            if not login_url:
                time.sleep(10)
            else:
                print(login_url)
                break

        o = urlparse(login_url)
        query_data = {x.split('=')[0]: x.split('=')[1] for x in o.query.split('&')}
        query_data['goPasswordless'] = '1'
        r = session.post('https://accounts.craigslist.org/pass',
                         headers={'Content-Type': 'application/x-www-form-urlencoded',
                                  'Origin': 'https://accounts.craigslist.org',
                                  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
                                  'Referer': login_url}, data=query_data)
        print(r.status_code)
        print('_________________---=--------------------')
        print('cookies')
        print(session.cookies)
        self.save_cookies()

    def account(self):
        self.read_cookies()
        r = session.get('https://accounts.craigslist.org/login/home')
        print('*********************************home')
        print(r.status_code)

    def accept(self):
        self.read_cookies()
        query_data = {
            'step': 'touAccepted',
            'rt': '',
            'rp': ''
        }
        r = session.post('https://accounts.craigslist.org/login/tou',
                         headers={'Content-Type': 'application/x-www-form-urlencoded',
                                  'Origin': 'https://accounts.craigslist.org',
                                  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
                                  'Referer': 'https://accounts.craigslist.org/login/tou'}, data=query_data)
        print('*********************************accept')
        print(r.status_code)

    def create_post(self):
        self.read_cookies()
        r = session.get('https://post.craigslist.org/c/tor',
                        headers={'Content-Type': 'application/x-www-form-urlencoded',
                                 'Origin': 'https://post.craigslist.org',
                                 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
                                 'Referer': 'https://toronto.craigslist.org/'})
        print('*********************************create_post')
        print(r.text)
        print(r.status_code)
        soup = BeautifulSoup(r.text, 'html.parser')
        tags = soup.findAll('form', action=re.compile("https://post.craigslist.org/"))
        post_url = tags[0]['action']
        cryptedStepCheck = soup.find_all('input', {"name": "cryptedStepCheck"})[0]['value']
        subarea_data = {}
        session.get(post_url + '?s=subarea', headers={'Content-Type': 'application/x-www-form-urlencoded',
                                                      'Origin': 'https://toronto.craigslist.org/',
                                                      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
                                                      'Referer': 'https://toronto.craigslist.org/'},
                    )
        r = session.post(post_url,
                         headers={'Content-Type': 'application/x-www-form-urlencoded',
                                  'Origin': 'https://toronto.craigslist.org/',
                                  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
                                  'Referer': 'https://toronto.craigslist.org/'},
                         data={'n': '1', 'cryptedStepCheck': cryptedStepCheck})
        print('1______________________________________')
        print(post_url)
        print(r.status_code)

        session.get(post_url + '?s=type', headers={'Content-Type': 'application/x-www-form-urlencoded',
                                                   'Origin': 'https://toronto.craigslist.org/',
                                                   'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
                                                   'Referer': 'https://toronto.craigslist.org/'})
        r = session.post(post_url,
                         headers={'Content-Type': 'application/x-www-form-urlencoded',
                                  'Origin': 'https://toronto.craigslist.org/',
                                  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
                                  'Referer': 'https://toronto.craigslist.org/'},
                         data={'id': 'ho', 'cryptedStepCheck': cryptedStepCheck})
        print('2________________________________________')
        print(r.status_code)

        r = session.post(post_url,
                         headers={'Content-Type': 'application/x-www-form-urlencoded',
                                  'Origin': 'https://toronto.craigslist.org/',
                                  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
                                  'Referer': 'https://toronto.craigslist.org/'},
                         data={'id2': '2019x810X2019x576X2048x1152', 'id': '18', 'cryptedStepCheck': cryptedStepCheck})
        print('3_________________________________________')
        print(r.status_code)

        data = {"id2": "1411x1245X1411x568X1440x900",
                "PostingTitle": "Toronto+student+homestay",
                "GeographicArea": "Toronto",
                "postal": "M2J0B3",
                "PostingBody": "Please+check+out+this+homestay%0D%0Ahttps%3A%2F%2Fwww.homadorma.com%2Fen%2Fhomestay%2FHS104267",
                "price": "",
                "Sqft": "0",
                "private_room": "0",
                "private_bath": "0",
                "housing_type": "6",
                "laundry": "",
                "parking": "",
                "movein_date": "",
                "FromEMail": self.email_ad,
                "Privacy": "C",
                "go": "continue",
                "cryptedStepCheck": "U2FsdGVkX18zMTM5ODMxMx-_4o5EoXILYZOz0Ebyl5G7RWC-3j0KCQDBw8F0dVvK",
                }

        r = session.post(post_url,
                         headers={'Content-Type': 'application/x-www-form-urlencoded',
                                  'Origin': 'https://toronto.craigslist.org/',
                                  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
                                  'Referer': 'https://toronto.craigslist.org/'},
                         data=data)
        print('4_________________________________________')
        print(r.status_code)

        r = session.get('https://accounts.craigslist.org/login/home?show_tab=drafts',
                        headers={'Content-Type': 'application/x-www-form-urlencoded',
                                 'Origin': 'https://toronto.craigslist.org/',
                                 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
                                 'Referer': 'https://toronto.craigslist.org/'})
        print('5_________________________________________')
        print(r.status_code)
        print(r.text)
