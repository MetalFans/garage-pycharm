import re
import requests
import time
import math
from bs4 import BeautifulSoup as bs
import os
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

urlList = []

domain = 'http://tw.openrice.com'
rs = requests.session()
rs.headers.update({
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
    })

def getRivewURL(rs, u):
    res = rs.get(u)
    soup = bs(res.text, 'html.parser')
    review = domain + soup.select('.main-menu.table-center li')[1].select('a')[0]['href']
    number = soup.select('.main-menu.table-center li')[1].select('a')[0].text
    count = int(re.search('(\d+)', number).group(1))
    page = int(math.ceil(count / 15.0))
    return (review, page, count)


def getContent(u, p):
    result = []
    driver = webdriver.Firefox()
    url = u
    driver.get(url)
    for i in xrange(1,p+1):
        element = WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".js-layout-option.full"))
        )
        res =  driver.page_source.encode('utf-8')
        soup = bs(res, 'html.parser')
        n = len(soup.select('.middle-header'))
        time.sleep(0.5)
        driver.find_element_by_css_selector(".js-layout-option.full").click()
        res = driver.page_source
        soup = bs(res, 'html.parser')
        for t in soup.select('.review-container'):
            temp = re.sub('<img.*>','',t.text)
            s = "".join(temp.split()).strip()
            result.append(s)
        if i < p:
            nextpage = driver.find_element_by_css_selector(".pagination-button.next.js-next")
            nextpage.click()
        else:
            driver.quit()
    return result


def getall(u):
    st = []
    review = getRivewURL(rs, u)
    st.extend(getContent(review[0],review[1]))
    return st

text = []
for ul in urlList:
    text.extend(getall(ul))






