# -*- coding: utf-8 -*-
import requests
import json
from bs4 import BeautifulSoup
import random

url = 'http://www.proxynova.com/proxy-server-list/country-tw/'
res = requests.get(url)
soup = BeautifulSoup(res.text,'html.parser')
print soup.text