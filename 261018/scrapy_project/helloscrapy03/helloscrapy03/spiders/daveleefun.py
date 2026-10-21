import scrapy
from helloscrapy03.items import Helloscrapy03Item


class DaveleefunSpider(scrapy.Spider):
    name = "daveleefun"
    allowed_domains = ["davelee-fun.github.io"]
    start_urls = ["https://davelee-fun.github.io"]

    def parse(self, response):
        item = Helloscrapy03Item()
        item["title"] = response.css('h1.sitetitle::text').get()
        item["description"] = response.xpath('//p[@class="lead"]/text()').get()

        yield item
