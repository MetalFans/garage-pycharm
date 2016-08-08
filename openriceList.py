import random
import re
import requests
import time
import math
import numpy as np
import operator
from bs4 import BeautifulSoup as bs
from collections import Counter
import os
import json
data = {}
for fname in os.listdir('/Users/fan/anaconda/bin/Workspace/data/openrice/'):
    if 'openrice' in fname:
        with open('/Users/fan/anaconda/bin/Workspace/data/openrice/' + fname, 'r') as f:
            jd = json.load(f)
            for ele in jd:
                if ele not in data:
                    data[ele] = jd[ele]

urlList = []
for u in data.values():
    urlList.append(u['shortenUrl'])

domain = 'http://tw.openrice.com'
rs = requests.session()
rs.headers.update({
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
    })

def getRivewURL(rs, u):
    res = rs.get(u)
    soup = bs(res.text, 'html.parser')
    review = domain + soup.select('.main-menu.table-center li')[1].select('a')[0]['href']
    number = soup.select('.main-menu.table-center li')[1].select('a')[0].text
    count = int(re.search('(\d+)', number).group(1))
    page = int(math.ceil(count / 15.0))
    return (review, page, count)

result = []
count = 0
with open('/Users/fan/anaconda/bin/Workspace/log/testOPB.txt', 'a') as f2:
    with open('/Users/fan/anaconda/bin/Workspace/log/testOPG.txt', 'a') as f:
        for i in xrange(len(urlList)):
            try:
                tu = getRivewURL(rs, urlList[i])
            except:
                pass
            count += 1
            print count, tu
            if tu[2] != 0:
                result.append(urlList[i])
                f.write(urlList[i] + '\n')
            else:
                f2.write(urlList[i] + '\n')