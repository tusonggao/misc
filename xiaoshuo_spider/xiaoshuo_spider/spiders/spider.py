# -*- coding: utf-8 -*-
from __future__ import absolute_import

import scrapy
from bs4 import BeautifulSoup
from xiaoshuo_spider.items import XiaoshuoItem


class XiaoshuoSpider(scrapy.Spider):
    name = 'xiaoshuospider'
    allowed_domains = ['136book.com']
    base_url = 'http://www.136book.com/'    
    xiaoshuo_names = ['huaqiangu', 'fanyiguan-1', 
                      'xianqingjue', 'xuanfengshaonv']
                      
    def start_requests(self):
        for name in self.xiaoshuo_names:
            url = self.base_url + name + '/'
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        
        book_detail = soup.find_all(id='book_detail')[1]
        li_list = book_detail.find('ol').find_all('li')
        for li in li_list:
            content_url = li.a['href']
            yield scrapy.Request(url=content_url, callback=self.parse_content)
        
    def parse_content(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
         
        title = soup.find('h1').text         
        content = soup.find(id='content')
        text = ''
        for p in content.find_all('p'):
            text += p.text + '\n\n'
     
        item = XiaoshuoItem()
        item['name'] = response.url.split('/')[3]
        item['title'] = title
        item['content'] = text
        
        return item
	

