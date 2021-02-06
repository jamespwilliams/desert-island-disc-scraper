from scrapy.item import Item, Field
from scrapy.crawler import CrawlerProcess

class Appearance(Item):
    id = Field()
    broadcast_time = Field()
    guest_name = Field()

class Disc(Item):
    appearance_id = Field()
    artist = Field()
    title = Field()
    index = Field()
