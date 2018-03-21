import requests
import threading
"""
    文件下载类 支持多线程下载 但主要看服务器是否支持range的方式 
    注意如果服务器keep-alive可能无法下载
"""
class DownFile(object):
    def Handler(self,start, end, url, filename):
        headers = {'Range': 'bytes=%d-%d' % (start, end)}
        r = requests.get(url, headers=headers, stream=True)
        
        # 写入文件对应位置
        with open(filename, "r+b") as fp:
            fp.seek(start)
            fp.tell()
            fp.write(r.content)
    def download_file(self,url,num_thread=1):
        r = requests.head(url)
        if r.status_code==200:
            """
                状态码为200不能支持range
            """
            num_thread = 1
        elif r.status_code==206:
            """
              状态代码206支持range
            """
            num_thread=5
            
        try:
            file_name = url.split('/')[-1]           
            file_size =  int(r.headers['content-length'])

         
        except:
            print('检查url,或不支持对线程的下载')
            return
        fp = open(file_name,"wb")
        fp.truncate(file_size)
        fp.close()
      
        part = file_size//num_thread
        for i in range(num_thread):
            start = part*i
            if i==num_thread-1:
                end = file_size
            else:
                end = start+file_size
        
        t = threading.Thread(target=self.Handler,kwargs={'start':start,'end':end,'url':url,'filename':file_name})
        t.setDaemon(False)
        t.start()


        main_thread = threading.current_thread()
        for t in threading.enumerate():
            if t is main_thread:
                continue
            t.join()
        print('%s 下载完成' %file_name)
                
