import requests
from ra import *
from bs4 import BeautifulSoup
import random
ck={
    '__utma':'156441338.931606428.1461905487.1461905487.1461905487.1',
    '__utmb':'156441338.3.10.1461905487',
    '__utmc':'156441338',
    '__utmt':'1',
    '__utmz':'156441338.1461905487.1.1',
    'over18':'1'
}
proxies = {}
prx = []
count = 1
while True:
    if count > len(prx):
        count = 1
        res = requests.get('http://www.ip-adress.com/proxy_list/?k=type')
        soup = BeautifulSoup(res.text,'html.parser')
        p = soup.select('.proxylist tr')[2:-1]
        prx = []
        for td in p:
            if td.select('td')[1].text == "Anonymous" or td.select('td')[1].text == "Elite":
                prx.append(td.select('td')[0].text)
    try:
        proxies['http'] = prx[count-1]
        res2 = requests.get('http://httpbin.org/get',proxies=proxies, timeout=5)
        if res2.status_code == 200:
            print res2.text
            break
    except:
        print 'Time Out'
    finally:
        count += 1
#res = requests.get('https://www.ptt.cc/bbs/Gossiping/index.html',cookies=ck,proxies=proxies)
#a = ReqAgent()
#pr = a.g('http://httpbin.org/get','ref')
#response = a.send(pr)
#print response.text