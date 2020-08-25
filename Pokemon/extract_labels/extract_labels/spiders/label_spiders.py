import scrapy
import requests
import logging

from ..items import PokemonLabel


class LabelSpider(scrapy.Spider):
    name = "labelSpider"
    start_urls = [
        "https://www.serebii.net/pokemon/legendary.shtml",
    ]

    def parse(self, response):
        """
        Parse https://www.serebii.net/pokemon/legendary.shtml and extract
        the links grouped by legendary, semi-legendary and mythic pokemon.
        Follow each link to a Pokemon's page.

        Parameters:
            response    --    The HTML-Structure and HTTP-Code.

        Returns:

            Yields a respone.follow(...) object.

        """
        # Pokemon are contained inside a nested table structure, that is
        # each Pokemon is represented as a table within the parent table.
        subleg_pokemon =  response.xpath("//table[tr[contains(., 'Sub-Legendary')]]/tr/td/table")
        # First link references to the Pokemon's page.
        subleg_links = [a.xpath("./tr/td/a")[0] for a in subleg_pokemon]
        subleg_links = [link.xpath("./@href").get() for link in subleg_links]

        leg_pokemon =  response.xpath("//table[tr[contains(., 'Legendary')]]/tr/td/table")
        leg_links = [a.xpath("./tr/td/a")[0] for a in leg_pokemon]
        leg_links = [link.xpath("./@href").get() for link in leg_links]

        myth_pokemon =  response.xpath("//table[tr[contains(., 'Mythical')]]/tr/td/table")
        myth_links = [a.xpath("./tr/td/a")[0] for a in myth_pokemon]
        myth_links = [link.xpath("./@href").get() for link in myth_links]

        for a in subleg_links:
            yield response.follow(a, callback=self.parse_subLegendary)

        for a in leg_links:
            yield response.follow(a, callback=self.parse_legendary)

        for a in myth_links:
            yield response.follow(a, callback=self.parse_mythic)

    def parse_subLegendary(self, response):

        pokeLabel = PokemonLabel()

        dex_data = response.xpath("//td[@class='fooinfo']/table/tr[contains(., 'National')]/td")[1]
        dex = dex_data.xpath("text()").get() #contains dex entry in format '#xyz'

        pokeLabel["_dex"] = dex
        pokeLabel["_label"] = "Sub-Legendary"

        yield pokeLabel

    def parse_legendary(self, response):

        pokeLabel = PokemonLabel()

        dex_data = response.xpath("//td[@class='fooinfo']/table/tr[contains(., 'National')]/td")[1]
        dex = dex_data.xpath("text()").get() #contains dex entry in format '#xyz'

        pokeLabel["_dex"] = dex
        pokeLabel["_label"] = "Legendary"

        yield pokeLabel

    def parse_mythic(self, response):

        pokeLabel = PokemonLabel()

        dex_data = response.xpath("//td[@class='fooinfo']/table/tr[contains(., 'National')]/td")[1]
        dex = dex_data.xpath("text()").get() #contains dex entry in format '#xyz'

        pokeLabel["_dex"] = dex
        pokeLabel["_label"] = "Mythical"

        yield pokeLabel
