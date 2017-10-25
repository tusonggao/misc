# -*- coding: utf-8 -*-
from __future__ import print_function

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import logging
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class LagouPipeline(object):
    def process_item(self, item, spider):
        logging.info('in LagouPipeline process_item cwd is {0}'.format(os.getcwd()))
        path = os.getcwd() + '/jobs/'
        if not os.path.exists(path):
            os.mkdir(path)   # 如果不存在，则创建文件夹
        
        file_name = path + os.sep + item['number'] + '.html'
        logging.warning('save file_name is: {0}'.format(file_name))
        with open(file_name, 'w') as f:
            f.write(item['content'])
            
        return item
