from selenium import webdriver
import sys

import time

def get(url,iteration=15,sleeptime=2):
    try:
        driver = webdriver.Chrome()
        driver.implicitly_wait(30)
        driver.get(url)
        for i in range(1, iteration):
            print ('Try scrolling =>'+str(i))
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(sleeptime)
        html_source = driver.page_source
        data = html_source.encode('utf-8')
        print ('Get data of size:'+len(data))
        return data
    except Exception as e:
        print(e)
        print ('Looks like driver not install , please donload the zip extact the executables an put into the path')
        sys.exit(0)

def test():
    get('https://www.myntra.com/men-tshirts?src=tNav', 20)
#test()
