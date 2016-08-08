# -*- coding: utf-8 -*-
import requests
import json
import time
import copy
import os
from requests.adapters import HTTPAdapter

start = time.time()
head = {
    'User-Agent': 'ai shi ji/5.2.0 (iPhone; iOS 9.3.1; Scale/2.00)'
}

url = 'https://ifoodie.tw/api/user/{}' #user主頁
follow = 'https://ifoodie.tw/api/follow/?limit={}&offset={}&rtn_type=user&target_user_id={}' #粉絲名單
collect = 'https://ifoodie.tw/api/collection/?all=true&user_id={}' #收藏頁面
restaurant = 'https://ifoodie.tw/api/collection/{}/blogs/?limit={}&offset={}' #收藏/推薦/到訪
blog = 'https://ifoodie.tw/api/user/{}/blogs/?limit={}&offset={}' #文章列表
if not os.path.exists('./Workspace/data/user'):
    os.makedirs('./Workspace/data/user')
if not os.path.exists('./Workspace/data/restaurant'):
    os.makedirs('./Workspace/data/restaurant')
if not os.path.exists('./Workspace/data/blog'):
    os.makedirs('./Workspace/data/blog')
if not os.path.exists('./Workspace/log'):
    os.makedirs('./Workspace/log')
rs = requests.session()
rs.mount('https://', HTTPAdapter(max_retries=3)) #設定重試數量

# 丟掉不要的使用者資訊
def extract(d):
    d['_id'] = d['id']
    d.pop('id', None)
    d.pop('thumb', None)
    d.pop('cover_url', None)
    d.pop('profile_pic_origin', None)
    d.pop('is_following', None)

def createLog(log, type):
    date = time.strftime('%Y%m%d')
    with open('./Workspace/log/%s_%s.txt' % (type, date), 'a') as f:
        f.write(log+'\n')

with open('./Workspace/data/userlist.json','r') as f:
    userJson = json.load(f)

beginIndex = 0 #起始點
endIndex = 1000 #結束點
users = userJson['users'][beginIndex:endIndex] #抓取範圍
user = {} #最後要輸出的user json
response = [] #各個user字典檔的存放位置
restat = {} #最後要輸出的餐廳 json
restList = [] #各餐廳字典檔的存放位置
blogInfo = {} #最後要輸出的blog json
blogs = [] #各blog字典檔的存放位置
for u in users: #進去各個user頁面
    try:
        res = rs.get(url.format(u), headers=head)
        jd = json.loads(res.text, encoding='utf8')
        i = jd['response'] #取得user基本資料
        extract(i) # 丟掉不要的使用者資訊
        track = []
        x = 0
        while True: #持續翻頁取得粉絲名單
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
                createLog(i['_id'], 'user_follower')

            if len(rf) < 300: #最後一頁中斷迴圈
                break
            x += 300
        i['follow'] = track #保存粉絲清單
        x = 0
        blogID = []
        while True: #持續翻頁取得文章清單
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
                        blogID.append(blogDict['_id'])
                        blogs.append(blogDict)
                        rbi['restaurant']['_id'] = rbi['restaurant']['id']
                        rbi['restaurant']['timestamp'] = time.time()
                        rbi['restaurant'].pop('id', None)
                        if rbi['restaurant']['_id'] not in [ele['_id'] for ele in restList]:
                            restList.append(rbi['restaurant'])
                            print 'restaurant from blog'
                    except:
                        print "no restaurant data", rbi['title']
            except:
                print "no response"
                createLog(i['_id'], 'user_blog')
            if len(rb) < 300:
                break
            x += 300
        i['blog'] = copy.deepcopy(blogID)
        collectionList = collect.format(i['_id'])
        try: #進入個人收藏頁面
            collectRes = rs.get(collectionList, headers=head)
            jdCollection = json.loads(collectRes.text, encoding='utf8')
            rc = jdCollection['response']
            for j in xrange(0, 3): #抓收藏/推薦/到訪
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
                                if rri['restaurant']['_id'] not in [ele['_id'] for ele in restList]:
                                    restList.append(rri['restaurant'])
                                    print 'restaurant from collection'
                            except:
                                print "no restaurant data", rri['title']
                    except:
                        print "no response"
                        createLog(rc[j]['id'], 'collection')
                    if len(rr) < 300:
                        break
                    x += 300
                if j == 0:
                    i['collection'] = copy.deepcopy(c)  #存收藏
                elif j == 1:
                    i['recommendation'] = copy.deepcopy(c)  #存推薦
                elif j == 2:
                    i['visit'] = copy.deepcopy(c)  #存到訪
            i['timestamp'] = time.time()
            response.append(i)
            print '%d users in the house' % len(response)
        except:
            print "no response"
    except:
        print "no response"
        createLog(u, 'user')
user['user'] = response
restat['restaurant'] = restList
blogInfo['blog'] = blogs
try:
    with open('./Workspace/data/user/ifoodUsers_%d_%d.json' % (beginIndex, endIndex), 'w') as f:
        json.dump(user, f)
    with open('./Workspace/data/restaurant/ifoodRestaurant_%d_%d.json' % (beginIndex, endIndex), 'w') as f:
        json.dump(restat, f)
    with open('./Workspace/data/blog/ifoodBlog_%d_%d.json' % (beginIndex, endIndex), 'w') as f:
        json.dump(blogInfo, f)
except:
    print 'Failed'
end = time.time()
print end - start
