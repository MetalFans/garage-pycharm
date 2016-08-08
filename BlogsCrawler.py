# -*- coding: utf-8 -*-
import re
import requests
from bs4 import BeautifulSoup as bs


def removePunctuation(source):
    xx = u"([^a-z^A-Z^\u4e00-\u9fff]+)"
    s = re.sub(xx, ' ', source)
    return s


def removeTag(soup,tag):
    [x.extract() for x in soup.select(tag)]


# xuite
res = requests.get('http://blog.xuite.net/ca062/blog/413854020')
res.encoding = 'utf-8'
soup = bs(res.text, 'html.parser')
[x.extract() for x in soup.select('script')]
removeTag(soup,'script')
removeTag(soup,'a')
removeTag(soup,'.rank')
removeTag(soup,'iframe')
art = soup.select('.blogbody')
line = [a.text for a in art if a.text != ""]
st = "".join("".join(line).split()).replace(u'延伸閱讀', '').replace('^','')
s = removePunctuation(st)
print s

# pixnet
res = requests.get('http://yao55.pixnet.net/blog/post/31422842')
res.encoding = 'utf-8'
soup = bs(res.text,'html.parser')
removeTag(soup,'script')
removeTag(soup,'a')
removeTag(soup,'.rank')
removeTag(soup,'iframe')
art = soup.select('.article-content-inner')
line = [a.text for a in art if a.text!=""]
st = "".join("".join(line).split()).replace(u'延伸閱讀','').replace('^','')
s = removePunctuation(st)
print s

# ifoodie
res = requests.get('https://ifoodie.tw/post/573c6fa92756dd04749b8ab2')
res.encoding = 'utf-8'
soup = bs(res.text,'html.parser')
removeTag(soup,'script')
removeTag(soup,'a')
removeTag(soup,'.rank')
removeTag(soup,'iframe')
art = soup.select('#blog_content')
line = [a.text for a in art if a.text!=""]
st = "".join("".join(line).split()).strip(',').replace(u'延伸閱讀','').replace('^','')
s = removePunctuation(st)
print s

# miha
res = requests.get('https://miha.tw/tp-vegetejiya/')
res.encoding = 'utf-8'
soup = bs(res.text,'html.parser')
removeTag(soup,'script')
removeTag(soup,'a')
removeTag(soup,'.rank')
removeTag(soup,'iframe')
art = soup.select('#content article p')
line = [a.text for a in art if a.text!=""]
st = "".join("".join(line).split()).replace(u'延伸閱讀','').replace('^','')
s =  removePunctuation(st)
print s

# banbi
res = requests.get('https://banbi.tw/weichi-sweets/')
res.encoding = 'utf-8'
soup = bs(res.text,'html.parser')
removeTag(soup,'script')
removeTag(soup,'a')
removeTag(soup,'.rank')
removeTag(soup,'iframe')
art = soup.select('article')
line = [a.text for a in art if a.text!=""]
st = "".join("".join(line).split()).replace(u'延伸閱讀','').replace('^','')
s =  removePunctuation(st)
print s

# 合併
print '====================='
print '萬用版'
print '====================='
# http://blog.xuite.net/ca062/blog/413854020
# http://yao55.pixnet.net/blog/post/31422842
# https://ifoodie.tw/post/573c6fa92756dd04749b8ab2
# https://miha.tw/tp-vegetejiya/
# https://banbi.tw/weichi-sweets/
res = requests.get('http://yao55.pixnet.net/blog/post/31422842')
res.encoding = 'utf-8'
soup = bs(res.text,'html.parser')
removeTag(soup,'script')
removeTag(soup,'a')
removeTag(soup,'.rank')
removeTag(soup,'iframe')
xuite = soup.select('.blogbody')
pixnet = soup.select('.article-content-inner')
ifoodie = soup.select('#blog_content')
miha = soup.select('#content article p')
banbi = soup.select('article')
art = xuite+pixnet+ifoodie+miha+banbi
line = [a.text for a in art if a.text!=""]
st = "".join("".join(line).split()).replace(u'延伸閱讀','').replace('^','')
s =  removePunctuation(st)
print s