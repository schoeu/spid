import re
import os
import json
import time
from bs4 import BeautifulSoup
import utils
import getpagedata
import db

config = utils.getconfig()

alljsonpath = './infolist/all.json'

def getsubinfo(htmlstr):
    subsoup = BeautifulSoup(htmlstr, "lxml")
    sublistitem = subsoup.select('#list_videos_common_videos_list_items > .item > a')
    sublistinfos = [{'title': item['title'], 'url': item['href']} for item in sublistitem]
    return sublistinfos

def getleavesinfo(str):
    lsoup = BeautifulSoup(str, "lxml")
    llistitem = [i.get_text() for i in lsoup.select('script') if not i.has_attr('src')]
    s = ''.join(llistitem)
    # f = open('./tmp1.txt', 'w')
    # f.write(str)
    # f.close()
    # v url
    if s:
        reg = re.compile(r"video_url: '(.*?)'", re.M)
        rs = re.search(reg, s)
        try:
            vurl = rs.group(1)
        except AttributeError as e:
            vurl = ''
        else:
            pass
        return vurl

def gettypehash(url):
    rs = getpagedata.gethtml(url)
    soup = BeautifulSoup(rs, "lxml")
    # parse main page info
    listitems = soup.select('#list_categories_categories_list_items > a')
    listinfos = [{'type': item['title'], 'url': item['href']} for item in listitems]
    # save json data
    utils.savejson(alljsonpath, listinfos)

def getsingletypeurl(hash):
    baseurl = config['typeurl']
    timestamp = str(time.time()).split('.')[0]
    fmturl = baseurl.format(hash=hash, timestamp=timestamp)
    return fmturl

def savesubinfo():
    '''
        sub page info
    '''
    data = utils.getjsondata(alljsonpath)
    vinfo = []
    for i in data:
        purl = i['pageurl']
        vtype = i['type']
        # initial page num to 1
        pagenum = 1
        if purl:
            while True:
                tpurl = purl.replace('pagenum', str(pagenum))
                subrs = getpagedata.gethtml(tpurl)
                slists = getsubinfo(subrs)
                if len(slists) == 0:
                    break
                vinfo.extend(slists)
                pagenum += 1

            utils.savejson('./infolist/{vtype}.json'.format(vtype = vtype), vinfo)
            print('共{count}条'.format(count=len(vinfo)))
            vinfo = []

def getleavelsinfo():
    rootpath = './infolist'
    lpath = './leaveinfo'
    lists = os.listdir(path = rootpath)
    for i in range(len(lists)):
        p = os.path.join(rootpath, lists[i])
        if p.find('all') == -1 and os.path.splitext(p)[1] == '.json':
            data = utils.getjsondata(p)
            for item in data:
                if item['url']:
                    levlestr = getpagedata.gethtml(item['url'])
                    vurl = getleavesinfo(levlestr)
                    print(item['title'], vurl)
                    if vurl:
                        item['vurl'] = vurl
            utils.savejson(os.path.join(lpath, lists[i]), data)
            print(os.path.join(lpath, lists[i]), ' done.')

def updatevinfo():
    vpath = '../../pspider/movies'
    baseurl = 'update spider_data.v_list set hash = %s, dl_state= 1 where title = %s'
    lists = os.listdir(path = vpath)
    for i in lists:
        p = os.path.join(vpath, i)
        vl = os.listdir(path = p)
        for item in vl:
            title = os.path.splitext(item)[0]
            hash = utils.getfilemd5(os.path.join(p, item))
            db.execute(baseurl, (hash, title))
            print((hash, title))
            

def savedata():
    basesql = 'insert into spider_data.v_list (title, url, v_url,v_type, v_source) values (%s, %s, %s, %s, %s)'
    lpath = './leaveinfo'
    lists = os.listdir(path = lpath)
    for i in lists:
        basename = os.path.splitext(i)[0]
        path = os.path.join(lpath, i)
        if path.find('.json') != -1:
            data = utils.getjsondata(path)
            sqldata = [tuple(i.values()) + (basename, 'ppx') for i in data]
            # print(sqldata)
            db.executemany(basesql, sqldata, basename)

def main():
    # step 1
    # # 获取分类列表
    # url = config['categoriesurl']
    # gettypehash(url)
    # # 获取每个分类的内容列表并保存
    # data = utils.getjsondata(alljsonpath)
    # for i in data:
    #     if i['url']:
    #         hash = i['url'].split('/')
    #         rshash = hash[4]
    #         if rshash:
    #             rsurl = getsingletypeurl(rshash)
    #             i['pageurl'] = rsurl
    # utils.savejson(alljsonpath, data)

    # step 2
    # savesubinfo()

    # step 3
    # getleavelsinfo()

    # step 4
    # save data to mysql
    # savedata()

    # step 5
    #ts = utils.getfilemd5('../videos/5.mp4')
    #updatevinfo()

    # finally
    db.closeconn()

if __name__ == '__main__':
    main()
    