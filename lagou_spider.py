# -*- coding: utf-8 -*-
from __future__ import print_function


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
from collections import OrderedDict
import requests

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

crawled_urls_set = set()


def make_dir(path_dir):
    cwd_path = os.getcwd()
    path = os.path.join(cwd_path, path_dir)
    if not os.path.exists(path):
        os.mkdir(path)                 #创建文件夹

def store_file(url_set, path):
    global headers, crawled_urls_set
    
    for url in url_set:
        print('crawling url ', url)
        if url in crawled_urls_set:
            print('already crawled url ', url)
            continue
        else:
            crawled_urls_set.add(url)
        file_number = url.split('/')[-1].split('.')[0]
        filename = path + os.sep + str(file_number) + '.html'
        try:
            content = requests.get(url, headers=headers, timeout=45).text
        except Exception as e:
            print('error occured ', str(e))
        else:
            with open(filename, 'w') as f:
                f.write(content)
                
        
def get_job_link(html):
    soup = BeautifulSoup(html, 'lxml')
    positions = soup.select('a.position_link')
    link_list = [pos['href'] for pos in positions]
    return link_list
    

def get_job_urls(start_url):
    global position_link_set
    driver = webdriver.Firefox()
    
    if isinstance(start_url, list)==False:
        start_url = [start_url]
    
    position_link_set = set()
    for url in start_url:
        driver.get(url)
        WebDriverWait(driver, 30)
        
        count = 0
        while count<=30:
            time.sleep(0.5)
            link_list = get_job_link(driver.page_source)
            position_link_set |= set(link_list)
            print('url_list_set length is {0} '.format(len(position_link_set)))
#            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);");  # 下拉到底部
            try:
                next_page = driver.find_element_by_class_name('pager_next')
                next_page.click()
            except Exception as e:
                print('Exception is ', str(e))
            count += 1
    
    driver.quit()
    return position_link_set


if __name__=='__main__':
    start_url1 = 'https://www.lagou.com/jobs/list_%E6%9C%BA%E5%99%A8%E5%AD%A6%E4%B9%A0?px=default&city=%E5%85%A8%E5%9B%BD' #机器学习
    start_url2 = 'https://www.lagou.com/jobs/list_%E6%95%B0%E6%8D%AE%E6%8C%96%E6%8E%98?city=%E5%85%A8%E5%9B%BD' #数据挖掘
    
       
#    headers = {
#        'Cookie':
#        'user_trace_token=20170912201213-09228d89-2962-45d8-a915-5005559ee5fb; LGUID=20170912201214-9d07ff59-97b3-11e7-9168-5254005c3644; X_HTTP_TOKEN=f5e95edcbf2a1be96a7fd41c54770f6e; witkey_login_authToken="Es4VFc9tCRfrXwegii/KXN0dXGhRzASqCgXlI76jcfS1RuQNCc4upBIMUZb7XXZWbqy3dFhBeVlO+7DhOHf3ffFhGZt5SpgGkkBmZ9M92HFPcg0yppb2cyfDjLJvH6L1mmOu5zxBk3EndkZF0210r9RLi99f7Es6cAqEugcqKmB4rucJXOpldXhUiavxhcCELWDotJ+bmNVwmAvQCptcy5e7czUcjiQC32Lco44BMYXrQ+AIOfEccJKHpj0vJ+ngq/27aqj1hWq8tEPFFjdnxMSfKgAnjbIEAX3F9CIW8BSiMHYmPBt7FDDY0CCVFICHr2dp5gQVGvhfbqg7VzvNsw=="; TG-TRACK-CODE=index_search; SEARCH_ID=f871fb519d1a400192aa0f26a8cd5d1e; index_location_city=%E5%85%A8%E5%9B%BD; JSESSIONID=ABAAABAABEEAAJAE6A679B15293A0C478219C6874A7E3C3; _putrc=EE0DDE02D8CF828E; login=true; unick=%E6%B6%82%E6%9D%BE%E9%AB%98; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=0; _gid=GA1.2.412706642.1508718279; _ga=GA1.2.144406653.1505218340; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1508031899,1508157502,1508755371,1508755385; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1508858901; LGRID=20171024232805-ee8eff0c-b8cf-11e7-9610-5254005c3644',
#        'User-Agent':
#        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.76 Safari/537.36'
#    }
    
#    headers = {
#        'origin':
#        'https://www.lagou.com',
#        'User-Agent':
#        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.76 Safari/537.36'
#    }
    
    headers = {
        'Accept':
        'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding':
        'gzip, deflate, sdch, br',
        'Accept-Language':
        'zh-CN,zh;q=0.8',
        'Cache-Control':
        'max-age=0',
        'Connection':
        'keep-alive',
        'Cookie':
        'user_trace_token=20170912201213-09228d89-2962-45d8-a915-5005559ee5fb; LGUID=20170912201214-9d07ff59-97b3-11e7-9168-5254005c3644; X_HTTP_TOKEN=f5e95edcbf2a1be96a7fd41c54770f6e; witkey_login_authToken="Es4VFc9tCRfrXwegii/KXN0dXGhRzASqCgXlI76jcfS1RuQNCc4upBIMUZb7XXZWbqy3dFhBeVlO+7DhOHf3ffFhGZt5SpgGkkBmZ9M92HFPcg0yppb2cyfDjLJvH6L1mmOu5zxBk3EndkZF0210r9RLi99f7Es6cAqEugcqKmB4rucJXOpldXhUiavxhcCELWDotJ+bmNVwmAvQCptcy5e7czUcjiQC32Lco44BMYXrQ+AIOfEccJKHpj0vJ+ngq/27aqj1hWq8tEPFFjdnxMSfKgAnjbIEAX3F9CIW8BSiMHYmPBt7FDDY0CCVFICHr2dp5gQVGvhfbqg7VzvNsw=="; TG-TRACK-CODE=index_search; SEARCH_ID=f871fb519d1a400192aa0f26a8cd5d1e; index_location_city=%E5%85%A8%E5%9B%BD; JSESSIONID=ABAAABAABEEAAJAE6A679B15293A0C478219C6874A7E3C3; _putrc=EE0DDE02D8CF828E; login=true; unick=%E6%B6%82%E6%9D%BE%E9%AB%98; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=0; _gid=GA1.2.412706642.1508718279; _ga=GA1.2.144406653.1505218340; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1508031899,1508157502,1508755371,1508755385; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1508858901; LGRID=20171024232805-ee8eff0c-b8cf-11e7-9610-5254005c3644',
        'Host':
        'www.lagou.com',
        'Upgrade-Insecure-Requests':
        '1',
        'User-Agent':
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
    }
    
    start_url_list = [start_url1, start_url2]

#Accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
#Accept-Encoding:gzip, deflate, sdch, br
#Accept-Language:zh-CN,zh;q=0.8
#Cache-Control:max-age=0
#Connection:keep-alive
#Cookie:user_trace_token=20171021104521-08891d3f-05f7-4d08-8c3c-c284f173b897; LGUID=20171021104521-e1e6f8f0-b609-11e7-a0f1-525400f775ce; SEARCH_ID=cdbcae6ebcc344e192963d283332d6e2; JSESSIONID=ABAAABAACEBACDGDB9EFCF5B208790F65FA65D0EB2B0F86; PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fjobs%2F3315756.html; X_HTTP_TOKEN=c2afecee58f044ccb17669e222590b27; _gid=GA1.2.1542207181.1508851520; _ga=GA1.2.637769763.1508553928; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1508553929,1508851520; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1508858767; LGSID=20171024231345-ed96b6e2-b8cd-11e7-9610-5254005c3644; LGRID=20171024232551-9ec0c916-b8cf-11e7-9610-5254005c3644
#Host:www.lagou.com
#Upgrade-Insecure-Requests:1
#User-Agent:Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36

#    headers = {
#        'Accept': '*/*',
#        'Accept-Language': 'en-US,en;q=0.8',
#        'Cache-Control': 'max-age=0',
#        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
#        'Connection': 'keep-alive',
#        'Referer': 'http://www.lagou.com/'
#    }    

#    headers = {
#        'Connection':
#        'keep-alive',
#        'origin':
#        "https://www.lagou.com",
#        'x-anit-forge-code':
#        "0",
#        'user-agent':
#        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36",
#        'content-type':
#        "application/x-www-form-urlencoded",
#        'accept':
#        "application/json, text/javascript, */*; q=0.01",
#        'x-requested-with':
#        "XMLHttpRequest",
#        'x-anit-forge-token':
#        "None",
#        'dnt':
#        "1",
#        'accept-encoding':
#        "gzip, deflate, br",
#        'accept-language':
#        "zh-CN,zh;q=0.8,en;q=0.6",
#        'cookie':
#        "user_trace_token=20170728162449-adcee15cc85848189cfb891619b80998; LGUID=20170728162451-3a327df6-736e-11e7-b9bc-5254005c3644; _gat=1; PRE_UTM=; PRE_HOST=; PRE_SITE=https%3A%2F%2Fwww.lagou.com%2Fgongsi%2F; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; LGSID=20170807221703-15e8d3a5-7b7b-11e7-839b-5254005c3644; index_location_city=%E5%85%A8%E5%9B%BD; JSESSIONID=ABAAABAACBHABBI1DE966CF9357E8BD2D82C53257584955; X_HTTP_TOKEN=2274185a2011ec03f73ab98f8ceaf490; TG-TRACK-CODE=index_navigation; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1501230293; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1503803797; _ga=GA1.2.1475031428.1501230295; LGRID=20170827111636-22b244c2-8ad6-11e7-8f3c-5254005c3644; SEARCH_ID=52d0e756ac5d41b395d4a9e57ab74b72; user_trace_token=20170728162449-adcee15cc85848189cfb891619b80998; LGUID=20170728162451-3a327df6-736e-11e7-b9bc-5254005c3644; index_location_city=%E5%85%A8%E5%9B%BD; user_trace_token=20170728162449-adcee15cc85848189cfb891619b80998; LGUID=20170728162451-3a327df6-736e-11e7-b9bc-5254005c3644; _gat=1; PRE_UTM=; PRE_HOST=; PRE_SITE=https%3A%2F%2Fwww.lagou.com%2Fgongsi%2F; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; LGSID=20170807221703-15e8d3a5-7b7b-11e7-839b-5254005c3644; index_location_city=%E5%85%A8%E5%9B%BD; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1501230293; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1503587852; _ga=GA1.2.1475031428.1501230295; LGRID=20170824231731-59096c0b-88df-11e7-8ea0-5254005c3644; JSESSIONID=ABAAABAACBHABBI1DE966CF9357E8BD2D82C53257584955; X_HTTP_TOKEN=2274185a2011ec03f73ab98f8ceaf490; TG-TRACK-CODE=index_navigation; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1501230293; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1503807054; _ga=GA1.2.1475031428.1501230295; LGSID=20170827121054-b83e61a1-8add-11e7-8f3c-5254005c3644; PRE_UTM=; PRE_HOST=; PRE_SITE=https%3A%2F%2Fwww.lagou.com%2Fzhaopin%2Fheiheceshi%2F%3FlabelWords%3Dlabel; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fjobs%2Flist_Go%3Fcity%3D%25E5%2585%25A8%25E5%259B%25BD%26cl%3Dfalse%26fromSearch%3Dtrue%26labelWords%3D%26suginput%3D; LGRID=20170827121054-b83e632d-8add-11e7-8f3c-5254005c3644; SEARCH_ID=ced77b843c064940a3c12c51d8720ca1",
#    }
         
    job_link_set = get_job_urls(start_url_list)
    print('len of job_link_set is ', len(job_link_set))
    store_file(job_link_set, './jobs/')
    
    



