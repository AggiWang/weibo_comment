# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log


class WeiboPipeline(object):
    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        #update方法，第一个参数传入查询条件，url_token，第二个参数传入字典类型的对象，item，第三个参数传入True，如果查询数据存在的话就更新，不存在的话就插入。这样可以保证去重。
        self.collection.update({'id': item['id']}, {'$set': dict(item)}, True)
        return item