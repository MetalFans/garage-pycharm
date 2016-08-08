import requests
import time
start = time.time()
head = {
    'User-Agent': 'ai shi ji/5.2.0 (iPhone; iOS 9.3.1; Scale/2.00)User-Agent: ai shi ji/5.2.0 (iPhone; iOS 9.3.1; Scale/2.00)'
}
urls = [
    'http://www.heroku.com',
    'http://python-tablib.org',
    'http://httpbin.org',
    'http://python-requests.org',
    'http://www.heroku.com',
    'http://python-tablib.org',
    'http://httpbin.org',
    'http://python-requests.org',
    'http://www.heroku.com',
    'http://python-tablib.org',
    'http://httpbin.org',
    'http://python-requests.org',
    'http://www.heroku.com',
    'http://python-tablib.org',
    'http://httpbin.org',
    'http://python-requests.org',
    'http://kennethreitz.com'
]
for u in urls:
    r = requests.get(u,headers=head)
    print r.text
end = time.time()
print end-start
