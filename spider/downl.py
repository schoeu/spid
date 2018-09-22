import threading
from multiprocessing import cpu_count
import cusconf
import requests

config = cusconf.getconfig()

baseheader = {
    'User-Agent': config['ua'],
    'accept-encoding': 'gzip',
    'cookie': config['cookie']
}

def Handler(start, end, url, filename):
    cushander = {'Range': 'bytes=%d-%d' % (start, end)}
    headers = {**baseheader, **cushander}
    r = requests.get(url, headers=headers, stream=True)
    with open(filename, "r+b") as fp:
        fp.seek(start)
        var = fp.tell()
        fp.write(r.content)

def download(url, path):
    num_thread = cpu_count()
    r = requests.head(url)
    print(r.headers['Transfer-Encoding'])
    try:
        file_size = int(r.headers['content-length'])
    except:
        print("Not surpport.")
        return
 
    #  create file
    fp = open(path, "wb")
    fp.truncate(file_size)
    fp.close()
 
    # 启动多线程写文件
    part = file_size // num_thread  
    for i in range(num_thread):
        start = part * i
        if i == num_thread - 1: 
            end = file_size
        else:
            end = start + part
 
        t = threading.Thread(target=Handler, kwargs={'start': start, 'end': end, 'url': url, 'filename': path})
        t.setDaemon(True)
        t.start()
 
    # all thread done
    main_thread = threading.current_thread()
    for t in threading.enumerate():
        if t is main_thread:
            continue
        t.join()