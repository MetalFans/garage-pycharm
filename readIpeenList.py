# -*- coding: utf-8 -*-
import json
with open('./Workspace/data/ipeenList.json', 'r') as f:
    jd = json.load(f)['restaurants']
count = 1
for i in jd:
    print '[%d]' % count
    print i['ifoodName'] + ' | ' + i['ipeenName']
    print i['ifoodAddress'] + ' | ' +i['ipeenAddress']
    print i['ifoodURL'] + ' | ' +i['ipeenURL'] + ' | ' + 'https://ifoodie.tw/search?q=%s' % i['ipeenName']
    count += 1