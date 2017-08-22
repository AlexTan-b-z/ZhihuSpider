# 知乎爬虫(scrapy默认配置下单机1小时可爬取60多万条数据)  
***
*版本*：2.0  
*作者*: AlexTan  

*CSDN*: [AlexTan_](http://blog.csdn.net/alextan_)  
*E-Mail* : <alextanbz@gmail.com> 
***

## 原文博客：[ZhihuSpider](http://blog.csdn.net/AlexTan_/article/details/77057068)



## 更新日志：

* 2017.08.17: v2.0版本 对scrapy_redis进行优化，修改了scrapy-redis的去重机制（加了布隆过滤器）。更新原因： v1.0版本运行两到三天就会把内存（16G的服务器）占满。 更新后，V2.0版本，运行3天，只会占大概2到3G内存（几乎不会增长）。

* 2017.08.22: 对三个版本的 pipline 和 spider 两个文件都修改了一下。因为以前RelationItem插入mongo时，next的数据会随机插入到粉丝或者关注里，导致数据会发生错误。 现已修正。

## 关于redis:
如果要持久运行，建议修改一下redis.conf文件，ubuntu默认在 `/etc/redis/redis.conf` 下:
1. 把 maxmemory 设置成你内存的 3/4
2. 把 maxmemory-policy 设置成 allkeys-lru

### 最后建议多弄几个账号运行，目测78个就足够了。


## 原文博客：[ZhihuSpider](http://blog.csdn.net/AlexTan_/article/details/77057068)


***

最后，欢迎大家提出问题，共同学习！！！
