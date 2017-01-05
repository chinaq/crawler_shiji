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
    driver.set_page_load_timeout(10)


def loadpage(num):
    global driver
    try:
        url = "http://www.ikanman.com/comic/11314/115077.html#p=" + str(num)
        print(url)
        driver.get(url)
    except TimeoutException:  
        print('time out after XX seconds when loading page')
        driver.execute_script('window.stop()') # 当页面加载时间超过设定时间，通过执行Javascript来stop加载，即可执行后续动作
    finally:
        loadimg(num)

def loadimg(num):
    global driver
    try:
        element = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.ID, "mangaFile")))
    finally:        
        getSave(num)

def getSave(num):
    global driver
    # imgSrc = driver.find_element_by_id('mangaFile').get_attribute("src") + ".webp"
    imgSrc = driver.find_element_by_id('mangaFile').get_attribute("src")
    print(imgSrc)
    r = requests.get(imgSrc, stream=True, \
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36", \
        "Referer": "http://www.ikanman.com/comic/11314/115077.html"})
    if r.status_code == 200:
        with open("shiji/s1/" + str(num) + ".jpg", 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
    print("status code: " + str(r.status_code))

def close():
    global driver
    driver.close()


def main():
    for i in range(1, 138):
        init()
        loadpage(i)
        close()

# start
main()