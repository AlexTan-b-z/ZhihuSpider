# 知乎爬虫(scrapy默认配置下单机1小时可爬取60多万条数据)  
***
*版本*：1.0  
*作者*: AlexTan  

*CSDN*: [AlexTan_](http://blog.csdn.net/alextan_)  
*E-Mail* : <alextanbz@gmail.com>  
***

## 原文博客：[ZhihuSpider](http://blog.csdn.net/AlexTan_/article/details/77057068)



## 前言：
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