# 知乎爬虫(scrapy默认配置下单机1小时可爬取60多万条数据)  
***
*版本*：1.0  
*作者*: AlexTan  
<CSDN   :   http://blog.csdn.net/alextan_ >  
<E-Mail : alextanbz@gmail.com >  
***


## 前言：

*在这里特别鸣谢: 九茶*  <http://blog.csdn.net/bone_ace>   <Github: https://github.com/LiuXingMing> 

学了爬虫差不多快一年了，然而由于项目原因，这还是第一次发爬虫的博客，在学习的过程中，受益最大的就是看了九茶的微博爬虫吧，所以在这里特别鸣谢。 他的代码里涉及了很多：自动化技术、模拟登录、分布式、redis、mongodb等都有涉及，而且还讲了代码的可复用性，深受启发。 不过，对于爬虫的知识块儿来讲，还没涉及抓包（因为个人觉得，如果只抓取json数据的话，会比抓取普通网页速度来得快得多）、以及自动更换IP技术，于是在这里写一个知乎爬虫的博客，这篇博客里，除了九茶的微博爬虫所涉及的知识以外，还有抓包、以及更换ip技术。



## 环境：

1. Ubuntu16.04
2. Python环境是ubuntu自带的python3.5.2
3. 需要安装的软件Redis, MongoDB, Phantomjs;
4. 需要安装的python模块：scrapy, scrapy-redis, selenium
5. 电脑是用的小米笔记本4999元的那个版本，如果是台式机的话速度应该会更快。（ps:如果想更快，可以加大setting.py 中的 `CONCURRENT_REQUESTS`的值，这个值默认是16，可以调大，直到CPU使用率达到80-90%，相信速度会快很多，绝不仅仅是一分钟6000多条。当然也可以在单机上多进程爬取）



## 使用说明：

1. 打开cookie.py,填入你的知乎账号密码
2. 运行爬虫 ： `scrapy crawl zhishuspider` 即可
3. 分布式扩展：把代码考到新一台机器上，只需要把setting.py里的`REDIS_HOST`和`FILTER_HOST`改成主机的地址就好，其他的根据自己的具体情况修改。然后运行即可。
4. 提示：如果你的账号数量不够多，建议把`DOWNLOAD_DELAY`开启（即把代码里注释的那四行取消注释掉），数值多少根据自己具体情况更改。



## 代码说明：

1. 爬虫基于scrapy+redis架构进行开发、优化。
2. 爬虫支持断点续爬。
3. 非常简易地，便可实现分布式扩展。
4. 使用Redis的“位”进行去重，1G的内存可满足80亿个用户ID的瞬间去重。
5. 将种子优化到不足40个字符，大大降低了Redis的内存消耗，也提高了各子爬虫从Redis取种子的速度。
6. 维护了一个Cookie池，各子机器共用一个Cookie池，断点续爬不会重复获取Cookie，当某个Cookie失效时会自动更新。
7. 直接爬取通过抓包得到的json格式的链接，请求速度更快、爬取速度更快。**单机一小时可爬取60多万条数据**
8. 代码中自带proxy（自动更换ip），但并未启用，经测试，只要账号数量够多，暂不需要启用，如需启用，请自行购买代理ip，并修改代码proxy.py中`GetIPPOOLS()`函数（我是用的大象代理，5元20000个，不是广告，挺便宜，但真心觉得不咋好用，每十个ip差不多有一个能用(延迟在2s内)），如果你是用的大象代理，就不需要修改代码。
9. 支持手动识别验证码和自动识别验证码，如需自动登录，请自行购买云打码平台账号。默认启动的是手动识别，需要手动输入验证码。如果你想自己写个代码识别验证码，那也是可以的。



## 爬取内容：

1. 用户的个人信息以及粉丝和关注的人（可以生成用户的拓扑关系图）
2. 用户的回答
3. 用户的提问
4. 文章



## 爬取字段：

### ZhihuItem（用户个人信息）:

| 字段名            | 含义     |
| -------------- | ------ |
| user_id        | 用户id   |
| user_image_url | 用户头像链接 |
| name           | 用户昵称   |
| locations      | 用户住址   |
| business       | 用户所在行业 |
| employments    | 用户职业经历 |
| gender         | 用户性别   |
| education      | 用户教育经历 |
| followees_num  | 用户关注数  |
| followers_num  | 用户粉丝数  |



### RelationItem（关系）:

| 字段名           | 含义      |
| ------------- | ------- |
| user_id       | 用户id    |
| relation_type | 关系类型    |
| relations_id  | 关系的人的id |



###AnswerItem（回答）：

| 字段名            | 含义      |
| -------------- | ------- |
| answer_user_id | 回答的用户   |
| answer_id      | 回答内容的id |
| question_id    | 问题的id   |
| cretated_time  | 创建的时间戳  |
| updated_time   | 更新的时间戳  |
| voteup_count   | 赞成数     |
| comment_count  | 评论数     |
| content        | 回答内容    |



### QuestionItem（问题）:

| 字段名             | 含义     |
| --------------- | ------ |
| ask_user_id     | 提问人的id |
| question_id     | 问题的id  |
| ask_time        | 提问时间   |
| answer_count    | 回答数量   |
| followees_count | 关注数量   |
| title           | 提问标题   |



### ArticleItem（文章）:

| 字段名           | 含义    |
| ------------- | ----- |
| author_id     | 作者id  |
| title         | 文章标题  |
| article_id    | 文章id  |
| content       | 文章内容  |
| cretated_time | 创建时间戳 |
| updated_time  | 更新时间戳 |
| voteup_count  | 赞成数   |
| comment_count | 评论数   |





## 关于抓包获取到的几个链接问题：

未登录状态下需要`Authorization`才能访问json数据的链接，带登录后的cookie访问就不需要了。

`Authorization`可以通过访问任意一个用户页面在请求json数据链接中的header中获取，建议通过模拟浏览器的方式获取，不过如果登陆了就不需要了，故代码中没有获取`Authorization`



***

最后，欢迎大家提出问题，共同学习！！！



