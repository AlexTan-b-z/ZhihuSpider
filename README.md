# 知乎爬虫(scrapy默认配置下单机1小时可爬取60多万条数据)  
***
*版本*：2.0  
*作者*: AlexTan  

*CSDN*: [AlexTan_](http://blog.csdn.net/alextan_)  
*E-Mail* : <alextanbz@gmail.com> 
***

## 原文博客：[ZhihuSpider](http://blog.csdn.net/AlexTan_/article/details/77057068)



## 更新日志：
* 2017.12.18：v2.0版本，修改spider，解决了 爬虫运行过久由于一些特殊原因把redis里的待爬取requests队列里的Request都耗尽，从而导致重新运行爬虫时start_requests里的request都被dupefilter过滤掉 的问题。

* 2017.11.21:v2.0版本 对proxy.py进行了优化，使每个ip的权值都不会超过10，避免出现有的ip权值无限增长，失效后要等很久才能删掉失效ip的问题。

* 2017.10.08: v2.0版本 对ip代理池（中间件）进行了优化(知乎爬虫用不上，这个中间件可以移植到其他爬虫去，只对知乎爬虫有需求的可以无视)，由于上次那个代理ip过期了，这次用的讯代理，感觉比上次那个代理好用多了，有效率在95%左右。但是缺点就是优质版每次只能提取20个，每天最多提取1000个。以前那个换ip的代码会误删很多并没有失效的ip，所以这次代码就对ip进行了加权(status)处理。默认权值为10，一次访问失败会减一，访问成功会加一，当权值小于1的时候，删除该ip。

* 2017.08.22: 对三个版本的 pipline 和 spider 两个文件都修改了一下。因为以前RelationItem插入mongo时，next的数据会随机插入到粉丝或者关注里，导致数据会发生错误。 现已修正。同时，有人说到如果启用代理ip，获取ip那儿会造成堵塞，这次在获取代理ip那儿加了个多线程，解决了堵塞问题。

* 2017.08.17: v2.0版本 对scrapy_redis进行优化，修改了scrapy-redis的去重机制（加了布隆过滤器）。更新原因： v1.0版本运行两到三天就会把内存（16G的服务器）占满。 更新后，V2.0版本，运行3天，只会占大概2到3G内存（几乎不会增长）。


## 关于redis:
如果要持久运行，建议修改一下redis.conf文件，ubuntu默认在 `/etc/redis/redis.conf` 下:
1. 把 maxmemory 设置成你内存的 3/4
2. 把 maxmemory-policy 设置成 allkeys-lru

### 最后建议多弄几个账号运行，目测78个就足够了。


## 原文博客：[ZhihuSpider](http://blog.csdn.net/AlexTan_/article/details/77057068)


***

最后，欢迎大家提出问题，共同学习！！！
