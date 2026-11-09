from fastapi import FastAPI, HTTPException

# API 부가설명을 기입 = API Metadata
app = FastAPI(
  title="Wconcept API",
  description="Wconcept 상품 및 리뷰 데이터 API",
  version="1.0.1"
)
# Major : 호환성이 불가능한 정도의 버전 / Minor : 호환이 가능한 정도의 버전 / Patch : 호환 가능 버그 수정

# 현재 우리 서버 설치되어있는 엔드포인드 및 HTTP Method 종류
# Swagger UI : 목록

# http://127.0.0.1:8000/docs
# > 임시 테스트 목적

# http://127.0.0.1:8000/redoc
# > 현재 설정된 메서드들의 자세한 메뉴얼 정보

# 임시 DB
products = [
  {
    "product_id": 1,
    "brand_name": "ZICO",
    "product_name": "Wconcept Jacket",
    "price": 129000
  },
  {
    "product_id": 2,
    "brand_name": "SAM",
    "product_name": "Wconcept Bag",
    "price": 89000
  }
]

@app.get("/")
def home():
  return {
    "message": "Wconcept API"
  }

@app.get("/products")
def get_products(limit: int = 10, brand: str | None = None):

  result = products

  if brand :

    result = [product for product in result if product["brand_name"] == brand]

  return {
    "count": len(result[:limit]),
    "products": result[:limit]
  }
  
@app.get("/products/{product_id}")
def get_product(product_id: int):

  for product in products :

    if product["product_id"] == product_id:

      return product
  
  raise HTTPException(
    status_code=404,
    detail="해당 상품을 찾을 수 없습니다."
  )
# 200 : 조회성공
# 201 : 신규상품등록
# 204 : 상품삭제 완료
# 400 : 잘못된요청
# 401 : 인증실패 (payload 누락)
# 403 : 접근권한
# 404 : 존재하지 않는 상품 요청
# 422 : 요청한 데이터 타입 오류
# 500 : 서버 내부 오류