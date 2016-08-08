# -*- coding: utf-8 -*-
import requests
import grequests
from bs4 import BeautifulSoup as bs
import math
import json
import time
import os
start = time.time()
if not os.path.exists('./Workspace/data'):
    os.makedirs('./Workspace/data')

class Agent():
    def __init__(self):
        self.header = {
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36'
        }
        self.cookie = {
            '__flash_buy_ad_cookie':'ok'
        }


def countPages():
    a = Agent()
    url = 'http://www.ipeen.com.tw/search/taiwan/000/1-0-0-0/'
    rs = requests.session()
    res = rs.get(url, cookies=a.header, headers=a.cookie)
    soup = bs(res.text,'html.parser')
    num = int(soup.select('.num b')[0].text)
    pages = int(math.ceil(num/15.0))
    return pages


agent = Agent()
ipeen = {}
restaurants = []
domain = 'http://www.ipeen.com.tw'
url = 'http://www.ipeen.com.tw/search/taiwan/000/1-0-0-0/?p={}'
header = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36'
}
ck = {
    '__flash_buy_ad_cookie':'ok'
}
pages = countPages()
rs = (grequests.get(url.format(p), cookies=agent.cookie, headers=agent.header) for p in xrange(1,pages+1))
print 'preparing requests'
res = grequests.map(rs, size=20)
for r in res:
    if r:
        soup = bs(r.text, 'html.parser')
        titles = [ele for ele in soup.select('.serShop') if ele.select('.name a')[0]['data-action'] != 'ad_shop']
        for title in titles:
            try:
                ct = title.select('.name a')[0].text.replace('(',' ').replace(')','')
                restaurant = {}
                restaurant['ipeenURL'] =  domain+title.select('a')[0]['href'].split('-')[0]
                restaurant['ipeenName'] = ct
                restaurant['ipeenAddress'] = title.select('.basic li')[1].select('span')[0].text.split()[0]
                restaurants.append(restaurant)
            except:
                print "bad respnose"
ipeen['restaurants'] = restaurants
with open('./Workspace/data/ipeenSimpleList.json','w') as f:
    json.dump(ipeen, f)
print '餐廳數：%d' % len(restaurants)
print time.time()-start