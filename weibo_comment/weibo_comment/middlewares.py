# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals


class WeiboSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

#自定义的ip代理池配置		
import random  
import time
import scrapy  
from scrapy import log  
import requests
import json

# logger = logging.getLogger()  

class ProxyMiddleWare(object):  
    """docstring for ProxyMiddleWare"""  
    def process_request(self,request, spider):  
        '''对request对象加上proxy'''  
        proxy = self.get_random_proxy()  
        print("this is request ip:"+proxy)  
        request.meta['proxy'] = proxy   


    def process_response(self, request, response, spider):  
        '''对返回的response处理'''  
        # 如果返回的response状态不是200，重新生成当前request对象  
        if response.status != 200:  
            proxy = self.get_random_proxy()  
            print("this is response ip:"+proxy)  
            # 对当前reque加上代理  
            request.meta['proxy'] = proxy   
            return request  
        return response  

    # def get_random_proxy(self):
    #     '''随机从文件中读取proxy'''
    #     while 1:
    #         with open('proxies.txt', 'r') as f:
    #             proxies = f.readlines()
    #         if proxies:
    #             break
    #         else:
    #             time.sleep(1)
    #     proxy = random.choice(proxies).strip()
    #     return proxy

    def get_random_proxy(self):
        '''获取proxy'''
        r = requests.get('http://127.0.0.1:8000/?types=0&protocol=1&count=99')
        ip_ports = json.loads(r.text)
        # ip = ip_ports[self.i][0]
        # port = ip_ports[self.i][1]
        # proxies = {
        #     'http': 'http://%s:%s' % (ip, port),
        #     'https': 'https://%s:%s' % (ip, port)
        # }

        # print(proxies)
        # r = requests.get('http://ip.chinaz.com/', proxies=proxies['https'])
        # print(r)
        # r.encoding = 'utf-8'
        # proxy = r.text
        ip_port = random.choice(ip_ports)
        proxy = "https://%s:%s" % (ip_port[0], ip_port[1])
        return proxy
