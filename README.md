# Spider_jobbole
### 这是一个爬虫项目
### 目的：获取帖子中的主要信息，并存储在本地数据库中
### 所用技术
* scrapy
  1. item
  2. itemLoader
  3. pipelines
* mysqlclient(pymysql也可以)
* Twisted异步
  1. adbapi创建连接池，避免阻塞
### 运行环境
需要搭建Scrapy框架以及数据库模块
### 结果
![image](https://github.com/ericyishi/img-folder/blob/master/spider/jobbole/captureForDB.png)



