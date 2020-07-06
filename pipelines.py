# -*- coding: utf-8 -*-

# Define your item pipelines here
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql


class JdspiderPipeline(object):
    def __init__(self):
        self.f = open('user.txt', 'a', encoding='utf-8')
        self.fp = open('content.txt', 'a', encoding='utf-8')

    def process_item(self, item, spider):
        if 'title' in str(item):
            self.f.write(str(item) + '\n')
        elif 'content' in str(item):
            self.fp.write(str(item) + '\n')
        return item

    def close_spider(self, spider):
        self.f.close()
        self.fp.close()


class JdspiderMySQLPipeline(object):

    def __init__(self):
        self.client = pymysql.connect(
            host='47.115.21.129',
            port=3306,
            user='root',  # 使用自己的用户名
            passwd='111111',  # 使用自己的密码
            db='JDSpider',  # 数据库名
            charset='utf8')
        self.cursor = self.client.cursor()

    def process_item(self, item, spider):
        if 'title' in str(item):
            sql = 'insert into user(title, price, productId) values (%s,%s,%s)'
            lis = (item['title'], item['price'], item['productId'])
            self.cursor.execute(sql, lis)
            self.client.commit()
        if 'content' in str(item):
            sql = """insert into newcomments(content, productId ,score ) values (%s,%s ,%s)"""
            lis = (item['content'], item['productId'], item['score'])
            self.cursor.execute(sql, lis)
            self.client.commit()
        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.client.close()
