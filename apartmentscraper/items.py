# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class ApartmentscraperItem(Item):
    # define the fields for your item here like:
    url = Field()
    name = Field()
    address = Field()
    location = Field()
    surface_area = Field()
    construction_year = Field()
    price = Field()
    monthly_costs = Field()


    pass
