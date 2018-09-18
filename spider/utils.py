import os
from urllib.request import build_opener, install_opener, urlretrieve
import json
import hashlib

'''
Utils for pspider.
'''

def getconfig():
    return getjsondata('./conf.json')

config = getconfig()

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

def dlmovie(url, base, title=''):
    strarr = url.split('?')
    if url:
        path = os.path.basename(strarr[0][:-1])
        extension = os.path.splitext(path)[1]
        local = os.path.join(base, title + extension)
        print('local~~', local)
        opener=build_opener()
        opener.addheaders=[('User-Agent', config['ua'])]
        install_opener(opener)
        urlretrieve(url, local)
        print(title + ' done.')

def savejson(path, data):
    with open(path, 'w') as jsonfile:
        json.dump(data, jsonfile, ensure_ascii=False)

def getjsondata(path):
    f = open(path)
    b = os.path.join(getcwd(), 'movies')
    # encoding='ISO-8859-1'
    data = json.loads(f.read())
    return data

def dlvlist():
    f = open('./movieinfo.js')
    b = os.path.join(getcwd(), 'movies')
    data = json.loads(f.read())
    for i in data:
        burl = os.path.join(b, i['type'])
        mkdirs(burl)
        for j in i['subs']:
            print(j['vurl'])
            if j['vurl']:
                print('vurl~~', j['vurl'])
                dlmovie(j['vurl'], burl, j['title'])

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
