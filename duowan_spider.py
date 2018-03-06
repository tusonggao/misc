# -*- coding: utf-8 -*-
from __future__ import print_function


import logging
from bs4 import BeautifulSoup 
import re
import time
import os
import sip
import PyQt4
import spynner
import json
from collections import OrderedDict
from urllib import urlencode
import requests

from sklearn import neighbors

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def get_page_pic(url_id):
    try:
        headers = {
            'Accept': 'text/javascript, text/html, application/xml, text/xml, */*',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        }
    
        start_url = 'http://tu.duowan.com/gallery/' + str(url_id) + '.html'
        res = requests.get(start_url, headers=headers, timeout=30)
        print('res.encoding is ', res.encoding)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, 'lxml')
        title = soup.select('div#currentview > h1')[0].text
        print('title is ', title)
        
        path = os.getcwd() + '/pic_duowan/'
        path = os.path.join(path, title)
        if not os.path.exists(path):
            os.mkdir(path)     # 创建文件夹
        
        start_url = 'http://tu.duowan.com/index.php?r=show/getByGallery/&gid=' + str(url_id)
        res = requests.get(start_url, headers=headers, timeout=30)
        pattern = re.compile('"url":"(http:\\\\/\\\\/[^"]+\.(png|jpg))"')
        results = re.findall(pattern, res.text)
        link_list = [res[0].replace('\\/', '/') for res in results]
        
        time.sleep(1)
        for i, link in enumerate(link_list):
            res = requests.get(link, headers=headers, timeout=30)
            with open(path + '/' + str(i) + '.jpg', 'wb') as f:
                f.write(res.content)
    except Exception as e:
        print('an exception occurs: ', str(e)) 
        
    
def get_duowan_url_id_list(number=30):
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'Cookie': 'Hm_lvt_d3da82191e5540a9e42feaba8dcfc9ac=1509065453; Hm_lpvt_d3da82191e5540a9e42feaba8dcfc9ac=1509065453; 20171027statistics=f6pxcyaiy9; hiido_ui=0.5352905765690372; hd_newui=0.07670915897426855; dw_mini_popup_status=0; da_ui=59f290f40333a6413; BA=l=89&le=3.88&ip=; hdjs_session_id=0.05558658178287468; Hm_lvt_66ee381f0140ac33122f0051eae9b401=1509065453; Hm_lpvt_66ee381f0140ac33122f0051eae9b401=1509082273; Hm_lvt_4941f2298273634934f789da00bbabe0=1509080585,1509080600,1509080606,1509081021; Hm_lpvt_4941f2298273634934f789da00bbabe0=1509082273; hdjs_session_time=1509082273531',
        'Host': 'tu.duowan.com',
        'Referer': 'http://tu.duowan.com/m/meinv',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }
    
    num = 30
    url_set = set()
    title_set = set()
    while True:    
        start_url = 'http://tu.duowan.com/m/meinv?offset=' + str(num) + '&order=created&math=0.574756804666471'
        res = requests.get(start_url, headers=headers)
        print('res.encoding is ', res.encoding)
        res.encoding = 'utf-8'
#        res.encoding = 'ISO-8859-1'
        html = res.text
#        soup = BeautifulSoup(html, 'lxml')
#        results = soup.select('em > a')
#        link_list = [res['href'].replace('\\/', '/')[2:-2] for res in results]
#        title_list = [res.text for res in results]
#        for title in title_list:
#            print('title is ', title)
#        url_set |= set(link_list)
#        title_set |= set(title_list)
# <em><a href=\"http:\/\/tu.duowan.com\/gallery\/134698.html\" target=\"_blank\">\u6027\u611f\u7684\u540c\u4eba\u963f\u72f8COS \u6839\u672c\u628a\u6301\u4e0d\u4f4f<\/a> 
        
        jjss = json.loads(html)
        html = jjss['html']
#        print('jjss.html is ', jjss['html'])
        pattern1 = re.compile('<em><a href="(http://tu\.duowan\.com/gallery/\d+\.html)"')
#        pattern1 = re.compile('<em><a href=\\\\"(http:\\\\/\\\\/tu\.duowan\.com\\\\/gallery\\\\/\d+\.html)\\\\"')
        results1 = re.findall(pattern1, html)
        print('results1 is ', results1)
        
        pattern2 = re.compile('<em><a href="http://tu\.duowan\.com/gallery/\d+\.html" target="_blank">(.*?)</a>')
        results2 = re.findall(pattern2, html)
        print('results2 is ', results2[:3])
#        title_list = [res.replace('\\\\u', '\\u') for res in results2[:3]]
        title_list = [res for res in results2[:3]]
        print('title_list is ', title_list)
        
        link_list = [res.replace('\\/', '/') for res in results1]
        url_set |= set(link_list)
        
        
#        pattern = re.compile('href=\\\\"(http:\\\\/\\\\/tu\.duowan\.com\\\\/gallery\\\\/\d+\.html)')
#        results = re.findall(pattern, html)
#        link_list = [res.replace('\\/', '/') for res in results]
#        url_set |= set(link_list)
#        print('len of urlset 1 is ', len(url_set))
        if len(url_set) >= number:
            break
        break
        num += 30
    
    
    url_id_list = [url.split('/')[-1].split('.')[0] for url in  url_set]
#    print('url_id_list is ', url_id_list)
#    print('title_set is ', title_set)
#    print('url_set is ', url_set)
    return url_id_list

if __name__=='__main__':
#    headers = {
#        'Accept': 'application/json, text/javascript, */*; q=0.01',
#        'Accept-Encoding': 'gzip, deflate',
#        'Accept-Language': 'zh-CN,zh;q=0.8',
#        'Connection': 'keep-alive',
#        'Cookie': 'Hm_lvt_d3da82191e5540a9e42feaba8dcfc9ac=1509065453; Hm_lpvt_d3da82191e5540a9e42feaba8dcfc9ac=1509065453; 20171027statistics=f6pxcyaiy9; hiido_ui=0.5352905765690372; hd_newui=0.07670915897426855; dw_mini_popup_status=0; da_ui=59f290f40333a6413; BA=l=89&le=3.88&ip=; hdjs_session_id=0.05558658178287468; Hm_lvt_66ee381f0140ac33122f0051eae9b401=1509065453; Hm_lpvt_66ee381f0140ac33122f0051eae9b401=1509082273; Hm_lvt_4941f2298273634934f789da00bbabe0=1509080585,1509080600,1509080606,1509081021; Hm_lpvt_4941f2298273634934f789da00bbabe0=1509082273; hdjs_session_time=1509082273531',
#        'Host': 'tu.duowan.com',
#        'Referer': 'http://tu.duowan.com/m/meinv',
#        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
#        'X-Requested-With': 'XMLHttpRequest'
#    }

    
    start_t = time.time()
    
#    start_url = 'http://tu.duowan.com/m/meinv?offset=300&order=created&math=0.574756804666471'
#    start_url = 'http://tu.duowan.com/m/meinv?offset=300&order=created&math=0.3565021552359482'

#    html = 'www.baidu.com/aiaitu/art.html wwww.baidu.com/cef.html aaa' 
#    BookID = str(re.search('com/(.*?)\.html', html).group(1))    
#    print(BookID)
#    
#    pattern = re.compile('com/(.*?)\.html')
#    results = re.findall(pattern, html)
#    print(results)
    
#    start_url = 'http://tu.duowan.com/index.php?r=show/getByGallery/&gid=129003'
    
#    res = requests.get(start_url, headers=headers)
#    res.encoding = 'gbk'
#    html = res.text
#    print('res.text is ', html)
    
    # "url":"http:\/\/s1.dwstatic.com\/group1\/M00\/56\/DB\/16b11563dcc2d2ac75e1c0d88f70d042.png",
#    pattern = re.compile('"url":"(http:\\\\/\\\\/[^"]+\.(png|jpg))"')
#    results = re.findall(pattern, html)
#    link_list = [res[0].replace('\\/', '/') for res in results]
#    print('result is ', link_list)
#    print('result is ', len(link_list))
    
#    print('res.encoding is ', res.encoding)
    
    id_list = get_duowan_url_id_list()
    
#    for i, pic_url_id in enumerate(id_list):
#        print('i is ', i)
#        get_page_pic(pic_url_id)
    
    end_t = time.time()
    print('get end of prog, cost time: ', (end_t - start_t))
        
    

    
