import eventlet
import requests
import grequests
import time
start = time.time()
pool = eventlet.GreenPool(20)
url = 'http://httpbin.org/get'
for i in xrange(0,20):
    pool.spawn_n(requests)
end = time.time()
print end-start