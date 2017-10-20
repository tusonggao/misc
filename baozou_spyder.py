import urllib.request
import bs4, os
import requests
import time

# http://wanzao2.b0.upaiyun.com/1505864549963f322d56dae7738693c85e876c4b1b681.gif-picSmall
#content = 'aaa"333.gif"bbb"444.gif"'

def grabe_gif_pics(url):
    global path
#    url = "http://baozoumanhua.com/catalogs/gif"   #url地址
    headers = {
         'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
         ' Chrome/32.0.1700.76 Safari/537.36'
         }
    req = urllib.request.Request(url=url, headers=headers)
    content = urllib.request.urlopen(req).read()
    url_list = get_url_list(content)
    print('url_list is ', len(url_list))
    store_file(url_list, path, headers)
    

def get_url_list(content):
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
            req = urllib.request.Request(url = url.decode(), headers = headers)
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

for page in range(2):
    print('page is ', page)
    url = 'http://baozoumanhua.com/catalogs/gif?page=' + str(page)
    print('url is ', url)
    grabe_gif_pics(url)


