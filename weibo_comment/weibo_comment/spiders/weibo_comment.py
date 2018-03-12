
import scrapy
from ..items import CommentItem
import requests
import json
import re
import time
import math


class weiboSpider(scrapy.Spider):
    name = "weibo_single"
    allowed_domains = ['m.weibo.cn']
    id = 4171147094621232
    comment_count = 0
    comment_page = -1
    init_url = 'https://m.weibo.cn/api/comments/show?id={}&page={}'
    start_urls = [init_url.format(id, 1)]
    html = requests.get(start_urls[0]).text
    infos = json.loads(html)
    comment_counts = int(infos['data']['total_number'])


    def parse(self,response):
        if self.comment_count < self.comment_counts:
            self.comment_page += 1
            print(self.comment_page)
            comment_url = 'https://m.weibo.cn/single/rcList?format=cards&id={}&type=comment&hot=0&page={}'.format(self.id, self.comment_page)
            yield scrapy.Request(url=comment_url, dont_filter=True,callback=self.comment_info)


    def comment_info(self,response):
        infos = json.loads(response.body)
        item = CommentItem()
        for data in infos[-1]['card_group']:

            created_at = data['created_at']
            like_counts = data['like_counts']
            source = data['source']
            str_text = data['text']
            st = re.compile(r'<[^>]+>', re.S)
            text = st.sub('', str_text)
            try:
                str_reply_text = data['reply_text']
                rt = re.compile(r'<[^>]+>', re.S)
                reply_text = rt.sub('', str_reply_text)
            except:
                reply_text = ''
            id = data['id']
            profile_url = 'https://m.weibo.cn' + data['user']['profile_url']
            screen_name = data['user']['screen_name']
            verified_type = data['user']['verified_type']

            item['crawl_time'] = time.strftime('%Y-%m-%d %H:%M:%S')
            item['created_at'] = created_at
            item['like_counts'] = like_counts
            item['source'] = source
            item['text'] = text
            item['reply_text'] = reply_text
            item['id'] = id
            item['profile_url'] = profile_url
            item['screen_name'] = screen_name
            item['verified_type'] = verified_type

            self.comment_count += 1
            yield item

        yield scrapy.Request(url=response.url, callback=self.parse)