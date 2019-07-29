# -*- coding:utf-8 -*-
import requests
from requests.exceptions import RequestException
import re
import json
from multiprocessing import Pool

def get_one_page(url):
    try:
        headers={
        'User-Agent':'Mozilla/5.0 (Macintosh; intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
        }
        response = requests.get(url,headers = headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


def parse_one_page(html):
    pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?title="(.*?)".*?data-src="(.*?)"'
                         +'.*?star">(.*?)</p>.*?releasetime">(.*?)</p>.*?integer">(.*?)</i>.*?'
                          +'fraction">(\d+)</i>.*?</dd>', re.S)
    items = re.findall(pattern,html)
    #print(items)
    for item in items:
        yield {
            'index':item[0],
            'title':item[1],
            'image':item[2],
            'stars':item[3].strip()[3:],
            'time':item[4][5:],
            'score':item[5]+item[6]
        }

def write_to_file(content):
    with open('result.txt','a') as f:
        f.write(json.dumps(content,ensure_ascii=False)+'\n')


def main(offset):
    url = 'https://maoyan.com/board/4?offset=' + str(offset)
    #print(url)
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)

if __name__ == '__main__':
    for offset in range(0,100,10):
        main(offset)
#multiprocess:
    # pool = Pool()
    # pool.map(main, [i*10 for i in range(10)])

