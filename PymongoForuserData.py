from pymongo import MongoClient
import json
import time
start = time.time()
#connection = MongoClient("0.tcp.ngrok.io", 17510)
connection = MongoClient("140.115.236.204", 27017)
#db = connection["userdata"]
#db.authenticate("ab101", "1234")
#collection = db.userinfo2


db = connection['user']

collectionName = db.users

with open('/Users/fan/anaconda/bin/Workspace/result/UserWithPredecessorsV2.json', 'r') as f:
    userdata = json.load(f)

collectionName.insert_many(userdata.values())

# for ele in userdata.values():
#     collection.update_one({
#       '_id': ele['_id']
#     },{
#       '$set':ele
#     }, upsert=False)
#
# print time.time()-start