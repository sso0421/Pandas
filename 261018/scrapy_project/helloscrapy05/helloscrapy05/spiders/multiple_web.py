import scrapy
from helloscrapy05.items import Helloscrapy05Item

class MultipleWebSpider(scrapy.Spider):
    name = "multiple_web"
    allowed_domains = ["davelee-fun.github.io"]
    # 보통 단일 페이지 내 크롤링 시 아래와 같은 구문 사용!
    start_urls = ["https://davelee-fun.github.io"]

    def start_requests(self):
        urls = ["https://davelee-fun.github.io/"]
        # 리스트 컴프리핸션 문법 = 리스트 자료구조
        # 리스트 .add() : ["https://davelee-fun.github.io/", "https://davelee-fun.github.io/page2"] 
        urls.extend([f"https://davelee-fun.github.io/page{i}" for i in range(2, 9)])
        for url in urls : 
            yield scrapy.Request(url, self.parse)

    def parse(self, response):
        titles = response.css('h4.card-text::text').getall()
        for title in titles :
            item = Helloscrapy05Item()
            item["title"] = title
            yield item
