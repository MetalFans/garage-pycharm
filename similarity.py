# -*- coding: utf-8 -*-
import requests
import json
import time
import os
import difflib
import Levenshtein

start = time.time()

with open('/Users/fan/anaconda/bin/Workspace/data/openriceName.json', 'r') as f:
    openrice = json.load(f, encoding='utf8')

with open('/Users/fan/anaconda/bin/Workspace/data/ifoodName.json', 'r') as f:
    ifood = json.load(f, encoding='utf8')

for o in ifood:
    ifname =ifood[o].split('|')[0]
    ifaddress =ifood[o].split('|')[1]
    temp = {}
    for o in openrice:
        opname = openrice[o].split('|')[0]
        opaddress = openrice[o].split('|')[1]
        jw = Levenshtein.jaro_winkler(ifname, opname, 0.25)
        if jw not in temp:
            temp[jw] = '%s|%s' % (opname, opaddress)
        else:
            addressjw0 = Levenshtein.jaro(ifaddress, temp[jw].split('|')[1])
            addressjw1 = Levenshtein.jaro(ifaddress, opaddress)
            if addressjw1 > addressjw0:
                temp[jw] = '%s|%s' % (opname, opaddress)

    print '%s|%s' % (ifname, temp[max(temp.keys())].split('|')[0])
    print '%s|%s' % (ifaddress, temp[max(temp.keys())].split('|')[1])