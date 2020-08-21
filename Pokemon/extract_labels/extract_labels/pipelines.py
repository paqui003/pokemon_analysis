# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

import os

from itemadapter import ItemAdapter
import sqlite3
from sqlite3 import Error


class LabelPipeline:

    #Called when spider has been opened
    def open_spider(self, spider):
        self.create_connection()
        self.create_table()


    def close_spider(self, spider):
        try:
            self.conn.close()
        except Error as e:
            print(e)

    def create_connection(self):
        try:
            self.conn = sqlite3.connect("../database/pokemon.db")
            self.curr = self.conn.cursor()

        except Error as e:
            print(e)

    def create_table(self):

        label_table = None #TODO: Create the table Label here if it does not already
                           # exist.

        try:
            self.curr.execute(label_table)

        except Error as e:
            print(e)

    def store_item(self, item):

        self.curr.execute("""INSERT OR IGNORE INTO Label VALUES (?, ?)""",
        (
        #TODO: Fill in the columns with the content of item
        ))

        self.conn.commit()

    def process_item(self, item, spider):
        self.store_item(item)

        print("Pipeline: " + item["_name"])

        return item
