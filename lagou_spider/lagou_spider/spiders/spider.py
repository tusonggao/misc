# -*- coding: utf-8 -*-
from __future__ import absolute_import

import scrapy
import time
import logging
from bs4 import BeautifulSoup
from lagou_spider.items import LagouItem

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By

class LagouSpider(scrapy.Spider):
    name = 'lagouspider'
    allowed_domains = ['lagou.com']
    headers = {
        'origin':
        "https://www.lagou.com",
        'x-anit-forge-code':
        "0",
        'user-agent':
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36",
        'content-type':
        "application/x-www-form-urlencoded",
        'accept':
        "application/json, text/javascript, */*; q=0.01",
        'x-requested-with':
        "XMLHttpRequest",
        'x-anit-forge-token':
        "None",
        'dnt':
        "1",
        'accept-encoding':
        "gzip, deflate, br",
        'accept-language':
        "zh-CN,zh;q=0.8,en;q=0.6",
        'cookie':
        "user_trace_token=20170728162449-adcee15cc85848189cfb891619b80998; LGUID=20170728162451-3a327df6-736e-11e7-b9bc-5254005c3644; _gat=1; PRE_UTM=; PRE_HOST=; PRE_SITE=https%3A%2F%2Fwww.lagou.com%2Fgongsi%2F; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; LGSID=20170807221703-15e8d3a5-7b7b-11e7-839b-5254005c3644; index_location_city=%E5%85%A8%E5%9B%BD; JSESSIONID=ABAAABAACBHABBI1DE966CF9357E8BD2D82C53257584955; X_HTTP_TOKEN=2274185a2011ec03f73ab98f8ceaf490; TG-TRACK-CODE=index_navigation; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1501230293; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1503803797; _ga=GA1.2.1475031428.1501230295; LGRID=20170827111636-22b244c2-8ad6-11e7-8f3c-5254005c3644; SEARCH_ID=52d0e756ac5d41b395d4a9e57ab74b72; user_trace_token=20170728162449-adcee15cc85848189cfb891619b80998; LGUID=20170728162451-3a327df6-736e-11e7-b9bc-5254005c3644; index_location_city=%E5%85%A8%E5%9B%BD; user_trace_token=20170728162449-adcee15cc85848189cfb891619b80998; LGUID=20170728162451-3a327df6-736e-11e7-b9bc-5254005c3644; _gat=1; PRE_UTM=; PRE_HOST=; PRE_SITE=https%3A%2F%2Fwww.lagou.com%2Fgongsi%2F; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; LGSID=20170807221703-15e8d3a5-7b7b-11e7-839b-5254005c3644; index_location_city=%E5%85%A8%E5%9B%BD; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1501230293; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1503587852; _ga=GA1.2.1475031428.1501230295; LGRID=20170824231731-59096c0b-88df-11e7-8ea0-5254005c3644; JSESSIONID=ABAAABAACBHABBI1DE966CF9357E8BD2D82C53257584955; X_HTTP_TOKEN=2274185a2011ec03f73ab98f8ceaf490; TG-TRACK-CODE=index_navigation; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1501230293; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1503807054; _ga=GA1.2.1475031428.1501230295; LGSID=20170827121054-b83e61a1-8add-11e7-8f3c-5254005c3644; PRE_UTM=; PRE_HOST=; PRE_SITE=https%3A%2F%2Fwww.lagou.com%2Fzhaopin%2Fheiheceshi%2F%3FlabelWords%3Dlabel; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fjobs%2Flist_Go%3Fcity%3D%25E5%2585%25A8%25E5%259B%25BD%26cl%3Dfalse%26fromSearch%3Dtrue%26labelWords%3D%26suginput%3D; LGRID=20170827121054-b83e632d-8add-11e7-8f3c-5254005c3644; SEARCH_ID=ced77b843c064940a3c12c51d8720ca1",
    }
    start_url1 = 'https://www.lagou.com/jobs/list_%E6%9C%BA%E5%99%A8%E5%AD%A6%E4%B9%A0?px=default&city=%E5%85%A8%E5%9B%BD' #机器学习
    start_url2 = 'https://www.lagou.com/jobs/list_%E6%95%B0%E6%8D%AE%E6%8C%96%E6%8E%98?city=%E5%85%A8%E5%9B%BD' #数据挖掘
    start_url3 = 'https://www.lagou.com/jobs/list_%E6%8E%A8%E8%8D%90%E7%AE%97%E6%B3%95?city=%E5%85%A8%E5%9B%BD' # 推荐算法
    start_url_list = [start_url1, start_url2, start_url3]
#    start_url_list = [start_url1]
    crawled_urls_set = set()					  
                      
    def start_requests(self):
        driver = webdriver.Firefox()
    
        for url in self.start_url_list:
            driver.get(url)
            WebDriverWait(driver, 30)
            count = 0
            while count<=30:
                count += 1
                link_list = self.get_job_link(driver.page_source)
                for url_ in link_list:
                    if url_ in self.crawled_urls_set:
                        logging.info('already crawled url {0}'.format(url_))
                        continue
                    else:
                        self.crawled_urls_set.add(url_)
                        logging.info('crawl url is {0}'.format(url_))
                        yield scrapy.Request(url=url_, headers=self.headers, 
                                             callback=self.parse)       
                try:
                    next_page = driver.find_element_by_class_name('pager_next')
                    next_page.click()
                except Exception as e:
                    print('Exception is ', str(e))
        
        driver.quit()
    
    
    def get_job_link(self, html):
        soup = BeautifulSoup(html, 'lxml')
        positions = soup.find_all(class_='position_link')
        link_list = [pos['href'] for pos in positions]
        return link_list

    def parse(self, response):
        logging.info('get response of url {0}'.format(response.url))
        number = response.url.split('/')[-1].split('.')[0]     
        item = LagouItem()
        item['number'] = number
        item['content'] = response.text        
        return item
        
#    def parse_job_url(self, response):
#	   number = response.url.split('/')[-1].split('.')[0]     
#        item = XiaoshuoItem()
#        item['number'] = number
#        item['content'] = response.text        
#        return item
	

