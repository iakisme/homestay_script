from craigslist_api import craigslist

if __name__ == '__main__':
    c = craigslist()
    c.sign_up_and_login()
    c.accept()
    c.create_post()