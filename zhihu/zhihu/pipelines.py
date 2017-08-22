# -*- coding: utf-8 -*-
import pymongo
import pdb
from .items import ZhihuItem,RelationItem,AnswerItem,QuestionItem,ArticleItem

# ------------------------------------------
#   版本：1.0
#   日期：2017-8-06
#   作者：AlexTan
#   <CSDN:   http://blog.csdn.net/alextan_>  
#   <e-mail: alextanbz@gmail.com>
# ------------------------------------------


class ZhihuPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls,crawler):
        return cls(
                mongo_uri = crawler.settings.get('MONGO_URI'),
                mongo_db = crawler.settings.get('MONGO_DATABASE','zhihu')
            )

    def open_spider(self,spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self,spider):
        self.client.close()

    def process_item(self, item, spider):
        if isinstance(item, ZhihuItem):
            self._process_user_item(item)
        elif isinstance(item, AnswerItem):
            self._process_answer_item(item)
        elif isinstance(item, QuestionItem):
            self._process_question_item(item)
        elif isinstance(item, ArticleItem):
            self._process_article_item(item)
        else:
            #pdb.set_trace()
            self._process_relation_item(item)
        return item

    def _process_user_item(self,item):
        self.db.UserInfo.insert(dict(item))

    def _process_relation_item(self,item):
        try:
            isnext,relation_type = item['relation_type'].split(':')
            if isnext == 'next':
                for one in item['relations_id']:
                    #pdb.set_trace()
                    self.db.Relation.update({'user_id':item['user_id'],'relation_type':relation_type},{"$push":{'relations_id':one}})
        except:
            self.db.Relation.insert(dict(item))

    def _process_answer_item(self,item):
        self.db.AnswerInfo.insert(dict(item))

    def _process_question_item(self,item):
        self.db.QuestionInfo.insert(dict(item))

    def _process_article_item(self,item):
        self.db.ArticleInfo.insert(dict(item))
