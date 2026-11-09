# REST API -> Fast API 구현 도와주는 라이브러리 모듈

# GET : 데이터 조회 (상품조회, 키워드검색)
# POST : 데이터 생성 | 데이터 처리 요청 (상품생성, 로그인)
# PUT/PATCH : 데이터 수정 (데이터 전체수정, 부분수정)
# DELETE : 데이터 삭제 (상품삭제, 댓글삭제, 회원정보 제거)

from fastapi import FastAPI, HTTPException, Response

app = FastAPI(
  title="Wconcept API",
  description="Wconcept 상품 및 리뷰 데이터 API",
  version="1.0.1"
)

products = [
  {
    "product_id": 1,
    "brand_name": "ZICO",
    "product_name": "Jacket",
    "price": 129000
  },
  {
    "product_id": 2,
    "brand_name": "SAM",
    "product_name": "Bag",
    "price": 89000
  },
  {
    "product_id": 3,
    "brand_name": "MARDI",
    "product_name": "T-Shirt",
    "price": 59000
  }
]

@app.get("/products")
def get_products():
  return products

@app.get("/products/{product_id}")
def get_product(product_id: int):

  for product in products :

    if product["product_id"] == product_id:

      return product
  
  raise HTTPException(
    status_code=404,
    detail="해당 상품을 찾을 수 없습니다."
  )

@app.post("/products", status_code=201)
def create_product(product: dict):

  products.append(product)

  return product

@app.put("/products/{product_id}", status_code=201)
def update_product(
  product_id: int,
  new_product: dict
):

  for index, product in enumerate(products):

    if product["product_id"] == product_id:

      new_product["product_id"] = product_id

      products[index] = new_product

      return new_product
  
  raise HTTPException(
    status_code=404,
    detail="Product not found"
  )

@app.patch("/products/{product_id}")
def patch_product(
  product_id: int,
  updated_data: dict
):

# { "price": 79000 }

  for product in products :

    if product["product_id"] == product_id :

      product.update(updated_data)

      return product
  
  raise HTTPException(
    status_code=404,
    detail="Product not found"
  )

@app.delete("/products/{product_id}", status_code=204)
def delete_product(product_id: int):

  for index, product in enumerate(products):

    if product["product_id"] == product_id :

      products.pop(index)

      return Response(status_code=204)
  
  raise HTTPException(
    status_code=404,
    detail="Product not found"
  )
