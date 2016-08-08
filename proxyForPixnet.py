# -*- coding: utf-8 -*-
import requests
import json
from bs4 import BeautifulSoup
import random


def getproxy():
    res = None
    ck = {
        'Cookie':'__utmz=11986028.1462945261.1.1.utmccn=(direct)|utmcsr=(direct)|utmcmd=(none); __utma=11986028.142856697.1462945261.1462945261.1462950702.2; __utmc=11986028; __utmb=11986028; __asc=3b4454ce1549ea82d4213708470; __auc=1f4883341549e55276d173aec4f; __atuvc=10%7C19; __atuvs=5732db2e8b25716a003'
    }
    while res == None or res.status_code != 200:
        try:
            print "Getting Proxy"
            res = requests.get('http://www.ip-adress.com/proxy_list/?k=type', cookies=ck, timeout=3)
        except:
            print "Failed"
    prx = []
    px = {}
    soup = BeautifulSoup(res.text,'html.parser')
    p = soup.select('.proxylist tr')[2:-1]
    for td in p:
        if td.select('td')[1].text == "Anonymous" or td.select('td')[1].text == "Elite":
            prx.append(td.select('td')[0].text)
    index = random.randint(0,len(prx)-1)
    px['http'] = prx[index]
    print px['http']
    return px

with open('ifood.json', 'r') as f:
    jd = json.load(f)
headers = {
    'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.86 Safari/537.36'
}
print 'start'
c = 1
res = None
for u in jd['blog']:
    while res == None or res.status_code != 200:
        try:
            print "sending"
            res = requests.get(u, headers=headers, proxies=getproxy(), timeout=3)
        except:
            print "failed"
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text,'html.parser')
    art = soup.select('.article-content-inner p')
    line = [a.text for a in art if a.text!=""]
    s = "".join(line).encode('utf-8').split('// <![CDATA')[0].strip()
    print c, s
    c += 1
    res = None