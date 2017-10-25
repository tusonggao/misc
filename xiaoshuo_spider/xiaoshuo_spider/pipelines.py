# -*- coding: utf-8 -*-
from __future__ import print_function

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os

class XiaoshuoPipeline(object):
    def process_item(self, item, spider):
        print('in XiaoshuoPipeline process_item cwd is ', os.getcwd())
        path = os.getcwd() + '/xiaoshuo/'
        path = os.path.join(path, item['name'])
        if not os.path.exists(path):
            os.mkdir(path)   # 如果不存在，则创建文件夹
            
        file_name = path + os.sep + item['title'] + '.txt'
        with open(file_name, 'w') as f:
            f.write(item['content'])
            
        return item
