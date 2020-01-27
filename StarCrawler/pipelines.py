# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import requests
import os
from scrapy.exceptions import DropItem
import pymysql

class StarcrawlerPipeline(object):
    def __init__(self):
        # 查重
        self.nameSeen = set()

        # 先创建文件路径
        self.file_dir = r"C:\StarPic"
        # 判断文件路径是否存在，如果不存在，则创建
        if not os.path.isdir(self.file_dir):
            os.makedirs(self.file_dir)

        # 创建数据表格
        self.conn = pymysql.connect(host="localhost", user="root", password="19990710", charset="utf8mb4")
        self.cursor = self.conn.cursor()
        # 创建starinfo 数据库, 如果存在则删除starinfo 数据库
        self.cursor.execute("DROP DATABASE IF EXISTS STARINFO")
        self.cursor.execute("CREATE DATABASE STARINFO")
        #选择 starinfo 这个数据库
        self.cursor.execute("USE STARINFO")
        # 如果数据表已经存在使用 execute() 方法删除表。
        sql = """DROP TABLE IF EXISTS INFO"""
        self.cursor.execute(sql)
        sql = """CREATE TABLE INFO (
                ID  INT PRIMARY KEY,
                NAME  CHAR(20),
                NATION CHAR(20),  
                BIR CHAR(20),
                URL CHAR(255) )"""
        self.cursor.execute(sql)
        sql = """ALTER TABLE INFO CONVERT TO CHARACTER SET utf8mb4"""
        self.cursor.execute(sql)

    def __del__(self):
        self.cursor.close()
        self.conn.close()

    def process_item(self, item, spider):
        if item['name'] in self.nameSeen:
            raise DropItem("Duplicate item found: %s" % item['name'])
        else:
            self.nameSeen.add(item['name'])

            self.cursor.execute("""INSERT INTO INFO (ID, NAME, NATION, BIR, URL) VALUES (%s, %s, %s, %s, %s)""",
            (item['id'], item['name'], item['nation'], item['bir'], item['url']))
            # 提交到数据库执行
            self.conn.commit()

            if item['pic'] != "":
                filename = self.file_dir + "\\" + str(item['id']) + "_" + item['name'] + "." + item['pic'].split(".")[-1]
                with open(filename, "wb") as f:
                    f.write(requests.get(item['pic']).content)

        return item
