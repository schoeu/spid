import os
import shutil
import utils

def get_FileSize(filePath):
    fsize = os.path.getsize(filePath)
    fsize = fsize / float(1024*1024)
    return round(fsize, 2)

p = '../pspider/movies'
dist = '../pspider/tmp'
lists = os.listdir(path = p)
for i in lists:
    rsp = os.path.join(p, i)
    l = os.listdir(os.path.join(rsp))
    d = os.path.join(dist, i)
    for item in l:
        dirs = os.path.join(rsp, item)
        ddirs = os.path.join(d, item)
        h = get_FileSize(dirs)
        if h < 24:
            utils.mkdirs(d)
            print(h, 'MB, ', dirs)
            shutil.copy(dirs, ddirs)
