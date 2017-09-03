#_*_coding: utf-8 _*_
#FileName: crossinip.py
#Author: yang
#History: 1.0#2017/8/25

import requests
import json
import pickle

api_url = 'http://lab.crossincode.com/proxy/get/?num=20'
s = json.loads(requests.get(api_url).text)
li = []
for proxies in s['proxies']:
    li.append(proxies['http'])

out = open('crossin.pick','wb')
pickle.dump(li, out)
