import sys
import pymongo
from pymongo import MongoClient
import json
#connection = MongoClient("ds015962.mlab.com", 15962)
connection = MongoClient("localhost", 27017)
db = connection["userdata"]
# MongoLab has user authentication
db.authenticate("ab101", "1234")

network = db.network100
network.insert_many(r);