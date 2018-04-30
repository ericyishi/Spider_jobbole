# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi


class ArticalspiderPipeline(object):
    def process_item(self, item, spider):
        return item


class MysqlTwistedPipline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    # 会在初始化的时候将setting.py文件传进来，这样就可以取里面的所有内容了
    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
                host=settings["MYSQL_HOST"],
                db=settings["MYSQL_DBNAME"],
                user=settings["MYSQL_USER"],
                passwd=settings["MYSQL_PASSWORD"],
                charset='utf8',
                cursorclass=MySQLdb.cursors.DictCursor,
                use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)

        return cls(dbpool)

    def process_item(self, item, spider):
        # 使用twisted将mysql插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider)  # 处理异常

    def handle_error(self, failure, item, spider):
        # 处理异步插入的异常
        print(failure)

    def do_insert(self, cursor, item):
        # 执行具体的插入

        insert_sql = """
            insert into posts_spider(title, create_date,url,url_object_id, front_image_url,praise_nums, comment_nums,fav_nums,tags,content)
            VALUES (%s, %s, %s, %s,%s,  %s, %s,%s, %s, %s)
        """
        print(item["title"])
        print(item["create_date"])
        print(item["url"])
        print(item["url_object_id"])
        print(item["front_image_url"])

        print(item["praise_nums"])
        print(item["comment_nums"])
        print(item["fav_nums"])
        print(item["tags"])
        print(item["content"])
        cursor.execute(insert_sql, (
        item["title"], item["create_date"], item["url"], item["url_object_id"], item["front_image_url"],
        item["praise_nums"], item["comment_nums"], item["fav_nums"], item["tags"],
        item["content"]))
