#! python3
# coding: utf-8

from selenium import webdriver
import time
import urllib  
import requests
import shutil
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


global driver

def init():
    global driver
    # options = [
    #     '--load-images=false',
    #     '--disk-cache=true']
    options = ['--load-images=false']
    driver = webdriver.PhantomJS(executable_path='phantomjs/bin/phantomjs', service_args=options)
    driver.set_page_load_timeout(1)


def loadpage(page):
    global driver
    try:
        url = "http://www.ikanman.com/comic/11314/115078.html#p=" + str(page)
        print(url)
        driver.get(url)
    except TimeoutException:  
        print('time out after XX seconds when loading page')
        # driver.execute_script('window.stop()') # 当页面加载时间超过设定时间，通过执行Javascript来stop加载，即可执行后续动作
    # finally:
    #     loadimg(page)

def loadimg():
    global driver
    try:
        element = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "mangaFile")))
    except TimeoutException:  
        print('time out after XX seconds when loading img src')
    # finally:        
    #     getSave(page)

def getSave(vol, page):
    global driver
    # imgSrc = driver.find_element_by_id('mangaFile').get_attribute("src") + ".webp"
    imgSrc = driver.find_element_by_id('mangaFile').get_attribute("src")
    print(imgSrc)
    r = requests.get(imgSrc, stream=True, \
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36", \
        "Referer": "http://www.ikanman.com/comic/11314/115077.html"})
    if r.status_code == 200:
        with open("shiji/卷" + str(vol) + "/" + str(page) + ".jpg", 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
    print("status code: " + str(r.status_code))

def close():
    global driver
    driver.close()


def main():
    for vol in range(1, 13):
        url = "http://www.ikanman.com/comic/11314/" + str(115076 + vol) + ".html"
        for page in range(1, 139):
            init()
            loadpage(page)
            loadimg()
            getSave(vol, page)
            close()

# start
main()