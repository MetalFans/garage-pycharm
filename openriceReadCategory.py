import json
with open('./Workspace/data/openrice.json', 'r') as f:
    jd = json.load(f)['refineSearchFilter']
with open('./Workspace/data/cuisines.txt', 'w') as f:
    for c in jd['cuisines']:
        f.write(c['name'].encode('utf-8')+'\n')
with open('./Workspace/data/dishes.txt', 'w') as f:
    for d in jd['dishes']:
        f.write(d['name'].encode('utf-8')+'\n')
with open('./Workspace/data/amenities.txt', 'w') as f:
    for a in jd['amenities']:
        f.write(a['name'].encode('utf-8')+'\n')