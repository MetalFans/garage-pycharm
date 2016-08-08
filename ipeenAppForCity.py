import requests
payload = {
    'api':'NEARBY_SHOP_SEARCH',
    'channel_id':'1',
    'cities':'6',
    'device_id':'',
    'lat':'25.037531',
    'lng':'121.5639969',
    'p':'1',
    'sort':'0',
    'token':''
}
url = 'https://www.ipeen.com.tw/touch/api/appService.php'
res = requests.post(url, data=payload, verify=False)
print res.text