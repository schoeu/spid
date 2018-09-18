import urllib.request
import gzip
import io
import socket
import utils

config = utils.getconfig()

headers = {
    'User-Agent': config.ua,
    'accept-encoding': 'gzip',
    'cookie': config.cookie
}

timeout = 2
socket.setdefaulttimeout(timeout)

def gethtml(urls):
    rs = ''
    try:
        response = urllib.request.Request(urls, headers = headers)
        html = urllib.request.urlopen(response, timeout=10.0)
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