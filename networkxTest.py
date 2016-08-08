import networkx as nx
import os
import re
import json


def readData(path,key):
    data = {}
    for fname in os.listdir(path):
        if re.search('.*ifood.*',fname):
            with open(path+'/'+fname, 'r') as f:
                jd = json.load(f)[key]
                for ele in jd:
                    if ele['_id'] not in data:
                        data[ele['_id']] = ele
                    elif ele['timestamp'] > data[ele['_id']]['timestamp']:
                        data[ele['_id']] = ele
    return data


path = '/Users/fan/PycharmProjects/ETL/GuoWeiShiuan20161523/data/270000_280000/user'
key = 'user'
user = readData(path, key)
dg = nx.DiGraph()
for id in user:
    dg.add_node(id)
    for fid in user[id]['fans_id_list']:
        if user.get(fid):
            dg.add_weighted_edges_from([(fid, id, user[fid]['follower_cnt'])])
indg = dg.in_degree(weight='weight')
outdg = dg.in_degree(weight='weight')
#indg = dg.in_degree()
#outdg = dg.in_degree()
[dg.remove_node(ele) for ele in indg if indg[ele] < 100]
pos = nx.spring_layout(dg)
nx.draw(dg, pos, node_size=1)



