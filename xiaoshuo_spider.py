# -*- coding: utf-8 -*-

from __future__ import print_function

import requests
from bs4 import BeautifulSoup
import re
import time
import os
from collections import OrderedDict
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

headers = {
   'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
   ' Chrome/32.0.1700.76 Safari/537.36'
}

def get_title_url_map(start_url):
    global headers
    html = requests.get(start_url, headers=headers, timeout=45).text
    soup = BeautifulSoup(html)
    book_detail = soup.find_all(id='book_detail')[1]
    title_url_map = OrderedDict()
    li_list = book_detail.find('ol').find_all('li')
    
    for li in li_list:
        title = li.a.get_text().decode('utf-8')
        print('title is ', title)
        title_url_map[title] = li.a['href']
    
    return title_url_map

def get_content(xiaoshuo_url):
    global headers
    try:
        html = requests.get(xiaoshuo_url, headers=headers, timeout=45).content
        soup = BeautifulSoup(html)
        content = soup.find(id='content')
        text = ''
        for p in content.find_all('p'):
            text += p.text + '\n\n'
    except Exception as e:
        print('exception: ', str(e))
        return None
    else:
        return text    

if __name__=='__main__':
    start_url = 'http://www.136book.com/huaqiangu/'  # 花千骨 小说起始页
    start_url = 'http://www.136book.com/fanyiguan-1/'
    title_url_map = get_title_url_map(start_url)
    
    for title, url in title_url_map.iteritems():
        file_name = './xiaoshuo/' + title + '.txt'
        content = get_content(url)
        if content is None:
            continue
        with open(file_name, 'w') as f:
            f.write(content)
        print('title is ', title) #.decode('utf-8')
        
    print('end of operation')

    

    
    
    

