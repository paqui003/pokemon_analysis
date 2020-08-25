# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

import os

from itemadapter import ItemAdapter
import sqlite3
from sqlite3 import Error


class PokemonPipeline:

    # Called when spider has been opened
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
            print(os.getcwd())
            self.conn = sqlite3.connect("../database/pokemon.db")
            self.curr = self.conn.cursor()

        except Error as e:
            print(e)

    def create_table(self):

        pokemon_table = """ CREATE TABLE IF NOT EXISTS Pokemon (
                                        Dex INTEGER PRIMARY KEY,
                                        Name VARCHAR(128) NOT NULL,
                                        Hp INTEGER,
                                        Atk INTEGER,
                                        Def INTEGER,
                                        Satk INTEGER,
                                        Sdef INTEGER,
                                        Spd INTEGER,
                                        Total INTEGER,
                                        Height FLOAT,
                                        Weight FLOAT,
                                        Growthr VARCHAR(32),
                                        Catchr FLOAT,
                                        Gen VARCHAR(32),
                                        Legendary VARCHAR(16)
                                    ); """

        gender_table = """ CREATE TABLE IF NOT EXISTS Gender (
                                        Dex INTEGER PRIMARY KEY,
                                        Female BOOL,
                                        Male BOOL,
                                        Femaler FLOAT,
                                        Maler FLOAT,
                                        FOREIGN KEY (Dex) REFERENCES Pokemon(Dex)
                                    ); """

        types_table = """CREATE TABLE IF NOT EXISTS Type (
                                        Dex INTEGER,
                                        Type VARCHAR(16),
                                        PRIMARY KEY (Dex, Type),
                                        FOREIGN KEY (Dex) REFERENCES Pokemon(Dex)
                                    ); """


        try:
            self.curr.execute(pokemon_table)
            self.curr.execute(gender_table)
            self.curr.execute(types_table)

        except Error as e:
            print(e)

    def store_item(self, item):
        self.curr.execute("""INSERT OR IGNORE INTO Pokemon VALUES
        (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
          (
            item['_dex'],
            item['_name'],
            item['_hp'],
            item['_atk'],
            item['_def'],
            item['_satk'],
            item['_sdef'],
            item['_spd'],
            item['_total'],
            item['_height'],
            item['_weight'],
            item['_growthr'],
            item['_catchr'],
            item['_gen'],
            item['_legendary']
          ))

        self.curr.execute("""INSERT OR IGNORE INTO Gender VALUES (?, ?, ?, ?, ?)""",
          (
            item['_dex'],
            1 if (len(item['_gender']) > 1 and item['_genderr'][0] > 0) else 0,
            1 if (len(item['_gender']) > 1 and item['_genderr'][1] > 0) else 0,
            item['_genderr'][0] if len(item['_gender']) > 1 else 0.0,
            item['_genderr'][1] if len(item['_gender']) > 1 else 0.0
          ))

        for t in item['_types']:
            self.curr.execute("""INSERT OR IGNORE INTO Type VALUES (?, ?)""",
              (
                item['_dex'],
                t
              ))

        self.conn.commit()

    def process_item(self, item, spider):
        self.store_item(item)

        print("Pipeline: " + item["_name"])

        return item
