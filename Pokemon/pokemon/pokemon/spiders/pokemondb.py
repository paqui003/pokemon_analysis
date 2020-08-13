import scrapy

from ..items import Pokemon


 #table = response.xpath("//table[@id='pokedex']/tbody/tr")
#l = [entry.xpath("td") for entry in table]
 #_id, _name, _type, _total, _hp, _atk, _def, _satk, _sd, _spd = l[0]
class ReviewSpider(scrapy.Spider):
    name = "pokemon"
    start_urls = [
        "https://pokemondb.net/pokedex/all",
    ]

    _dex = {}

    #albums_l = []
    #artists_l = []

    '''def remove_html_tags(self, text):
        """Remove html tags from a string"""
        import re
        clean = re.compile('<.*?>')
        return re.sub(clean, '', text)'''

    def parse(self, response):
        dexTable = response.xpath("//table[@id='pokedex']/tbody")
        pokeLinks = dexTable.xpath("tr/td/a[@class='ent-name']")

        for a in pokeLinks.xpath("@href").getall():
            yield response.follow(a, callback=self.parse_review)

    def parse_review(self, response):
        import re
        pokeItem = Pokemon()

        main = response.xpath("//main")

        pokeItem["_name"] =  main.xpath("./h1/text()").get()
        pokeItem["_dex"] = dex = main.xpath(
            "//table[@class='vitals-table']/tbody/tr[contains(.,'National')]/td/strong/text()").get()

        height_raw = main.xpath("//table[@class='vitals-table']/tbody/tr[contains(.,'Height')]/td/text()").get()
        weight_raw = main.xpath("//table[@class='vitals-table']/tbody/tr[contains(.,'Weight')]/td/text()").get()

        try:
            pokeItem["_height"] = float(re.findall("[0-9]*\.[0-9]*", height_raw)[0])
            pokeItem["_weight"] = float(re.findall("[0-9]*\.[0-9]*", weight_raw)[0])
        except:
            pokeItem["_height"] = 0.0
            pokeItem["_weight"] = 0.0


        pokeItem["_hp"] = float(main.xpath("//table[@class='vitals-table']/tbody/tr[./th[contains(.,'HP')]]/td/text()").get())
        pokeItem["_atk"] = float(main.xpath("//table[@class='vitals-table']/tbody/tr[./th[contains(.,'Attack')]]/td/text()").get())
        pokeItem["_def"] = float(main.xpath("//table[@class='vitals-table']/tbody/tr[./th[contains(.,'Defense')]]/td/text()").get())
        pokeItem["_satk"] = float(main.xpath("//table[@class='vitals-table']/tbody/tr[./th[contains(.,'Sp. Atk')]]/td/text()").get())
        pokeItem["_sdef"] = float(main.xpath("//table[@class='vitals-table']/tbody/tr[./th[contains(.,'Sp. Def')]]/td/text()").get())
        pokeItem["_spd"] = float(main.xpath("//table[@class='vitals-table']/tbody/tr[./th[contains(.,'Speed')]]/td/text()").get())
        pokeItem["_total"] = (  pokeItem["_hp"] + pokeItem["_atk"] + pokeItem["_def"]
                                + pokeItem["_satk"] + pokeItem["_sdef"] + pokeItem["_spd"])
        print(pokeItem)
        pass
