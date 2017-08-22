# -*- coding: utf-8 -*-
import scrapy
import re
import pdb
import json
from scrapy.http import Request
from ..items import ZhihuItem,RelationItem,AnswerItem,QuestionItem,ArticleItem
from ..scrapy_redis.spiders import RedisSpider

# ------------------------------------------
#   版本：1.0
#   日期：2017-8-06
#   作者：AlexTan
#   <CSDN:   http://blog.csdn.net/alextan_>  
#   <e-mail: alextanbz@gmail.com>
# ------------------------------------------

class Zhihuspider0Spider(RedisSpider):
    name = 'zhihuspider'
    redis_key = "zhihuspider:start_urls"
    allowed_domains = ['zhihu.com']
    start_urls = ['http://zhihu.com/']
    strat_user_id = ['yun-he-shu-ju-8']

    def start_requests(self):
        for one in self.strat_user_id:
            yield Request('https://www.zhihu.com/api/v4/members/'+one+'?include=locations,employments,industry_category,gender,educations,business,follower_count,following_count,description,badge[?(type=best_answerer)].topics',meta={'user_id':one},callback=self.parse)
            

    def parse(self, response):
        json_result = str(response.body,encoding="utf8").replace('false','0').replace('true','1')
        dict_result = eval(json_result)
        item = ZhihuItem()
        if dict_result['gender'] == 1:
            item['gender'] = '男'
        elif dict_result['gender'] == 0:
            item['gender'] = '女'
        else:
            item['gender'] = '未知'
        item['user_id'] = dict_result['url_token']
        item['user_image_url'] = dict_result['avatar_url'][:-6] + 'xl.jpg'
        item['name'] = dict_result['name']
        item['locations'] = []
        for one in dict_result['locations']:
            item['locations'].append(one['name'])
        try:
            item['business'] = dict_result['business']['name']
        except:
            try:
                item['business'] = dict_result['industry_category']
            except:
                pass

        item['education'] = []
        for one in dict_result['educations']:
            try:
                education = one['school']['name'] + ":" + one['major']['name']
            except:
                try:
                    education = one['school']['name']
                except:
                    pass
            item['education'].append(education)
        #pdb.set_trace()
        item['followees_num'] = dict_result['following_count']
        item['followers_num'] = dict_result['follower_count']
        item['employments'] = []
        for one in dict_result['employments']:
            try:
                employment = one['company']['name'] + ":" + one['job']['name']
            except:
                try:
                    employment = one['company']['name']
                except:
                    pass
            item['employments'].append(employment)
        #pdb.set_trace()
        yield item
        item = RelationItem()
        one = response.meta['user_id']
        item['relations_id'] = []
        item['user_id'] = one
        item['relation_type'] = ''
        yield Request('https://www.zhihu.com/api/v4/members/'+one+'/followers?include=data[*].answer_count,badge[?(type=best_answerer)].topics&limit=20&offset=0',callback=self.parse_relation,meta={'item':item,'offset':0,'relation_type':'followers'})
        yield Request('https://www.zhihu.com/api/v4/members/'+one+'/followees?include=data[*].answer_count,badge[?(type=best_answerer)].topics&limit=20&offset=0',callback=self.parse_relation,meta={'item':item,'offset':0,'relation_type':'followees'})
        yield Request('https://www.zhihu.com/api/v4/members/'+one+'/answers?include=data[*].comment_count,content,voteup_count,created_time,updated_time;data[*].author.badge[?(type=best_answerer)].topics&limit=20&offset=0',callback=self.parse_answer,meta={'answer_user_id':one,'offset':0})
        yield Request('https://www.zhihu.com/people/'+one+'/asks?page=1',callback=self.parse_question,meta={'ask_user_id':one,'page':1})
        yield Request('https://www.zhihu.com/api/v4/members/'+one+'/articles?include=data[*].comment_count,content,voteup_count,created,updated;data[*].author.badge[?(type=best_answerer)].topics&limit=20&offset=0',callback=self.parse_article,meta={'author_id':one,'offset':0})

    def parse_relation(self,response):
        json_result = str(response.body,encoding="utf8").replace('false','0').replace('true','1')
        dict_result = eval(json_result)
        relations_id = []
        for one in dict_result['data']:
            relations_id.append(one['url_token'])
        response.meta['item']['relations_id'] = relations_id
        if response.meta['offset'] == 0:
            response.meta['item']['relation_type'] = response.meta['relation_type']
        else:
            response.meta['item']['relation_type'] = 'next:' + response.meta['relation_type']
        #pdb.set_trace()
        yield response.meta['item']
        for one in response.meta['item']['relations_id']:
                yield Request('https://www.zhihu.com/api/v4/members/'+one+'?include=locations,employments,industry_category,gender,educations,business,follower_count,following_count,description,badge[?(type=best_answerer)].topics',meta={'user_id':one},callback=self.parse)
        #pdb.set_trace()
        if dict_result['paging']['is_end'] == 0:
            #pdb.set_trace()
            offset = response.meta['offset'] + 20
            next_page = re.findall('(.*offset=)\d+',response.url)[0]
            #pdb.set_trace()
            yield Request(next_page + str(offset),callback=self.parse_relation,meta={'item':response.meta['item'],'offset':offset,'relation_type':response.meta['relation_type']})

    def parse_answer(self,response):
        json_result = str(response.body,encoding="utf8").replace('false','0').replace('true','1')
        dict_result = eval(json_result)
        for one in dict_result['data']:
            item = AnswerItem()
            item['answer_user_id'] = response.meta['answer_user_id']
            item['answer_id'] = one['id']
            item['question_id'] = one['question']['id']
            #pdb.set_trace()
            item['cretated_time'] = one['created_time']
            item['updated_time'] = one['updated_time']
            item['voteup_count'] = one['voteup_count']
            item['comment_count'] = one['comment_count']
            item['content'] = one['content']
            yield item
        if dict_result['paging']['is_end'] == 0:
            offset = response.meta['offset'] + 20
            next_page = re.findall('(.*offset=)\d+',response.url)[0]
            yield Request(next_page + str(offset),callback=self.parse_answer,meta={'answer_user_id':response.meta['answer_user_id'],'offset':offset})

    def parse_question(self,response):
        list_item = response.xpath('//div[@class="List-item"]')
        for one in list_item:
            item = QuestionItem()
            item['ask_user_id'] = response.meta['ask_user_id']
            title = one.xpath('.//div[@class="QuestionItem-title"]')
            item['title'] = title.xpath('./a/text()').extract()[0]
            item['question_id'] = title.xpath('./a/@href').extract()[0].replace('/question/','')
            content_item = one.xpath('.//div[@class="ContentItem-status"]//span/text()').extract()
            item['ask_time'] = content_item[0]
            item['answer_count'] = content_item[1]
            item['followees_count'] = content_item[2]
            yield item
        next_page = response.xpath('//button[@class="Button PaginationButton PaginationButton-next Button--plain"]/text()').extract()
        if next_page:
            response.meta['page'] += 1
            next_url = re.findall('(.*page=)\d+',response.url)[0] + str(response.meta['page'])
            yield Request(next_url,callback=self.parse_question,meta={'ask_user_id':response.meta['ask_user_id'],'page':response.meta['page']})

    def parse_article(self,response):
        json_result = str(response.body,encoding="utf8").replace('false','0').replace('true','1')
        dict_result = eval(json_result)
        for one in dict_result['data']:
            item = ArticleItem()
            item['author_id'] = response.meta['author_id']
            item['title'] = one['title']
            item['article_id'] = one['id']
            item['content'] = one['content']
            #pdb.set_trace()
            item['cretated_time'] = one['created']
            item['updated_time'] = one['updated']
            item['voteup_count'] = one['voteup_count']
            item['comment_count'] = one['comment_count']
            yield item
        if dict_result['paging']['is_end'] == 0:
            offset = response.meta['offset'] + 20
            next_page = re.findall('(.*offset=)\d+',response.url)[0]
            yield Request(next_page + str(offset),callback=self.parse_article,meta={'author_id':response.meta['author_id'],'offset':offset})
