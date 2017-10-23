import hashlib
import os
import time

def GetFileMd5(filename):
    if not os.path.isfile(filename):
        return
    myhash = hashlib.md5()
    f = file(filename,'rb')
    while True:
        b = f.read(8096)
        if not b :
            break
        myhash.update(b)
    f.close()
    return myhash.hexdigest()	
	
if __name__=='__main__':    
    start_t = time.time()
    print GetFileMd5('F:/github/tusonggao/spider_python/zhihu_pic/1.jpg')
    print GetFileMd5('F:/github/tusonggao/spider_python/zhihu_pic/111.jpg')
    print GetFileMd5('F:/github/tusonggao/spider_python/zhihu_pic/222.jpg')
    end_t = time.time()
    
    print(len('7e5712007f904bc90aca701eec09e980'))
    
    print('costs time is ', end_t-start_t)