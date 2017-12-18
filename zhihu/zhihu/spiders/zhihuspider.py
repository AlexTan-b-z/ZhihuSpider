# -*- coding: utf-8 -*-
import scrapy
import re
import pdb
import json
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from ..items import ZhihuItem,RelationItem
from scrapy.http import Request,FormRequest
from scrapy_redis.spiders import RedisSpider

# ------------------------------------------
#   版本：1.0
#   日期：2017-8-06
#   作者：AlexTan
#   <CSDN:   http://blog.csdn.net/alextan_>  
#   <e-mail: alextanbz@gmail.com>
# ------------------------------------------


#zhihuspider1是模拟浏览器爬（速度慢,不建议，仅供学习） zhihuspider0抓包爬（速度快）
class ZhihuspiderSpider(RedisSpider):
#class ZhihuspiderSpider(scrapy.Spider):
    name = "zhihuspider1"
    #allowed_domains = ["zhihu.com"]
    host = 'https://www.zhihu.com'
    redis_key = "zhihuspider:start_urls"
    #start_urls = ['https://www.zhihu.com/people/yun-he-shu-ju-8/answers']
    strat_user_id = ['yun-he-shu-ju-8']
    #pdb.set_trace()
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0")
    dcap["phantomjs.page.settings.loadImages"] = False
    obj = webdriver.PhantomJS(desired_capabilities=dcap)


    def start_requests(self):
        for one in self.strat_user_id:
            yield Request('https://www.zhihu.com/people/'+one+'/answers',callback=self.parse,dont_filter=True)
        #return [Request('https://www.zhihu.com/#signin',callback=self.start_login,meta={'cookiejar':1})] #这个登录已不可用，仅供学习

    def start_login(self,response):
        xsrf = response.xpath('//input[@name="_xsrf"]/@value').extract_first()
        return [FormRequest('https://www.zhihu.com/login/phone_num',method='POST',meta={'cookiejar':response.meta['cookiejar']},formdata={
                #'_xsrf':xsrf,
                'password':'feifengwind',
                'remember_me':"true",
                'phone_num':'18983848805'},
                callback=self.after_login
                )]

    def after_login(self,response):
        pdb.set_trace()
        if json.loads(response.body)['msg'].encode('utf8') == "登录成功":
            self.logger.info("登录成功！%s" % str(response.meta['cookiejar']))
            print("登录成功！")
            self.obj.add_cookie(response.meta['cookiejar'])
            for one in self.strat_user_id:
                yield Request('https://www.zhihu.com/people/'+one+'/answers',meta={'cookiejar':response.meta['cookiejar']},callback=self.parse)
        else:
            self.logger.error('登录失败')

    def __del__(self):
        self.obj.quit()

    def parse(self, response):
        item = ZhihuItem()
        name = response.xpath('//span[@class="ProfileHeader-name"]/text()').extract()[0]
        #pdb.set_trace()
        user_image_url = response.xpath('//img[@class="Avatar Avatar--large UserAvatar-inner"]/@srcset').extract()[0].replace(' 2x','')
        user_id = re.findall('people\/(.*?)\/',response.url)[0]
        gender_icon = response.xpath('.//svg[@class="Icon Icon--male" or @class="Icon Icon--female"]/@class').extract()
        #pdb.set_trace()
        gender = ""
        if gender_icon:
            if gender_icon[0] == "Icon Icon--female":
                gender = "女"
            elif gender_icon[0] == "Icon Icon--male":
                gender = "男"
        item['name'] = name
        item['user_id'] = user_id
        item['user_image_url'] = user_image_url
        item['gender'] = gender
        try:
            num = response.xpath('//div[@class="NumberBoard-value"]/text()').extract()
            item['followees_num'] = num[0]
            item['followers_num'] = num[1]
            followees_url = response.url.replace('answers','following')
            followers_url = response.url.replace('answers','followers')
            relation_item = RelationItem()
            relation_item['relations_id'] = []
            relation_item['user_id'] = user_id
            relation_item['relation_type'] = 'followees'
            yield Request(followees_url,callback=self.relations,meta={'page':1,'item':relation_item})
            relation_item['relation_type'] = 'followers'
            yield Request(followers_url,callback=self.relations,meta={'page':1,'item':relation_item})
        except:
            print("需要登录！")

        self.obj.get(response.url)
        try:
            self.obj.find_element_by_class_name('ProfileHeader-expandButton').click()
            first = self.obj.find_elements_by_xpath('//div[@class="ProfileHeader-detailItem"]')
            for one in first:
                label = one.find_element_by_class_name('ProfileHeader-detailLabel').text
                if label == "居住地":
                    location = one.find_element_by_class_name('ProfileHeader-detailValue').text.replace('\n',',')
                    item['location'] = location
                elif label == "所在行业" or "行业":
                    business = one.find_element_by_class_name('ProfileHeader-detailValue').text.replace('\n',',')
                    item['business'] = business
                elif label == "职业经历":
                    professional = one.find_element_by_class_name('ProfileHeader-detailValue').text.replace('\n',',')
                    item['professional'] = professional
                elif label == "教育经历":
                    education = one.find_element_by_class_name('ProfileHeader-detailValue').text.replace('\n',',')
                    item['education'] = education
                else:
                    pass
        except:
            pass
        yield item

    def relations(self,response):
        self.obj.get(response.url)
        followees_a = self.obj.find_elements_by_xpath('//a[@class="UserLink-link"]')
        #pdb.set_trace()
        #followees_a = response.xpath('//a[@class="UserLink-link"]/@href').extract()
        followees = []
        for one in followees_a:
            try:
                one = one.get_attribute('href')
                followees.append(one.replace('https://www.zhihu.com/people/',''))
            except:
                pass
        followees = list(set(followees))
        #pdb.set_trace()
        response.meta['item']['relations_id']+=followees
        nextpage_button = response.xpath('//button[@class="Button PaginationButton PaginationButton-next Button--plain"]').extract()
        if nextpage_button:
            #pdb.set_trace()
            nextpage_url = response.url.replace('?page='+str(response.meta['page']),'') + "?page=" + str(response.meta['page']+1)
            yield Request(nextpage_url,callback=self.relations,meta={'page':response.meta['page']+1,'item':response.meta['item']})
        else:
            yield response.meta['item']
            for user in followees:
                yield Request('https://www.zhihu.com/people/'+user+'/answers',callback=self.parse)
