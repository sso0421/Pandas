import scrapy

class Helloscrapy03Item(scrapy.Item):
    title = scrapy.Field()
    description = scrapy.Field()