# -*- coding:utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from pyquery import PyQuery as pq
import json

browser = webdriver.Chrome()
wait = WebDriverWait(browser, 10)
keyword = '笔记本'


def search():
    try:
        browser.get('https://jd.com')
        inp = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#key"))
        )
        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#search > div > div.form > button"))
        )
        inp.send_keys(keyword)
        submit.click()
        total = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#J_topPage > span > i"))
        )
        return total.text
    except TimeoutException:
        return search()


def next_page():
    try:
        submit = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#J_topPage > a.fp-next"))
            )
        submit.click()
        time.sleep(1)
    except TimeoutException:
        return next_page()


def get_detail():
    browser.maximize_window()
    time.sleep(0.05)
    for i in range(0, 100):
        time.sleep(0.05) # According to your network quality, you may neet to change this sleep time. 
        js = "window.scrollTo(0,%s)" % (i*100)
        browser.execute_script(js)

    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#J_goodsList > ul")))
    html = browser.page_source
    doc = pq(html)
    items = doc('#J_goodsList > ul .gl-item').items()
    for item in items:
        product = {
            'title': item.find('.p-name a em').text().replace('\n', ''),
            'image': 'https:' + item.find('.p-img img').attr('src'),
            'price': item.find('.p-price i').text()
        }
        #print(product)
        with open('{}.txt'.format(keyword), 'a') as f:
            f.write(json.dumps(product, ensure_ascii=False)+'\n')


def main():
    total = int(search())
    print(total)
    get_detail()
    for i in range(total):
        next_page()
        get_detail()


if __name__ == '__main__':
    main()
