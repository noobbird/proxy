#_*_coding: utf-8 _*_
#Author: yang
#FileName: test.py
#History: 1.0#2017/8/24

import requests
import pickle
import get_proxies
f = file("usaproxy.pick")
f1 = file("crossin.pick")
li1 = pickle.load(f1)
li = pickle.load(f)
li.extend(li1)
resli = []
#li = get_proxies.get_proxies()
url = "http://music.163.com"
print 'proxy'.ljust(20)  +'\t' + 'res_proxy'.ljust(20) +'\tdelay'
for p in li:
    proxy = {'http':'http://'+p}
    try:
        r = requests.get(url, proxies = proxy, timeout = 1)
        resli.append(p)
        req_proxy = p
        res_proxy = r.headers['X-From-Src']
        lapstime = r.elapsed.microseconds/1000
        print req_proxy.ljust(20) + '\t' +res_proxy.ljust(20)+'\t'+str(lapstime)+ 'ms'
    except Exception,e:
        print p
        continue
output = open('proxy.pick','wb')
pickle.dump(resli, output)
