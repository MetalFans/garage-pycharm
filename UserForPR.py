from pymongo import MongoClient
import json
import time
start = time.time()
connection = MongoClient("ds145415.mlab.com", 45415)
db = connection["ab101group4"]
db.authenticate("user", "1234")
#db.network.drop()
collection = db.network100
with open('/Users/fan/anaconda/bin/Workspace/result/UserForPR_V2.json', 'r') as f:
    userdata = json.load(f)
print len(userdata)
collection.insert_many(userdata.values())