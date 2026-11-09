import os
import mysql.connector

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException

load_dotenv()

app = FastAPI(
  title="Wconcept MySQL API",
  description="FastAPI & MySQL Connection",
  version="1.0.0"
)

def get_db_connection() :

  return mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
  )

@app.get("/products")
def get_products(limit: int = 10):

  conn = get_db_connection()
  cursor = conn.cursor(dictionary=True)

  cursor.execute(
    """
    SELECT
      product_id,
      brand_name,
      product_name,
      price
    FROM api_products
    LIMIT %s;
    """, (limit, )
  )

  products = cursor.fetchall()

  cursor.close()
  conn.close()

  return products

@app.get("/products/{product_id}")
def get_product(product_id: int) :

  conn = get_db_connection()
  cursor = conn.cursor(dictionary=True)

  cursor.execute(
    """
    SELECT
      product_id,
      brand_name,
      product_name,
      price
    FROM api_products
    WHERE product_id = %s
    """, (product_id, )
  )

  product = cursor.fetchone()

  cursor.close()
  conn.close()

  return product

@app.post("/products", status_code=201)
def create_product(product: dict):

  conn = get_db_connection()
  cursor = conn.cursor(dictionary=True)

  cursor.execute(
    """
    INSERT INTO api_products
      (brand_name, product_name, price)
    VALUES
      (%s, %s, %s);
    """, (
      product["brand_name"],
      product["product_name"],
      product["price"]
      )
  )

  # 단순 값 조회 시, 불필요
  # 기존 값 저장, 편집, 삭제 등 변경사항 저장 개념
  conn.commit()

  product_id = cursor.lastrowid

  cursor.close()
  conn.close()

  return {
    "product_id": product_id,
    **product
  }

  # tuple, dictionary
  # *arg, **arg

@app.put("/products/{product_id}")
def update_product(
  product_id: int,
  product: dict
):

  conn = get_db_connection()
  cursor = conn.cursor(dictionary=True)

  cursor.execute(
    """
    UPDATE api_products
    SET
      brand_name = %s,
      product_name = %s,
      price = %s
    WHERE product_id = %s
    """, (
      product["brand_name"],
      product["product_name"],
      product["price"],
      product_id
    )
  )

  conn.commit()

  if cursor.rowcount == 0:
    cursor.close()

    raise HTTPException(
      status_code=404,
      detail="Product not found"
    )
  
  cursor.close()

  return {
    "product_id": product_id,
    **product
  }

@app.patch("/products/{product_id}")
def patch_product(product_id: int, product: dict):
  pass