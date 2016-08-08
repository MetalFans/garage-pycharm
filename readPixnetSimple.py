# -*- coding: utf-8 -*-
import re
import requests
from bs4 import BeautifulSoup as bs

#去除標點符號及數字
def removePunctuation(source):
    xx = u"([^a-z^A-Z^\u4e00-\u9fff]+)"
    s = re.sub(xx,' ',source)
    return s

res = requests.get('http://hero910904.pixnet.net/blog/post/439367458')
res.encoding = 'utf-8'
soup = bs(res.text,'html.parser')
#去除script標籤
[x.extract() for x in soup.select('script')]
#去除a標籤
[x.extract() for x in soup.select('a')]
art = soup.select('.article-content-inner')
#去除沒東西的廢物
line = [a.text for a in art if a.text!=""]
#去除空格以及垃圾(需建垃圾清單)
st = "".join("".join(line).split()).replace(u'延伸閱讀','').replace('^','')
#去除標點符號及數字
print removePunctuation(st)
