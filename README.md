# 知乎爬虫(scrapy默认配置下单机1小时可爬取60多万条数据)  
***
*版本*：1.0  
*作者*: AlexTan  
<<<<<<< HEAD

*CSDN*: [AlexTan_](http://blog.csdn.net/alextan_)  
*E-Mail* : <alextanbz@gmail.com>  
=======

*CSDN*: [AlexTan_](http://blog.csdn.net/alextan_)  
*E-Mail* : <alextanbz@gmail.com>  
***

## 原文博客：[ZhihuSpider](http://blog.csdn.net/AlexTan_/article/details/77057068)
### v2.0版本已加上布隆过滤器，建议切换到2.0版本（已测试完毕）
## 前言：

*在这里特别鸣谢: 九茶*  <http://blog.csdn.net/bone_ace>   Github: <https://github.com/LiuXingMing>

学了爬虫差不多快一年了，然而由于项目原因，这还是第一次发爬虫的博客，在学习的过程中，受益最大的就是看了九茶的微博爬虫吧，所以在这里特别鸣谢。 他的代码里涉及了很多：自动化技术、模拟登录、分布式、redis、mongodb等都有涉及，而且还讲了代码的可复用性，深受启发。 不过，对于爬虫的知识块儿来讲，还没涉及抓包（因为个人觉得，如果只抓取json数据的话，会比抓取普通网页速度来得快得多）、以及自动更换IP技术，于是在这里写一个知乎爬虫的博客，这篇博客里，除了九茶的微博爬虫所涉及的知识以外，还有抓包、以及更换ip技术。



## 环境：

1. Ubuntu16.04
2. Python环境是ubuntu自带的python3.5.2
3. 需要安装的软件Redis, MongoDB, Phantomjs;
4. 需要安装的python模块：scrapy, scrapy-redis, selenium, redis, pymongo
5. 电脑是用的小米笔记本4999元的那个版本，如果是台式机的话速度应该会更快。（ps:如果想更快，可以加大setting.py 中的 `CONCURRENT_REQUESTS`的值，这个值默认是16，可以调大，直到CPU使用率达到80-90%，相信速度会快很多，绝不仅仅是一分钟6000多条。当然也可以在单机上多进程爬取）



## 使用说明：

#### 环境已经安装好的情况下:
1. 打开cookie.py,填入你的知乎账号密码
2. 运行爬虫 ： `scrapy crawl zhishuspider` 即可
3. 分布式扩展：把代码考到新一台机器上，只需要把setting.py里的`REDIS_HOST`和`FILTER_HOST`改成主机的地址就好，其他的根据自己的具体情况修改。然后运行即可。
4. 提示：如果你的账号数量不够多，建议把`DOWNLOAD_DELAY`开启（即把代码里注释的那四行取消注释掉），数值多少根据自己具体情况更改。
#### docker版本（不限系统版本，建议在root用户下进行，代码已上传到github，可以自行切换到zhihu-docker版本查看）：
1.  `docker pull alextanbz/zhihuspider`  下载镜像

2.  `docker run -idt alextanbz/zhihuspider` 建立一个容器

3. `docker ps`  查看这个正在运行的容器id

4. `docker exec it container_id(容器id) bash` 进入容器，然后在cookie.py文件中填入你的知乎账号密码，在yundama.py中填入相应参数；如果数据库在其他主机上，可以进入setting.py修改一下redis和mongodb对应的ip，如果数据库在本机上则不需要。

5. `docker commit container_id(容器id) myzhihuspider` 保存修改

6. 最后运行`docker run myzhihuspider && scrapy crawl zhihuspider` 就可以了。 如果数据库是安装在主机上的话运行: `docker run --net=host  myzhihuspider && scrapy crawl zhihuspider` 

   **注意**: --net=host会把主机的端口暴露给容器，实际应用不建议使用此方法。实际应用建议 一下方法任选一种： 

   1. 使用docker安装数据库建立两个新的容器(当然也可能不止两个)，然后再通过Link在容器之间建立连接
   2. 或者有专门做存储的服务器，直接进入setting.py改对应的ip就可以了。



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
>>>>>>> 1a058ac73fbce8dec4e9a0685caac12672d104b7

***

## 原文博客：[ZhihuSpider](http://blog.csdn.net/AlexTan_/article/details/77057068)


<<<<<<< HEAD
## 前言：
=======
### AnswerItem（回答）：
>>>>>>> 1a058ac73fbce8dec4e9a0685caac12672d104b7

发现github上有人问运行不起来，可能由于环境配置太过繁琐，所以在这里写一个docker版本的（同时也是自身的学习），直接pull，添加上必要的账号就可以运行起来。 不过由于代码中涉及个人密码之类的所以就没有push直接可以使用的版本，需要去容器里面自己配置账号和密码，以及云打码平台的必要参数才可以运行，数据是存到mongodb数据库的，还使用了redis数据库(支持去重[布隆过滤器]、断点续爬、分布式爬取功能)，如需工程性的使用请自己配置好数据库，如何配置下面会详细说明。



## 环境：

1. 本人使用的是ubuntu16.04，其他系统暂未测试，只要装上docker，数据库配置好应该都能用。

2. docker（安装和配置国内加速器，阿里云有很详细的教程：<https://account.aliyun.com/login/login.htm?oauth_callback=https%3A%2F%2Fcr.console.aliyun.com%2F%3Fspm%3D5176.1971733.0.2.5q2Lwj&lang=zh#/accelerator>  进去后点击"Docker Hub站点",很简单，速度也很快，这里就不详细说明了）

3. 本地测试或者把数据存到本地数据库可以本地主机安装mongodb(sudo apt-get install mongodb)以及redis(sudo apt-get install redis-server)数据库；如果工程性的使用建议用docker安装数据库，然后使用Link在容器之间建立连接，详细文档这里也不过多阐述了（如有不会的朋友们请在issues里提问，我会补上文档）。

   #### 我的测试环境：

   1. Ubuntu16.04
   2. 阿里云安装的docker，以及配置了加速器
   3. sudo apt-get install mongodb 以及 sudo apt get install redis-server（主机上安装的数据库）



## 使用说明(建议在root用户下进行)：

1.  `docker pull alextanbz/zhihuspider`  下载镜像

2.  `docker run -idt alextanbz/zhihuspider` 建立一个容器

3. `docker ps`  查看这个正在运行的容器id

4. `docker exec it container_id(容器id) bash` 进入容器，然后在cookie.py文件中填入你的知乎账号密码，在yundama.py中填入相应参数；如果数据库在其他主机上，可以进入setting.py修改一下redis和mongodb对应的ip，如果数据库在本机上则不需要。

5. `docker commit container_id(容器id) myzhihuspider` 保存修改

6. 最后运行`docker run myzhihuspider && scrapy crawl zhihuspider` 就可以了。 如果数据库是安装在主机上的话运行: `docker run --net=host  myzhihuspider && scrapy crawl zhihuspider` 

   **注意**: --net=host会把主机的端口暴露给容器，实际应用不建议使用此方法。实际应用建议 一下方法任选一种： 

   1. 使用docker安装数据库建立两个新的容器(当然也可能不止两个)，然后再通过Link在容器之间建立连接
   2. 或者有专门做存储的服务器，直接进入setting.py改对应的ip就可以了。


## 总结:

出这个docker的版本目的是想简化安装过程，但因为账号密码的原因感觉也没简化多少步骤。主要还是在于学习嘛，大家如果有什么问题欢迎留言！