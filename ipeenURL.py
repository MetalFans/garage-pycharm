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


def ifoodSearch(t):
    url = 'https://ifoodie.tw/api/blog/?offset=0&limit=1&order_by=-date&q={}'
    head = {
        'User-Agent': 'ai shi ji/5.2.0 (iPhone; iOS 9.3.1; Scale/2.00)User-Agent: ai shi ji/5.2.0 (iPhone; iOS 9.3.1; Scale/2.00)'
    }
    res = requests.get(url.format(t), headers=head)
    jd = json.loads(res.text, encoding='utf8')
    if len(jd['response'])>0:
        r = jd['response'][0]['restaurant']
    else:
        r = None
    return r

agent = Agent()
ipeen = {}
restaurants = []
domain = 'http://www.ipeen.com.tw'
idomain = 'https://ifoodie.tw/restaurant/'
url = 'http://www.ipeen.com.tw/search/taiwan/000/1-0-0-0/?so=commno&p={}'
header = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36'
}
ck = {
    '__flash_buy_ad_cookie':'ok'
}
pages = 10
rs = (grequests.get(url.format(p), cookies=agent.cookie, headers=agent.header) for p in xrange(1,pages+1))
print 'preparing requests'
res = grequests.map(rs,size=20)
for r in res:
    if r:
        soup = bs(r.text, 'html.parser')
        titles = [ele for ele in soup.select('.serShop') if ele.select('.name a')[0]['data-action'] != 'ad_shop']
        for title in titles:
            ct = title.select('.name a')[0].text.replace('(',' ').replace(')','')
            result = ifoodSearch(ct.encode('utf-8'))
            restaurant = {}
            if result:
                restaurant['id'] = result['id']
                restaurant['ipeenURL'] =  domain+title.select('a')[0]['href'].split('-')[0]
                restaurant['ifoodURL'] =  idomain+result['id']
                restaurant['ipeenName'] = ct
                restaurant['ifoodName'] = result['name']
                restaurant['ipeenAddress'] = title.select('.basic li')[1].select('span')[0].text.split()[0]
                restaurant['ifoodAddress'] = result['address']
                restaurants.append(restaurant)
ipeen['restaurants'] = restaurants
with open('./Workspace/data/ipeenList.json','w') as f:
    json.dump(ipeen,f)
print len(restaurants)
print time.time()-start