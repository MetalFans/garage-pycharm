# -*- coding: utf-8 -*-
import requests
import json
import time
import os
import difflib
import Levenshtein

start = time.time()

with open('/Users/fan/anaconda/bin/Workspace/data/openriceName.json', 'r') as f:
    jd = json.load(f, encoding='utf8')

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
temp = jd.values()[113]
name = temp.split('|')[0]
print temp
ifood = ifoodSearch(name.encode('utf-8'))
if ifood:
    print ifood['name'], ifood['address']
    print difflib.SequenceMatcher(None,name,ifood['name']).ratio()
    print Levenshtein.ratio(name,ifood['name'])
    print Levenshtein.jaro(name,ifood['name'])
    print Levenshtein.jaro_winkler(name,ifood['name'])