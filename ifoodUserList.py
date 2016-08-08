import requests
import json
import time
import copy
import os
from requests.adapters import HTTPAdapter

start = time.time()
head = {
    'User-Agent': 'ai shi ji/5.2.0 (iPhone; iOS 9.3.1; Scale/2.00)User-Agent: ai shi ji/5.2.0 (iPhone; iOS 9.3.1; Scale/2.00)'
}

url = 'https://ifoodie.tw/api/user/{}'
follow = 'https://ifoodie.tw/api/follow/?limit={}&offset={}&rtn_type=user&target_user_id={}'
collect = 'https://ifoodie.tw/api/collection/?all=true&user_id={}'
restaurant = 'https://ifoodie.tw/api/collection/{}/blogs/?limit={}&offset={}'
blog = 'https://ifoodie.tw/api/user/{}/blogs/?limit={}&offset={}'
if not os.path.exists('/Workspace/data/user'):
    os.makedirs('/Workspace/data/user')
if not os.path.exists('/Workspace/data/restaurant'):
    os.makedirs('/Workspace/data/restaurant')
if not os.path.exists('/Workspace/data/blog'):
    os.makedirs('/Workspace/data/blog')
rs = requests.session()
rs.mount('https://', HTTPAdapter(max_retries=3))


def extract(d):
    d['_id'] = d['id']
    d.pop('id', None)
    d.pop('thumb', None)
    d.pop('cover_url', None)
    d.pop('profile_pic_origin', None)

with open('/Workspace/data/userlist.json','r') as f:
    userJson = json.load(f)
users = userJson['users']
user = {}
response = []
restat = {}
restList = []
blogInfo = {}
blogs = []
for u in users:
    res = rs.get(url.format(u), headers=head)
    jd = json.loads(res.text, encoding='utf8')
    i = jd['response']
    extract(i)
    track = []
    x = 0
    while True:
        rf = []
        try:
            followList = follow.format(x+300, x, i['_id'])
            followRes = rs.get(followList, headers=head)
            jdFollow = json.loads(followRes.text, encoding='utf8')
            rf = jdFollow['response']
            for rfi in rf:
                track.append(rfi['id'])
        except:
            print "no response"
        if len(rf) < 300:
            break
        x += 300
    i['follow'] = track
    x = 0
    blogID = []
    while True:
        rb = []
        try:
            blogList = blog.format(i['_id'], x+300, x)
            blogRes = rs.get(blogList, headers=head)
            jdBlog = json.loads(blogRes.text, encoding='utf8')
            rb = jdBlog['response']
            for rbi in rb:
                blogDict = {}
                try:
                    blogDict['_id'] = rbi['id']
                    blogDict['timestamp'] = time.time()
                    blogDict['date'] = rbi['date']
                    blogDict['url'] = rbi['url']
                    blogDict['title'] = rbi['title']
                    blogDict['is_paid'] = rbi['is_paid']
                    blogDict['blog_type'] = rbi['url'].split('/')[2]
                    blogDict['browse_cnt'] = rbi['stat']['browse_cnt']
                    blogDict['favorite_cnt'] = rbi['stat']['favorite_cnt']
                    blogDict['share_cnt'] = rbi['stat']['share_cnt']
                    blogDict['recommend_cnt'] = rbi['stat']['recommend_cnt']
                    blogDict['restaurant_id'] = rbi['restaurant']['id']
                    blogID.append(blogDict['restaurant_id'])
                    blogs.append(blogDict)
                except:
                    print "no restaurant data", rbi['title']
        except:
            print "no response"
        if len(rb) < 300:
            break
        x += 300
    i['blog'] = copy.deepcopy(blogID)
    collectionList = collect.format(i['_id'])
    try:
        collectRes = rs.get(collectionList, headers=head)
        jdCollection = json.loads(collectRes.text, encoding='utf8')
        rc = jdCollection['response']
        for j in xrange(0, 3):
            idList = []
            x = 0
            c = []
            while True:
                rr = []
                try:
                    restReq = restaurant.format(rc[j]['id'], x+300, x)
                    restRes = rs.get(restReq, headers=head)
                    jdRestaurant = json.loads(restRes.text, encoding='utf8')
                    rr = jdRestaurant['response']
                    for rri in rr:
                        try:
                            rri['restaurant']['_id'] = rri['restaurant']['id']
                            rri['restaurant']['timestamp'] = time.time()
                            rri['restaurant'].pop('id', None)
                            c.append(rri['restaurant']['_id'])
                            restList.append(rri['restaurant'])
                        except:
                            print "no restaurant data", rri['title']
                except:
                    print "no response"
                if len(rr) < 300:
                    break
                x += 300
            if j == 0:
                i['collection'] = copy.deepcopy(c)
            elif j == 1:
                i['recommendation'] = copy.deepcopy(c)
            elif j == 2:
                i['visit'] = copy.deepcopy(c)
        i['timestamp'] = time.time()
        response.append(i)
        print '%d users in the house' % len(response)
    except:
        print "no response"
user['user'] = response
restat['restaurant'] = restList
blogInfo['blog'] = blogs
try:
    with open('/Workspace/data/user/ifoodUsers_%d.json' % len(users), 'w') as f:
        json.dump(user, f)
    with open('/Workspace/data/restaurant/ifoodRestaurant_%d.json' % len(users), 'w') as f:
        json.dump(restat, f)
    with open('/Workspace/data/blog/ifoodBlog_%d.json' % len(users), 'w') as f:
        json.dump(blogInfo, f)
except:
    print 'Failed'
end = time.time()
print end - start
