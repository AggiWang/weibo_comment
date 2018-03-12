# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CommentItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # table_name = 'comments'
    crawl_time = scrapy.Field()  # 当前爬取时间
    created_at = scrapy.Field()  # 评论发表时间
    like_counts = scrapy.Field()  # 评论被赞数
    source = scrapy.Field()  # 评论的发表来源
    text = scrapy.Field()  # 评论内容
    reply_text = scrapy.Field()  # 评论回复
    id = scrapy.Field()  # 评论用户id
    profile_url = scrapy.Field()  # 评论用户主页
    screen_name = scrapy.Field()  # 评论用户昵称
    verified_type = scrapy.Field()  # 评论用户认证类型，-1未认证，0认证




