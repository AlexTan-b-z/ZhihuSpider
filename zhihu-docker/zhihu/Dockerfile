FROM ubuntu:16.04

WORKDIR /app

COPY install.sh /app/install.sh
COPY scrapy.cfg /app/scrapy.cfg
COPY ./zhihu /app/zhihu
COPY sources.list /etc/apt/
COPY ./phantomjs-2.1.1-linux-x86_64 /usr/local/src/phantomjs
RUN ln -sf /usr/local/src/phantomjs/bin/phantomjs /usr/local/bin/phantomjs
RUN /app/install.sh

EXPOSE 6379
EXPOSE 27017
