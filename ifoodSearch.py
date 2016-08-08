# -*- coding: utf-8 -*-
import requests
import json
import time
import os.path
import csv
start = time.time()
#classlist = ['鍋類','牛排','精緻高級','燒肉','居酒屋','日式','小吃','合菜','甜點','早午餐','下午茶','咖啡','韓式','吃到飽','素食','壽司','拉麵','義式','熱炒','牛肉麵','泰式','美式','港式','輕食','漢堡','咖哩']
with open('./restaurantType.json', 'r') as f:
    classdict = json.load(f)
classlist = []
for wordlist in classdict.values():
    classlist.extend(wordlist)
classlist = [ele.encode('utf-8') for ele in classlist]

latlng = []
with open('./Workspace/data/latlng.csv', 'r') as f: #讀取各行政區經緯度
    for row in csv.reader(f):
        latlng.append(row[3]+','+row[2])

head = {
    'User-Agent': 'ai shi ji/5.2.0 (iPhone; iOS 9.3.1; Scale/2.00)User-Agent: ai shi ji/5.2.0 (iPhone; iOS 9.3.1; Scale/2.00)'
}

for classification in classlist:
    print classification
    rest = set()
    if os.path.isfile('./Workspace/data/%s.json' % classification):
        with open('./Workspace/data/%s.json' % classification,'r') as f:
            rest = set(json.load(f)[classification.decode('utf-8')])
    restaurant = {}
    for loc in latlng[1:]: #逐一帶入經緯度
        limit = 300
        offset = 0
        while True: #一次翻300
            url = 'https://ifoodie.tw/api/blog/?offset={}&limit={}&latlng={}&q={}'
            res = requests.get(url.format(offset,limit,loc, classification), headers=head)
            jd = json.loads(res.text, encoding='utf8')
            length = len(rest)
            for ele in jd['response']:
                if ele['restaurant']:
                    rest.add(ele['restaurant']['id'])
            print len(list(rest))
            if len(jd['response']) < 300:
                break
            offset += limit
    restaurant[classification] = list(rest)
    with open('./Workspace/data/%s.json' % classification,'w') as f:
        json.dump(restaurant,f)
print time.time()-start