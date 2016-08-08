from ra import *
a = ReqAgent()
pr = a.g('http://httpbin.org/get')
response = a.send(pr)
print response.text