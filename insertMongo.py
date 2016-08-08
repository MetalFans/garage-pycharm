# -*- coding: utf-8 -*-
import json
from pymongo import MongoClient
offset = 5
limit = 0
with open('/Workspace/data/user/ifoodUsers_%d.json' % (offset+limit), 'r') as f:
    userjd = json.load(f)
with open('/Workspace/data/restaurant/ifoodRestaurant_%d.json' % (offset+limit), 'r') as f:
    restjd = json.load(f)
with open('/Workspace/data/blog/ifoodBlog_%d.json' % (offset+limit), 'r') as f:
    blogjd = json.load(f)
connection = MongoClient("ds015962.mlab.com", 15962)
db = connection["hellomongo"]
db.authenticate("ab101", "1234")
users = db.ifoodUser
for u in userjd['user']:
    try:
        users.insert(u)
    except:
        print "duplicate user_id"
restaurants = db.ifoodRestaurant
for r in restjd['restaurant']:
    try:
        restaurants.insert(r)
    except:
        print "duplicate restaurant_id"
blogs = db.ifoodBlog
for b in blogjd['blog']:
    try:
        blogs.insert(b)
    except:
        print "duplicate blog_id"
connection.close()