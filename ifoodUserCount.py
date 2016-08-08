# -*- coding: utf-8 -*-
import requests
import time
import json
start = time.time()
with open('./Workspace/data/userlist.json','r') as f: #讀取舊檔
    old = json.load(f)
head = {
    'User-Agent': 'ai shi ji/5.2.0 (iPhone; iOS 9.3.1; Scale/2.00)User-Agent: ai shi ji/5.2.0 (iPhone; iOS 9.3.1; Scale/2.00)'
}
url = 'https://ifoodie.tw/api/user/?limit={}&offset={}'
userSet = set(old['users']) #把清單變為set方便之後加入時不加到重複
limit = 300
offset = 0
user = {}
count = 1
while True:
    try:
        res = requests.get(url.format(limit, offset), headers=head)
        jd = json.loads(res.text, encoding='utf8')
        r = jd['response']
        for u in jd['response']:
            userSet.add(u['id'])
            userList = list(userSet)
            user['users'] = userList
            print '第%d次運行 /' % count,'%d users' % len(userList)
            count += 1
    except:
        "no response"
    if len(r) < 300:
        break
    offset += limit
with open('./Workspace/data/userlist.json','w') as f: #輸出新檔
    json.dump(user,f)
print time.time()-start
