# -*- coding: utf-8 -*-

# running in python 2.3

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

#browser = spynner.Browser()
#browser.show()
#browser.load('https://www.zhihu.com/question/50734809', load_timeout=60)
#browser.load('http://www.phei.com.cn/')
#https://www.zhihu.com/question/50734809
#browser.wait(10)
#browser.close()

def make_dir(path_dir):
    cwd_path = os.getcwd()
    path = os.path.join(cwd_path, path_dir)
    if not os.path.exists(path):
        os.mkdir(path)                 #创建文件夹

def store_file(url_list, path, headers):
    file_num = 1
    crawled_urls_set = set()
    file_url_map = OrderedDict()
    
    for i, url in enumerate(url_list):
        if i > 2000:
            break
        if url in crawled_urls_set:
            print('already crawled url ', url)
            continue
        else:
            crawled_urls_set.add(url)
        print('get i: {0} file_num: {2} url {1}'.format(i, url, file_num))
        filename = path + os.sep + str(file_num) + ".jpg"
        time.sleep(1)
        try:
            content = requests.get(url, timeout=12).content
        except Exception as e:
            print('error occured ', str(e))
        else:
            with open(filename, 'wb') as f:
                f.write(content)
                file_url_map[filename] = url
            file_num += 1        
        
    with open('file_url_map.txt', 'w') as f:
        f.write(str(file_url_map))
                
def get_pic_url_list(start_url):
    driver = webdriver.Firefox()
    driver.get(start_url)
    
    count = 0
    while count<=6:
        try: 
            more_answer = driver.find_element_by_css_selector("Button.QuestionMainAction")
            more_answer.click()
        except:
            print('get an exception count is ', count)    
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);");
        html_content = driver.page_source
        pattern1 = re.compile(r'data-original="([^"]+\.jpg)"')  #查找所有图片
        #pattern1 = re.compile(r'"([^"]+\.png)"')
        find_list = re.findall(pattern1, html_content)
        print('count is ', count, 'len of find_list is ', len(find_list))
        count += 1
        
    return find_list


if __name__=='__main__':
    start_url = 'https://www.zhihu.com/question/50734809'
    headers = {
         'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
         ' Chrome/32.0.1700.76 Safari/537.36'
         }
         
    url_list = get_pic_url_list(start_url)    
    print('len of url_list is ', len(url_list))
    store_file(url_list, './zhihu_pic/', headers)
    
#    file_map = {'1.jpg': 'http://baidu.com', '2.jpg': 'http://google.com'}
#    with open('file_url.txt', 'w') as f:
#        f.write(str(file_map))
    
#    pic_url = 'https://pic3.zhimg.com/v2-ba523260fe45bb5e43a3e129dd83dd4a_r.jpg'
#    file_name = './zhihu_pic/1.jpg'
#    try:
#        content = requests.get(pic_url).content
#    except Exception as e:
#        print('error occured ', str(e))
#    else:
#        with open(file_name, 'wb') as f:
#            f.write(content)

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
#path = os.path.join(path,'zhihu_pic')
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
