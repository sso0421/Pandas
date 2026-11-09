from fastapi import FastAPI, HTTPException

app = FastAPI()
# GET, POST, PUT, DELETE

#EndPoint
@app.get("/")
def home():
    return {
        "message":"Hello Wconcept!"
    }

@app.get("/hello")
def hello():
    return{
        "message": "FastAPII Start!"
    }

@app.get("/products")
def get_products():
    return {
        "products": [
            {
                "product_id": "P001",
                "product_name": "Wconcept Jacket",
                "price": 129000
            },
            {
                "product_id": "P002",
                "product_name": "Wconcept Bag",
                "price": 89000
            }
        ]
    }


# Type Hint : 가변 파라미터 값을 수신, 정수와 같은 형태만 넣겠다
@app.get("/products/{product_id}")
def get_product(product_id: int):
    return {
        "product_id": product_id
    }

# Query Parameter 구문 연습
# 유튜브, 인스타그램 API를 통해서 값을 조회 // ?limit=10

# @app.get("/products")
# def get_product(limit: int = 10):
#     return {
#         "limit": limit
#     }

# 쿼리 파라미터 값 : 복수 설정
# ?utm_campaign=abc&utm_medium=meta
# ?limit=5&brand=musinsa
@app.get("/products")
def get_product(limit: int = 10, brand: str | None=None):
    return {
        "limit": limit,
        "brand": brand
    }

# /값은 path parameter라고 부름
# /값1?키=값2 -> 값2를 query parameter(string)이라고 부름

# 수동적으로 데이터를 수집!
# 수집된 데이터를 원하는 방식으로 제공!
# User -> Client -> Server -> DB

# 어떤 path parameter 값을 설정했을 때, db에서 값을 찾아서 client에게 값을 제공
# -> 만약 존재하지 않는 상품을 찾아달라고 한다면?
# => 해당 상품일 존재하지 않아요!를 나타내고 싶을 때, null로 표기하면 상품이 존재하지 않는지, 문법의 오류인지, 서버가 문제가 있는건지..
# 상태코드