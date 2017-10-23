# -*- coding: utf-8 -*-
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup 
import re
import time
import os
import sip
import PyQt4
import spynner
from setuptools import setup

#browser = spynner.Browser()
#browser.show()
#browser.load('https://www.zhihu.com/question/50734809', load_timeout=60)
#browser.load('http://www.phei.com.cn/')
#https://www.zhihu.com/question/50734809
#browser.wait(10)
#browser.close()

driver = webdriver.Firefox()
driver.get("https://www.zhihu.com/question/50734809")

count = 0
while count<=50:
    try: 
        more_answer = driver.find_element_by_css_selector("Button.QuestionMainAction")
        more_answer.click()
    except:
        print('get an exception count is ', count)    
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);");
    html_content = driver.page_source
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);");
    pattern1 = re.compile(r'"([^"]+\.jpg)"')  #查找所有图片
    #pattern1 = re.compile(r'"([^"]+\.png)"')
    find_list = re.findall(pattern1, html_content)
    print('count is ', count, 'len of find_list is ', len(find_list))
    count += 1



#for url in find_list:
#    print('url is ', url)


#time.sleep(2)  #休眠0.3秒
#driver.find_element_by_id("kw").send_keys(u"涂松高")
#time.sleep(2)  #休眠0.3秒



#url = 'https://www.zhihu.com/question/50734809'
#driver = webdriver.Firefox()
#
#driver.get("http://www.baidu.com")
#time.sleep(2)  #休眠0.3秒
#'https://www.zhihu.com/question/50734809', load_timeout=60
#driver.find_element_by_id("kw").send_keys(u"涂松高")
#time.sleep(2)  #休眠0.3秒
#driver.find_element_by_id("su").click()
#driver.find_element_by_name("tj_login").click()
#
#driver.find_element_by_name("userName").send_keys('tusonggao')
#driver.find_element_by_name("password").send_keys('12345asdfg')
#driver.find_element_by_id("TANGRAM__PSP_10__submit").click()


#def grabe_gif_pics(url):
#    global path
#    headers = {
#         'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
#         ' Chrome/35.0.1700.76 Safari/537.36'
#         }
#    req = urllib.request.Request(url=url, headers=headers)
#    content = urllib.request.urlopen(req).read().decode()
#    with open('./urllib_content.html', 'w', encoding='UTF-8') as f:
#        f.write(content)
#        
#    url_list = get_url_list(content)
#    print('content is ', content)
#    print('url_list is ', len(url_list))
##    store_file(url_list, path, headers)
#    
#    
#def get_url_list(content):
#    print('content is ', content)
#    url_list = []
#    pattern1 = re.compile(r'"([^"]+\.gif)"')
#    pattern2 = re.compile(r'"([^"]+\.gif-picSmall)"')
#    find_list1 = re.findall(pattern1, content)
#    find_list2 = re.findall(pattern2, content)
#    url_list.extend(find_list1)
#    url_list.extend(find_list2)
#    return url_list
#
#path = os.getcwd()
#path = os.path.join(path,'知乎GIF')
#if not os.path.exists(path):
#    os.mkdir(path)                 #创建文件夹
#
#crawled_urls_set = set()
#file_num = 0
#
#url = 'https://www.zhihu.com/question/22918070'
#print('#'*60)
#print('page is', page, 'file_num is', file_num, 'url is', url)
#print('#'*60)
#grabe_gif_pics(url)

    
    
#print('ending... file_num is ', file_num)

#driver.quit()
