# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PokemonLabel(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    _dex = scrapy.Field()    #Dex Number of the pokemon
    _label = scrapy.Field()  #Label (Legendary, Semi, Mythic)
