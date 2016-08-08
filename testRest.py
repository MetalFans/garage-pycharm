import requests
import json
head = {
    'User-Agent': 'ai shi ji/5.2.0 (iPhone; iOS 9.3.1; Scale/2.00)User-Agent: ai shi ji/5.2.0 (iPhone; iOS 9.3.1; Scale/2.00)'
}
url = 'https://ifoodie.tw/api/collection/55f7d2e42756dd1dbcd4fd63/blogs/?limit=33&offset=0'
res = requests.get(url, verify=False, headers=head)
jd = json.loads(res.text, encoding='unicode')
r = jd['response']
c = 1
for i in r:
    print c,i['restaurant']['id']
    c += 1
