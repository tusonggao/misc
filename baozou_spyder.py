import urllib.request
import bs4, os
import requests
import time
import re



def getHtml(url):  
    page = urllib.urlopen(url)  
    html =  page.read()  
    return html  
  
def getJpg(html):  
    reg = r'"largeTnImageUrl":"(.+?\.jpg)",'  
    reg = r'"(.+?\.gif)"'  
    imgre = re.compile(reg)  
    imglist = re.findall(imgre, html)      

def grabe_gif_pics(url):
    global path
    headers = {
         'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
         ' Chrome/32.0.1700.76 Safari/537.36'
         }
    req = urllib.request.Request(url=url, headers=headers)
    content = urllib.request.urlopen(req).read()
    url_list = get_url_list(content.decode())
    print('url_list is ', len(url_list))
    store_file(url_list, path, headers)
    
def get_url_list(content):
    url_list = []
    pattern1 = re.compile(r'"([^"]+\.gif)"')
    pattern2 = re.compile(r'"([^"]+\.gif-picSmall)"')
    find_list1 = re.findall(pattern1, content)
    find_list2 = re.findall(pattern2, content)
    url_list.extend(find_list1)
    url_list.extend(find_list2)
    return url_list

def get_url_list_bakup(content):
    url_list = []
    curr_index = 0
    while True:
        curr_index1 = content.find(b'.gif\"', curr_index)
        curr_index2 = content.find(b'.gif-picSmall\"', curr_index)       
        print('curr_index1', curr_index1, 'curr_index2', curr_index2)
        if curr_index1==-1 and curr_index2==-1:
            break
        if (curr_index1<curr_index2 and curr_index1!=-1) or curr_index2==-1 :
            curr_index = curr_index1
        else:
            curr_index = curr_index2
        start_index = content.rfind(b'\"', 0, curr_index)
        url_list.append(content[start_index+1:curr_index]+b'.gif')
        curr_index += 1
    return url_list    
    
    
def store_file(url_list, path, headers):
    global file_num, crawled_urls_set
    for i, url in enumerate(url_list):
        if url in crawled_urls_set:
            print('already crawled url ', url)
            continue
        else:
            crawled_urls_set.add(url)
        print('get {0} url{1}'.format(i, url))
        filename = path + os.sep + str(file_num) + ".gif"
        time.sleep(1)
        try:
            req = urllib.request.Request(url = url, headers = headers)
            content = urllib.request.urlopen(req, timeout=20).read()     
        except Exception as e:
            print('error occured ', str(e))
            continue
        with open(filename, 'wb') as f:
            f.write(content)
        if os.path.getsize(filename) < 1024*10: #如果文件小于10K
            print('Note: less than 10K, i is', i)
            os.remove(filename)
        else:
            file_num += 1

            


path = os.getcwd()
path = os.path.join(path,'暴走GIF')
if not os.path.exists(path):
  os.mkdir(path)                 #创建文件夹

crawled_urls_set = set()
file_num = 0

for page in range(1, 20):
    url = 'http://baozoumanhua.com/catalogs/gif?page=' + str(page)
    print('#'*60)
    print('page is', page, 'file_num is', file_num, 'url is', url)
    print('#'*60)
    grabe_gif_pics(url)
    
print('ending... file_num is ', file_num)


