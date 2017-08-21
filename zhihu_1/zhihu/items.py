# -*- coding: utf-8 -*-

# ------------------------------------------
#   版本：1.0
#   日期：2017-8-06
#   作者：AlexTan
#   <CSDN:   http://blog.csdn.net/alextan_>  
#   <e-mail: alextanbz@gmail.com>
# ------------------------------------------

import scrapy


class ZhihuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    user_id = scrapy.Field()
    user_image_url = scrapy.Field()
    name = scrapy.Field()
    locations = scrapy.Field()
    business = scrapy.Field() #所在行业
    employments = scrapy.Field() #职业经历
    gender = scrapy.Field()
    education = scrapy.Field()
    followees_num = scrapy.Field() #我关注的人数
    followers_num = scrapy.Field() #关注我的人数

class RelationItem(scrapy.Item):
    user_id = scrapy.Field()
    relation_type = scrapy.Field() #关系类型
    relations_id = scrapy.Field()

class AnswerItem(scrapy.Item):
    answer_user_id = scrapy.Field()
    answer_id = scrapy.Field()
    question_id = scrapy.Field()
    cretated_time = scrapy.Field()
    updated_time = scrapy.Field()
    voteup_count = scrapy.Field()
    comment_count = scrapy.Field()
    content = scrapy.Field()

class QuestionItem(scrapy.Item):
    ask_user_id = scrapy.Field()
    question_id = scrapy.Field()
    ask_time = scrapy.Field()
    answer_count = scrapy.Field()
    followees_count = scrapy.Field()
    title = scrapy.Field()

class ArticleItem(scrapy.Item):
    author_id = scrapy.Field()
    title = scrapy.Field()
    article_id = scrapy.Field()
    content = scrapy.Field()
    cretated_time = scrapy.Field()
    updated_time = scrapy.Field()
    voteup_count = scrapy.Field()
    comment_count = scrapy.Field()