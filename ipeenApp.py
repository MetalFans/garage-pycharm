import requests
payload = {
    'api':'SHOP_SEARCH',
    'channel_id':'1',
    'device_id':'dba8243f758f7ea85b4fb308e835f4c9d867761ce9cc1fcee7265f98ebcb2e12',
    'p':'1',
    'sort':'0',
    'token':'',
    'district':'1',
    'lat':'25.037531',
    'lng':'121.5639969'
}
url = 'https://www.ipeen.com.tw/touch/api/appService.php'
res = requests.post(url, data=payload, verify=False)
print res.text