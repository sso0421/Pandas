import os
import scrapy

from pathlib import Path # 루트폴더 기준으로 경로 주소를 찾아오려고 할 때 사용
from dotenv import load_dotenv # .env 파일을 읽어오려고 할 때 사용
from scrapy.http import JsonRequest

from wconcept.items import ProductItem, ReviewItem

ENV_PATH = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(ENV_PATH)

class ProductsSpider(scrapy.Spider):
    name = "products"

    allowed_domains = [
        "display.wconcept.co.kr",
        "gw-front.wconcept.co.kr",
        "gw-backend.wconcept.co.kr",
        "www.wconcept.co.kr"
    ]

    BEST_API_URL = "https://gw-front.wconcept.co.kr/display/api/best/v1/product"

    TARGET_COUNT = 20
    REVIEW_LIMIT = 20
    REVIEW_PAGE_SIZE = 20

    API_HEADERS = {
        "accept": "*/*",
        "accept-language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
        "agegroup": "",
        "birthdate": "",
        "cache-control": "no-cache",
        "content-type": "application/json; charset=utf-8",
        "devicetype": "PC",
        "display-api-key": os.getenv(
            "WCONCEPT_DISPLAY_API_KEY", ""
        ),
        "gendertype": "ALL",
        "membergrade": "8",
        "origin": "https://display.wconcept.co.kr",
        "pragma": "no-cache",
        "profileseqno": "",
        "referer": "https://display.wconcept.co.kr/",
        "user-agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/154.0.0.0 Safari/537.36"
        ),
    }

    AUTHORIZATION = os.getenv("WCONCEPT_REVIEW_AUTHORIZATION")

    async def start(self):

        payload = {
            "ageGroup": "all",
            "custNo": "0",
            "dateType": "daily",
            "depth1Code": "ALL",
            "depth2Code": "ALL",
            "domain": "WOMEN",
            "genderType": "all",
            "pageNo": 1,
            "pageSize": self.TARGET_COUNT
        }

        self.logger.info(f"BEST 상품 {self.TARGET_COUNT}개 요청 준비")

        yield JsonRequest(
            url=self.BEST_API_URL,
            method="POST",
            headers=self.API_HEADERS,
            data=payload,
            callback=self.parse_best
        )
    
    def parse_best(self, response):
        print("HTTP 상태코드:", response.status)
        print("API 주소:", response.url)

        try :
            data = response.json()
        
        except ValueError as e :
            self.logger.error(f"JSON 변환 실패: {e}")
            return

        print("data 자료형:", type(data))

        print("최상위 Key:", data.keys())

        print("API 결과:", data.get("result"))

        result_data = data.get("data", {})

        print("내부 data 자료형:", type(result_data))
        print("내부 data key:", result_data.keys())

        content = result_data.get("content", [])

        print("content 자료형:", type(content))
        print("수집된 상품 수:", len(content))

        # self.logger.info(f"요청 상품 수={self.TARGET_COUNT} | 실제 반환 상품 수={len(content)}")

        if content :
            product_data = content[0]

            print("첫 번째 상품 자료형:", type(product_data))

            print("첫 번째 상품 Key:", product_data.keys())

            print("상품 ID:", product_data.get("itemCd"))

            print("브랜드명:", product_data.get("brandNameKr"))

            print("상품명:", product_data.get("itemName"))

            print("판매가격:", product_data.get("salePrice"))
        
        for rank, product_data in enumerate(content[:self.TARGET_COUNT], start=1) :
            
            # print("=" * 40)

            # print("순위:", rank)
            # print("상품 ID:", product_data.get("itemCd"))
            # print("브랜드:", product_data.get("brandNameKr"))
            # print("상품명:", product_data.get("itemName"))
            # print("판매가격:", product_data.get("salePrice"))

            product = ProductItem()

            product["item_type"] = "product"

            product["rank"] = rank

            product["product_id"] = product_data.get("itemCd")

            product["brand_id"] = product_data.get("brandCd")

            product["brand_name_kr"] = product_data.get("brandNameKr")

            product["brand_name_en"] = product_data.get("brandNameEn")

            product["product_name"] = product_data.get("itemName")

            product["category_1"] = product_data.get("categoryDepthName1")

            product["category_2"] = product_data.get("categoryDepthName2")

            product["category_3"] = product_data.get("categoryDepthName3")

            product["customer_price"] = product_data.get("customerPrice")

            product["sale_price"] = product_data.get("salePrice")

            product["final_price"] = product_data.get("finalPrice")

            product["discount_rate"] = product_data.get("finalDiscountRate")

            product["review_count"] = product_data.get("reviewCnt")

            product["review_score"] = product_data.get("reviewScore")

            product["heart_count"] = product_data.get("heartCnt")

            product["product_url"] = product_data.get("landingUrl")

            product["image_url"] = product_data.get("productImageUrl")

            yield product

            review_count = product_data.get("reviewCnt") or 0

            self.logger.info(f"[상품처리] rank={rank} | product_id={product["product_id"]} | review_count={review_count}")
            
            if review_count <= 0 :

                self.logger.info(f"[리뷰 없음] product_id={product["product_id"]}")

                continue

            item_cd = product["product_id"]

            detail_url = f"https://www.wconcept.co.kr/Product/{"item_Cd"}"

            yield scrapy.Request(
                url=detail_url,
                callback=self.parse_product,
                cb_kwargs={
                    "rank": rank,
                    "product_id": item_cd,
                    "review_count": review_count,
                },

                headers={
                    "User-Agent": self.API_HEADERS["user-agent"],
                    "Referer": "https://display.wconcept.co.kr/women"
                }
            )

    def parse_product(self, response, rank, product_id, review_count) :
        category_cd = response.css("#ca::attr(value)").get()
        item_cd = response.css("#qa_itemcd::attr(value)").get()
        medium_cd = response.css("#mcd::attr(value)").get()

        self.logger.info(
            f"[상세정보] rank={rank} | product_id={product_id} | itemCd={item_cd} | medium_Cd={medium_cd} | categoryCd={category_cd} | review_count={review_count}"
        )
        if not all([item_cd, medium_cd, category_cd]) : 

            self.logger.warning(
                f"[리뷰 요청 생략] product_id={product_id} | 필수 코드 누락"
            )


            return
        
        review_request = self.make_review_request(
            item_cd=item_cd,
            medium_cd=medium_cd,
            category_cd=category_cd,
            product_id=product_id,
            rank=rank,
            page_no=1
        )

        if review_request is not None :
            yield review_request

    def make_review_request(
        self, item_cd, medium_cd, category_cd, product_id, rank, page_no
    ) :
        review_url = "https://gw-backend.wconcept.co.kr/api/v2/review/tab/list/with-summary"
        
        payload = {
            "categoryCd": category_cd,
            "hiddenReviewInclude": True,
            "itemCd": item_cd,
            "itemTypeCd": "15",
            "mediumCd": medium_cd,
            "pageNo": 1,
            "pageSize": 6,
            "searchType": 1
        }

        headers = {
            "Accept": "application/json",
            "content-type": "application/json",
            "Origin": "https://www.wconcept.co.kr",
            "Referer": "https://www.wconcept.co.kr/",
            "User-agent": self.API_HEADERS["user-agent"],
            "x-authorization": self.AUTHORIZATION
        }

        self.logger.info(
            f"[리뷰 API 요청] rank={rank} | product_id{product_id} | page={page_no}"
        )

        return JsonRequest(
            url=review_url,
            method="POST", 
            headers=headers,
            data=payload,
            callback=self.parse_reviews,
            cb_kwargs={
                "rank": rank,
                "product_id": product_id,
                "page_no":  page_no
            }
        )
    
    def parse_reviews(self, response, rank, product_id, page_no) :
        self.logger.info(f"[리뷰 API 응답] rank={rank} HTTP={response.status}")

        try :
            result = response.json()
        except ValueError as e :
            self.logger.error(f"[리뷰 JSONO 변환 실패] {e}")
            return

        data = result.get("data")

        reviews = data.get("reviews")

        review_total = data.get("reviewTotal")

        total_pages = data.get("reviewTotalPages")

        self.logger.info(f"[리뷰 수집 성공] rank={rank} | product_id{product_id} | page={page_no} | total={review_total} | total_pages={total_pages} | recevied={len(reviews)}")

        for review in reviews[:self.REVIEW_LIMIT] : 

            item = ReviewItem()
            item["product_id"] = product_id
            item["review_id"] = review.get("reviewMasterSeqNo")
            item["rating"] = review.get("reviewRating")
            item["review_text"] = review.get("contents")
            item["created_at"] = review.get("reviewRegDate")
            item["review_articles"] = review.get("reviewArticles")
            item["review_options"] = review.get("reviewOptions")
            item["review_images"] = [file.get("filePath") for file in review.get("reviewFiles")]

            yield item
            
            self.logger.info(f"[리뷰 저장] product_id={product_id} | review_id={item["review_id"]}")