import requests
import json
from pymongo import MongoClient
import time
import copy

start = time.time()
head = {
    'User-Agent': 'ai shi ji/5.2.0 (iPhone; iOS 9.3.1; Scale/2.00)User-Agent: ai shi ji/5.2.0 (iPhone; iOS 9.3.1; Scale/2.00)'
}
url = 'https://ifoodie.tw/api/user/?limit=1&offset=0'
res = requests.get(url, verify=False, headers=head)
jd = json.loads(res.text, encoding='unicode')
r = jd['response']
connection = MongoClient("ds015962.mlab.com", 15962)
db = connection["hellomongo"]
db.authenticate("pig6104", "qw745856")
collection = db.ifoodUser
follow = 'https://ifoodie.tw/api/follow/?limit={}&offset={}&rtn_type=user&target_user_id={}'
collect = 'https://ifoodie.tw/api/collection/?all=true&user_id={}'
restaurant = 'https://ifoodie.tw/api/collection/{}/blogs/?limit={}&offset={}'


def extract(d):
    d['_id'] = d['id']
    d.pop('id', None)
    d.pop('profile_pic', None)
    d.pop('thumb', None)
    d.pop('cover_url', None)
    d.pop('profile_pic_origin', None)

for i in r:
    extract(i)
    track = []
    x = 0
    while True:
        followList = follow.format(x+300, x, i['_id'])
        followRes = requests.get(followList, verify=False, headers=head)
        jdFollow = json.loads(followRes.text, encoding='unicode')
        rf = jdFollow['response']
        for rfi in rf:
            track.append(rfi['id'])
        if len(rf) < 300:
            break
        x += 300
    i['follow'] = track
    collectionList = collect.format(i['_id'])
    collectRes = requests.get(collectionList, verify=False, headers=head)
    jdCollection = json.loads(collectRes.text, encoding='unicode')
    rc = jdCollection['response']
    for j in xrange(0,3):
        restList = []
        x = 0
        while True:
            restReq = restaurant.format(rc[j]['id'], x+300, x)
            restRes = requests.get(restReq, verify=False, headers=head)
            jdRestaurant = json.loads(restRes.text, encoding='unicode')
            rr = jdRestaurant['response']
            for rri in rr:
                restDict = {}
                try:
                    restDict['city'] = rri['restaurant']['city']
                    restDict['name'] = rri['restaurant']['name']
                    restDict['address'] = rri['restaurant']['address']
                    restDict['lat'] = rri['restaurant']['lat']
                    restDict['lng'] = rri['restaurant']['lng']
                    restDict['id'] = rri['restaurant']['id']
                    restList.append(restDict)
                except:
                    print "Null"
            if len(rr) < 300:
                break
            x += 300
        if j == 0:
            i['collection'] = copy.deepcopy(restList)
        elif j == 1:
            i['recommendation'] = copy.deepcopy(restList)
        elif j == 2:
            i['visit'] = copy.deepcopy(restList)
    try:
        collection.insert(i)
    except:
        print 'Duplicate Element'
end = time.time()
print end - start
    # dic = {}
    # arr = []
    # for u in r:
    #    dic['name'] = u['display_name']
    #    arr.append(dic)
    # with open('ifood.json','w') as f:
    # json.dump(jd,f)
