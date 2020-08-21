import scrapy
import requests
from ..items import Pokemon

import logging
LOG_FILENAME = 'pokemon.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG, filemode = "w")

 #table = response.xpath("//table[@id='pokedex']/tbody/tr")
#l = [entry.xpath("td") for entry in table]
 #_id, _name, _type, _total, _hp, _atk, _def, _satk, _sd, _spd = l[0]
class PokemonSpider(scrapy.Spider):
    name = "pokemon"
    start_urls = [
        "https://pokemondb.net/pokedex/all",
    ]


    def parse(self, response):
        dexTable = response.xpath("//table[@id='pokedex']/tbody")
        pokeLinks = dexTable.xpath("tr/td/a[@class='ent-name']")

        for a in pokeLinks.xpath("@href").getall():
            yield response.follow(a, callback=self.parse_pokemon)

    def parse_pokemon(self, response):
        import re
        import numpy as np

        pokeItem = Pokemon()

        main = response.xpath("//main")
        tables = main.xpath("//table[@class='vitals-table']/tbody")

        pokeItem["_name"] =  main.xpath("./h1/text()").get()
        pokeItem["_dex"] = tables.xpath("tr[contains(.,'National')]/td/strong/text()").get()


        height_raw = tables.xpath("tr[contains(.,'Height')]/td/text()").get()
        weight_raw = tables.xpath("tr[contains(.,'Weight')]/td/text()").get()


        try:
            pokeItem["_height"] = float(re.findall("[0-9]*\.[0-9]*", height_raw)[0])
            pokeItem["_weight"] = float(re.findall("[0-9]*\.[0-9]*", weight_raw)[0])
        except:
            pokeItem["_height"] = -1.0
            pokeItem["_weight"] = -1.0

        gender_raw = tables.xpath("tr[./th[contains(.,'Gender')]]/td/span/text()").getall()
        uniqueGender = np.unique(gender_raw)

        genders = [re.findall("[a-zA-Z]+", item)[0] for item in uniqueGender]
        gender_rates = [re.findall("[0-9]*\.*[0-9]*", item)[0] for item in uniqueGender]

        if len(genders) > 1:
            tmp = [i for i in zip(genders, gender_rates)]
            tmp = sorted(tmp, key = lambda x: x[0])
            genders, gender_rates = zip(*tmp)

            del tmp

        pokeItem["_gender"] = genders if len(genders) else ["-1", "-1"]

        pokeItem["_genderr"] = [float(rate) for rate in gender_rates] if len(gender_rates) > 1 else [0, 0]

        types = tables.xpath("tr[./th[contains(.,'Type')]]/td/a/text()").getall()

        uniqueTypes = np.unique(types)

        cond = (len(types) > 1) and (types[0] != types[1])
        uniqueTypes = uniqueTypes[:2] if (cond == True) else uniqueTypes

        pokeItem["_types"] = uniqueTypes

        pokeItem["_hp"] = float(tables.xpath("tr[./th[contains(.,'HP')]]/td/text()").get())
        pokeItem["_atk"] = float(tables.xpath("tr[./th[contains(.,'Attack')]]/td/text()").get())
        pokeItem["_def"] = float(tables.xpath("tr[./th[contains(.,'Defense')]]/td/text()").get())
        pokeItem["_satk"] = float(tables.xpath("tr[./th[contains(.,'Sp. Atk')]]/td/text()").get())
        pokeItem["_sdef"] = float(tables.xpath("tr[./th[contains(.,'Sp. Def')]]/td/text()").get())
        pokeItem["_spd"] = float(tables.xpath("tr[./th[contains(.,'Speed')]]/td/text()").get())
        pokeItem["_total"] = (  pokeItem["_hp"] + pokeItem["_atk"] + pokeItem["_def"]
                                + pokeItem["_satk"] + pokeItem["_sdef"] + pokeItem["_spd"])

        pokeItem["_growthr"] = tables.xpath("tr[./th[contains(.,'Growth')]]/td/text()").get()

        try:
            catchr = float(tables.xpath("tr[./th[contains(.,'Catch rate')]]/td/text()").get())
        except:
            catchr = -1.0

        pokeItem["_catchr"] = catchr


        gen_tables = main.xpath("//table[@class='vitals-table']")

        pokeItem["_gen"] = response.xpath("//span[@class[contains(., 'igame')]]/text()").get()

        pokeItem["_legendary"] = "Non Legendary"


        img = response.xpath("//a/img/@src").get()


        self.GET(img)

        #print(pokeItem)

        yield pokeItem


    def GET(self, url):
        """ Download a image specified by url.
        :param conn: Image url.
        :return:
        """

        file = url.split("/")[-1]
        r = requests.get(url, allow_redirects=True)
        with open("./images/" + file, 'wb') as fp:
            fp.write(r.content) #change to img folder
