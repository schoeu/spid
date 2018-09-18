import utils
import os
import json

def getjsondata(path):
    if not os.path.isabs(path):
        path = os.path.join(os.path.dirname(os.path.realpath(__file__)), path)
    f = open(path)
    data = json.loads(f.read())
    return data

def getconfig():
    return getjsondata('./conf.json')