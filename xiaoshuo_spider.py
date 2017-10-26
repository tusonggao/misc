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
   'User-Agent':
   'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.76 Safari/537.36'
}

def get_title_url_map(start_url):
    global headers
    html = requests.get(start_url, headers=headers, timeout=45).text
    soup = BeautifulSoup(html, 'lxml')
    link_list = soup.select('#book_detail > ol > li > a')
    title_url_map = OrderedDict()
    
    for link in link_list:
        title = link.text
        print('title is ', title)
        title_url_map[title] = link['href']
    
    return title_url_map

def get_content(xiaoshuo_url):
    global headers
    try:
        html = requests.get(xiaoshuo_url, headers=headers, timeout=45).text
        soup = BeautifulSoup(html, 'lxml')
        content_list = soup.select('p')
        text = ''
        for content in content_list:
            text += content.text + '\n\n'
    except Exception as e:
        print('exception: ', str(e))
        return None
    else:
        return text    

if __name__=='__main__':
    start_url = 'http://www.136book.com/huaqiangu/'  # 花千骨 小说起始页
#    start_url = 'http://www.136book.com/fanyiguan-1/'
#    title_url_map = get_title_url_map(start_url)
    
#    print('title_url_map is ', title_url_map)
    
    print('content is ', get_content('http://www.136book.com/huaqiangu/ebxeet/'))
    
#    for title, url in title_url_map.iteritems():
#        file_name = './xiaoshuo/' + title + '.txt'
#        content = get_content(url)
#        if content is None:
#            continue
#        with open(file_name, 'w') as f:
#            f.write(content)
#        print('title is ', title) #.decode('utf-8')
#        
#    print('end of operation')

    

    
    
    

