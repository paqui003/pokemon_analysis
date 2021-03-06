# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import sqlite3
from sqlite3 import Error

class PokemonPipeline:

    def __init__(self):
        pass

    def open_spider(self, spider):
        pass



    def close_spider(self, spider):
        pass

    def create_connection(self):
        try:
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
                                        Male BOOL,
                                        Female BOOL,
                                        Maler FLOAT,
                                        Femaler FLOAT,
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

    def process_item(self, item, spider):
        #TODO:   Check what happens with different process functions.
        #        #parse vs. parse_pokemon
        #print(item)
        #print(spider)
        return item
