# -*- coding: utf-8 -*-
from __future__ import print_function

import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup 
import urllib
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
import pprint

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

headers = {
    'Accept': 'text/javascript, text/html, application/xml, text/xml, */*',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
}

#headers = {
#    'Accept': 'text/javascript, text/html, application/xml, text/xml, */*',
#    'Accept-Encoding': 'gzip, deflate',
#    'Accept-Language': 'zh-CN,zh;q=0.8',
#    'Content-Type': 'application/x-www-form-urlencoded',
#    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
#    'referer': 'https://www.lagou.com/jobs/list_%E6%9C%BA%E5%99%A8%E5%AD%A6%E4%B9%A0?labelWords=&fromSearch=true&suginput=',
#    'X-Anit-Forge-Code': '0',
#    'X-Anit-Forge-Token': 'None',
#    'X-Requested-With': 'XMLHttpRequest',
#    'Cookie': 'user_trace_token=20170912201213-09228d89-2962-45d8-a915-5005559ee5fb; LGUID=20170912201214-9d07ff59-97b3-11e7-9168-5254005c3644; X_HTTP_TOKEN=f5e95edcbf2a1be96a7fd41c54770f6e; witkey_login_authToken="Es4VFc9tCRfrXwegii/KXN0dXGhRzASqCgXlI76jcfS1RuQNCc4upBIMUZb7XXZWbqy3dFhBeVlO+7DhOHf3ffFhGZt5SpgGkkBmZ9M92HFPcg0yppb2cyfDjLJvH6L1mmOu5zxBk3EndkZF0210r9RLi99f7Es6cAqEugcqKmB4rucJXOpldXhUiavxhcCELWDotJ+bmNVwmAvQCptcy5e7czUcjiQC32Lco44BMYXrQ+AIOfEccJKHpj0vJ+ngq/27aqj1hWq8tEPFFjdnxMSfKgAnjbIEAX3F9CIW8BSiMHYmPBt7FDDY0CCVFICHr2dp5gQVGvhfbqg7VzvNsw=="; JSESSIONID=ABAAABAABEEAAJAE6A679B15293A0C478219C6874A7E3C3; PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; _putrc=EE0DDE02D8CF828E; login=true; unick=%E6%B6%82%E6%9D%BE%E9%AB%98; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=0; TG-TRACK-CODE=search_code; SEARCH_ID=cdf610d2454d47efa4016905621733c3; index_location_city=%E5%85%A8%E5%9B%BD; _gid=GA1.2.412706642.1508718279; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1508031899,1508157502,1508755371,1508755385; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1509022165; _ga=GA1.2.144406653.1505218340; LGSID=20171026203706-603d7fcc-ba4a-11e7-9626-5254005c3644; LGRID=20171026204908-0e70fa02-ba4c-11e7-a945-525400f775ce',
#}


def get_lagou_jobinfo_url(page_num, keyword, city_name):
    headers = {
        'Accept': 'text/javascript, text/html, application/xml, text/xml, */*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        'referer': 'https://www.lagou.com/jobs/list_%E6%9C%BA%E5%99%A8%E5%AD%A6%E4%B9%A0?labelWords=&fromSearch=true&suginput=',
        'X-Anit-Forge-Code': '0',
        'X-Anit-Forge-Token': 'None',
        'X-Requested-With': 'XMLHttpRequest',
        'Cookie': 'user_trace_token=20170912201213-09228d89-2962-45d8-a915-5005559ee5fb; LGUID=20170912201214-9d07ff59-97b3-11e7-9168-5254005c3644; X_HTTP_TOKEN=f5e95edcbf2a1be96a7fd41c54770f6e; witkey_login_authToken="Es4VFc9tCRfrXwegii/KXN0dXGhRzASqCgXlI76jcfS1RuQNCc4upBIMUZb7XXZWbqy3dFhBeVlO+7DhOHf3ffFhGZt5SpgGkkBmZ9M92HFPcg0yppb2cyfDjLJvH6L1mmOu5zxBk3EndkZF0210r9RLi99f7Es6cAqEugcqKmB4rucJXOpldXhUiavxhcCELWDotJ+bmNVwmAvQCptcy5e7czUcjiQC32Lco44BMYXrQ+AIOfEccJKHpj0vJ+ngq/27aqj1hWq8tEPFFjdnxMSfKgAnjbIEAX3F9CIW8BSiMHYmPBt7FDDY0CCVFICHr2dp5gQVGvhfbqg7VzvNsw=="; JSESSIONID=ABAAABAABEEAAJAE6A679B15293A0C478219C6874A7E3C3; PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; _putrc=EE0DDE02D8CF828E; login=true; unick=%E6%B6%82%E6%9D%BE%E9%AB%98; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=0; TG-TRACK-CODE=search_code; SEARCH_ID=cdf610d2454d47efa4016905621733c3; index_location_city=%E5%85%A8%E5%9B%BD; _gid=GA1.2.412706642.1508718279; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1508031899,1508157502,1508755371,1508755385; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1509022165; _ga=GA1.2.144406653.1505218340; LGSID=20171026203706-603d7fcc-ba4a-11e7-9626-5254005c3644; LGRID=20171026204908-0e70fa02-ba4c-11e7-a945-525400f775ce',
    }
    start_url = 'https://www.lagou.com/jobs/positionAjax.json?'
    data = {
        'first': 'false',
        'pn': page_num,
        'kd': keyword,
        'city': city_name
    }
    start_url += urlencode(data)
    return start_url



def get_page_pic():
    start_url = 'http://tu.duowan.com/gallery/129003.html'
    res = requests.get(start_url, headers=headers)
#    res.encoding = 'ISO-8859-1'
    res.encoding = 'utf-8'
#    res.encoding = 'GBK'
#    res.encoding = 'gb2312'
    html = res.text
    soup = BeautifulSoup(html, 'lxml')
    print('soup beutify is ', soup.prettify())
    print('soup.title is ', soup.title.text)
    title = soup.select('div#currentview > h1')[0].text
    print('title is ', title)
    
#    <div class="title" id="currentview">
#			    <h1>深夜福利~诱惑阿狸</h1><span id="seq">(1/10)</span>
#			</div>
    
    

if __name__=='__main__':
    start_url = 'http://www.toutiao.com/a6480317867202970126/'
    start_url = 'http://www.toutiao.com/a6480454226370626062/#p=1'
    start_url = 'http://book.jd.com/booktop/0-0-0.html?category=1713-0-0-0-10001-1#comfort'
#    start_url = get_lagou_jobinfo_url(1, '机器学习', '广州')
    start_url = 'http://bj.xiaozhu.com/search-duanzufang-p2-0/'
    start_url = 'http://127.0.0.1:8000'
#    start_url = 'http://bj.xiaozhu.com/fangzi/5700411214.html'
    
    print('hello world.')
    
    res = requests.get(start_url, headers=headers)
    res.encoding = 'utf-8'

    html = res.text
    print('res.text is ', html)
    print('res.encoding is ', res.encoding)
    
#    get_page_pic()
    
    # href=\"http:\/\/tu.duowan.com\/gallery\/128811.html\" target=\"
    
#    soup = BeautifulSoup(html, 'lxml')
#    print('soup beutify is ', soup.prettify())
#    elements = soup.select('div.p-detail > a.p-name')
#    link_list = [res['href'] for res in elements]
#    print('result is ', link_list)

    soup = BeautifulSoup(html, 'lxml')
    print('soup.title is ', soup.title.text.strip())
#    print('soup beutify is ', soup.prettify())
#    print('soup.title is ', soup.title.text)
    elements = soup.select('a')
    price_list = [ele.text for ele in elements]
    for p in price_list:
        print('price_list is ', p)
        
#    print('locals() is ', locals())
#    print('len is ', len(link_list))
#    
#    for i, link in enumerate(link_list):
#        res = requests.get('http:'+link, headers=headers)
#        with open('./avatar/'+str(i)+'.png', 'wb') as f:
#            f.write(res.content)
        
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    


