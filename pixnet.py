# -*- coding: utf-8 -*-
import grequests
import requests
import json
from bs4 import BeautifulSoup
import re
pixnet = {}
pixnetList = []

def removePunctuation(source):
    temp = source.decode('utf-8')
    xx = u"([^0-9^a-z^A-Z^\u4e00-\u9fff]+)"
    s = re.sub(xx,' ',temp)
    return s


with open('ifood.json', 'r') as f:
    jd = json.load(f)
headers = {
    'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.86 Safari/537.36'
}

rs = (grequests.get(u, headers=headers) for u in jd['blog'])
response = grequests.map(rs, size=20)
c = 1
for res in response:
    while res == None or (res.status_code != 200 and res.status_code != 404):
        print 'sending...'
        res = requests.get(res.url, headers=headers, timeout=5)
    if res.status_code == 404:
        print c, 'removed'
    else:
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text,'html.parser')
        [x.extract() for x in soup.select('script')]
        [x.extract() for x in soup.select('a')]
        art = soup.select('.article-content-inner')
        line = [a.text for a in art if a.text!=""]
        st = "".join("".join(line).split()).strip(',').replace(u'延伸閱讀','').replace('^','')
        s = removePunctuation(st.encode('utf-8'))
        pixnetList.append(s)
        print c, s, res.url
    c += 1
pixnet['context'] = pixnetList
with open('./Workspace/data/pixneTest.json', 'w') as f:
    json.dump(pixnet, f)
