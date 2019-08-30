# -*- coding:utf-8 -*-
import requests
from urllib.parse import urlencode
from requests.exceptions import RequestException
import json
from bs4 import BeautifulSoup
import re
import time
import os
from hashlib import md5

def get_page_index(offset,keyword):
    data = {
       # 'aid': 24,
        'app_name': 'web_search',
        'offset': offset,
        'format': 'json',
        'keyword': keyword,
        'autoload': 'true',
        'count': '20',
        #'en_qc': 1,
        'cur_tab': 3,
        #'from': 'search_tab',
        #'pd': 'synthesis',
       # 'timestamp': round(time.time())
    }
    url = 'https://www.toutiao.com/api/search/content/?' + urlencode(data)
    cookies = 'tt_webid=6719373825982760459; WEATHER_CITY=%E5%8C%97%E4%BA%AC; tt_webid=6719373825982760459; csrftoken=137c479d8a79bd6b3318b11c35c1c5f9; uuid="w:aa11850ca14243eea2c55397cc80252d"; UM_distinctid=16c420bec56b58-0fb0bc75873842-b781636-e1000-16c420bec5741a; s_v_web_id=8b6dd4717f71f4dd0cedf3f30812f7a7; __tasessionId=rpw3sw1l51564565389972; CNZZDATA1259612802=1420281822-1564470925-https%253A%252F%252Fwww.toutiao.com%252F%7C1564562726'
    proxies = {
        'http': 'http://120.83.104.195:9999'
    }
    headers={
        'User-Agent':"Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
        'Cookie': cookies
    }
    # headers={
    #     'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    # }
    try:
        response = requests.get(url, headers=headers, proxies=proxies)
        if response.status_code == 200:
            return response.text
        return 'No connection'
    except RequestException:
        print('error in get index.')
        return None

def parse_page_index(html):
    data = json.loads(html)
    if data and 'data' in data.keys():
        for item in data.get('data'):
            if 'image_list' in item.keys():

                yield item.get('article_url')

def get_page_detail(url):
    cookies = 'tt_webid=6719373825982760459; WEATHER_CITY=%E5%8C%97%E4%BA%AC; tt_webid=6719373825982760459; csrftoken=137c479d8a79bd6b3318b11c35c1c5f9; uuid="w:aa11850ca14243eea2c55397cc80252d"; UM_distinctid=16c420bec56b58-0fb0bc75873842-b781636-e1000-16c420bec5741a; s_v_web_id=8b6dd4717f71f4dd0cedf3f30812f7a7; __tasessionId=rpw3sw1l51564565389972; CNZZDATA1259612802=1420281822-1564470925-https%253A%252F%252Fwww.toutiao.com%252F%7C1564562726'
    proxies = {
        'http': 'http://120.83.104.195:9999'
    }
    headers={
        'User-Agent':"Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
        'Cookie': cookies
    }
    try:
        response = requests.get(url, headers=headers, proxies=proxies)#,cookies=cookies)
        if response.status_code == 200:
            return response.text
        return 'No connection'
    except RequestException:
        print('error in get detail.',url)
        return None

def parse_page_detail(html, url):
    soup = BeautifulSoup(html, 'lxml')#.encode('utf-8')
    title = soup.select('title')[0].get_text()
    print(title)
    image_pattern = re.compile('gallery: .*?parse(.*?)sibling',re.S)
    result = re.search(image_pattern, html)
    if result:
        #print(result.group(1))
        data = result.group(1).strip()[2:-3:].replace('\\', '')
        print(data)

        data = json.loads(data)
        if data and 'sub_images' in data.keys():
            sub_images = data.get('sub_images')
            images = [item.get('url') for item in sub_images]
            images2 = []
            for image in images:
                image = image.replace('u002F', '/')
                images2.append(image)
            # for image in images2:

            return{
                'title' : title,
                'url'   : url,
                'images': images2
            }
        # else:
        #     return 'No sub_images'
    # else:
    #     return 'No gallery'
    # print(soup)
# http://p3.pstatp.com/origin/pgc-image/2d89f47609c341fd9dab38fb788774b1

def save_image(content):
    file_path = '{0}/{1}.{2}'.format(os.getcwd(), md5(content).hexdigest(), 'jpg')
    if not os.path.exists(file_path):
        with open(file_path, 'wb') as f:
            f.write(content)

def download_image(url):
    cookies = 'tt_webid=6719373825982760459; WEATHER_CITY=%E5%8C%97%E4%BA%AC; tt_webid=6719373825982760459; csrftoken=137c479d8a79bd6b3318b11c35c1c5f9; uuid="w:aa11850ca14243eea2c55397cc80252d"; UM_distinctid=16c420bec56b58-0fb0bc75873842-b781636-e1000-16c420bec5741a; s_v_web_id=8b6dd4717f71f4dd0cedf3f30812f7a7; __tasessionId=rpw3sw1l51564565389972; CNZZDATA1259612802=1420281822-1564470925-https%253A%252F%252Fwww.toutiao.com%252F%7C1564562726'
    proxies = {
        'http': 'http://120.83.104.195:9999'
    }
    headers={
        'User-Agent':"Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
        'Cookie': cookies
    }
    # headers={
    #     'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    # }
    try:
        response = requests.get(url, headers=headers,proxies=proxies)
        if response.status_code == 200:
            save_image(response.content)
        return 'No pic connection'
    except RequestException:
        print('error in get pic.',url)
        return None

def main(offset, keyword):
    html = get_page_index(offset, keyword).encode('utf-8')
    #parse_page_index(html)
    for url in parse_page_index(html):
        #print(url)
        html = get_page_detail(url)
        if html:
            result = parse_page_detail(html, url)
            print(result)
            if result:
                print('now in {}'.format(result['title']))
                for image in result['images']:
                    download_image(image)


                # for image in result.get(images)


    #parse_page_index(html)

if __name__ == '__main__':
    for i in range(0,10,10):
        print('offset=', i)
        main(i, '街拍')

