# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Pokemon(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    _name = scrapy.Field()
    _dex = scrapy.Field()

    _hp = scrapy.Field()
    _atk = scrapy.Field()
    _def = scrapy.Field()
    _satk = scrapy.Field()
    _sdef = scrapy.Field()
    _spd = scrapy.Field()
    _total = scrapy.Field()

    _gender = scrapy.Field()
    _height = scrapy.Field()
    _weight = scrapy.Field()

    _catchr = scrapy.Field()
    _growthr = scrapy.Field()

    _legendary = scrapy.Field()
