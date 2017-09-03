#-*-coding:utf-8-*-

import pickle
import requests
from lxml import etree
import time
import sys

def get_proxies():
        url = "https://www.us-proxy.org"
        rq = requests.get(url, verify=False)
        tree = etree.HTML(rq.text)
        port_path =".//*[@id='proxylisttable']/tbody/tr/td[2]/text()"
        ip_path = ".//*[@id='proxylisttable']/tbody/tr/td[1]/text()"
        ips = tree.xpath(ip_path)
        ports = tree.xpath(port_path)
        proxies = [a+':'+b for a,b in zip(ips,ports)]
        #print proxies

        return proxies

def get_all():
	url = "https://www.us-proxy.org"
	rq = requests.get(url, verify=False)
	tree = etree.HTML(rq.text)
	
	port_path =".//*[@id='proxylisttable']/tbody/tr/td[2]/text()"
	ip_path = ".//*[@id='proxylisttable']/tbody/tr/td[1]/text()"
	anonymity_path = ".//*[@id='proxylisttable']/tbody/tr/td[5]/text()"
        http_path = ".//*[@id='proxylisttable']/tbody/tr/td[7]/text()"
        http = tree.xpath(http_path)
        anonymity = tree.xpath(anonymity_path)
	ips = tree.xpath(ip_path)
	ports = tree.xpath(port_path)
	proxies = [a+':'+b for a,b in zip(ips,ports)]	
	#print proxies
	
	return (proxies, anonymity, http)


def get_valid_proxies((proxies, anonymity, ishttp),count):
	url = 'http://www.baidu.com'
	results = []
	cur = 0
        avertime = 0
        filted_proxy = []
        print 'raw count= ' + str(len(proxies))
        print "proxies".ljust(20) +'\tanonymity\tisHttps\tavertime\n'
	for p,a,i in zip(proxies, anonymity, ishttp):
		proxy = {'http':'http://'+p}
		succeed = False
                try_count = 0
                consume_time = 0
		try:
                    while try_count < 3:
			r = requests.get(url,proxies = proxy,timeout = 1)
			lapstime = r.elapsed.microseconds/1000
                        consume_time += lapstime
                        try_count += 1
                        time.sleep(1)
                    avertime = consume_time/try_count 
                    succeed = True
		except Exception,e:
	            continue
		if succeed:
                        filted_proxy.append(p)
			print p.ljust(20) + "\t" + a + '\t' + i + "\t" +str(avertime) + 'ms'
			results.append(p)
			cur += 1
                        if count == -1:
                            continue
			elif cur>= count:
				break
        out = open("usaproxy.pick","wb")
        pickle.dump(filted_proxy, out)

if __name__ == '__main__':
        if len(sys.argv) > 1:
	    get_valid_proxies(get_all(),sys.argv[1])
        else:
            get_valid_proxies(get_all(),40)
