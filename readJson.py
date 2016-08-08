# -*- coding: utf-8 -*-
import requests
import grequests
import json
from bs4 import BeautifulSoup
from time import time
with open('ifoodUsers.json', 'r') as f:
    jds = json.load(f)
headers = {
    'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.86 Safari/537.36'
}
count = 1
while True:
    start = time()
    print '準備執行第 %d 次測試' % count
    for jd in jds['user']:
        print jd['display_name']
        rs = (grequests.get(u, headers=headers, timeout=3) for u in jd['blog'])
        res = grequests.map(rs, size=10)
        for i in xrange(0, len(jd['blog'])):
            while res[i] == None or (res[i].status_code != 200 and res[i].status_code != 404):
                try:
                    print "sending"
                    res[i] = requests.get(jd['blog'][i], headers=headers, timeout=3)
                except:
                    print "failed"
            if res[i].status_code == 404:
                print i+1, "網誌已移除"
            res[i].encoding = 'utf-8'
            soup = BeautifulSoup(res[i].text,'html.parser')
            art = soup.select('.article-content-inner p')
            line = [a.text for a in art if a.text!=""]
            s = "".join(line).encode('utf-8').split('// <![CDATA')[0].strip()
            print i+1,s
    count += 1
    end = time()
    print 'runtime:', end-start
