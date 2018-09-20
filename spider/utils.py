import os
import json
import hashlib
import urllib.request
import gzip
import io
import socket
import db
import conf
import requests

config = conf.getconfig()

def mkdirs(path):
    path = path.strip()
    isExists = os.path.exists(path)
    if isExists:
        print(path + 'is exist.')
        return False
    else:
        os.makedirs(path)
        return True

def getcwd():
    return os.getcwd()

def savejson(path, data):
    with open(path, 'w') as jsonfile:
        json.dump(data, jsonfile, ensure_ascii=False)

def getjsondata(path):
    f = open(path)
    data = json.loads(f.read())
    return data

def getfilemd5(file):
    md5_value = hashlib.md5()
    with open(file, "rb") as file:
        while True:
            data = file.read(2048)
            if not data:
               break
            #update md5
            md5_value.update(data)
    return md5_value.hexdigest()


headers = {
    'User-Agent': config['ua'],
    'accept-encoding': 'gzip',
    'cookie': config['cookie']
}

# timeout = 2
# socket.setdefaulttimeout(timeout)

def gethtml(urls):
    rs = ''
    try:
        response = urllib.request.Request(urls, headers = headers)
        html = urllib.request.urlopen(response, timeout=100.0)
        encoding = html.info().get('Content-Encoding')
        if html.getcode() == 200:
            if encoding == 'gzip':
                buf = io.BytesIO(html.read())
                gf = gzip.GzipFile(fileobj=buf)
                content = gf.read()

        if content:
            rs = content.decode('utf-8')
        
    except:
        print('Url error')
    return rs

def dlvlist():
    base = config['vdist']
    cursor = db.select('SELECT title, v_type, v_url FROM v_list WHERE dl_state = 0 order by rand() limit 0, 1000')
    rs = cursor.fetchall()
    for i in rs:
        p = os.path.join(getcwd(), base, i[1])
        mkdirs(p)
        dlmovie(i[2], p, i[0])

def updatevinfo(p, title):
    baseurl = 'update spider_data.v_list set hash = %s, dl_state= 1 where title = %s'
    hash = getfilemd5(p)
    db.execute(baseurl, (hash, title))

def dlmovie(url, base, title=''):
    strarr = url.split('?')
    if url:
        path = os.path.basename(strarr[0][:-1])
        extension = os.path.splitext(path)[1]
        local = os.path.join(base, title + extension)
        dl(url, local)
        # update to db.
        updatevinfo(local, title)
        print(local, 'done.')

def dl(url, path):
    req = requests.get(url, headers=headers, stream=True)
    chunk_size = 1024 
    content_size = int(req.headers['content-length'])
    with open(path, "wb") as file:
        for data in req.iter_content(chunk_size=chunk_size):
            file.write(data)