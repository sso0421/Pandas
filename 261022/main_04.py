# python + mysql을 연결시켜줄 라이브러리 모듈
# mysql-connector-python
# pip install mysql-connector-python
# pip list
import os
import mysql.connector

from dotenv import load_dotenv

load_dotenv()

# python + mtsql = 다리 연결
# conn = mysql.connector.connect(
#   host="localhost",
#   user="root",
#   password="ssojini9804",
#   database="api_db"
# )

# print(conn.is_connected())

conn = mysql.connector.connect(
  host=os.getenv("DB_HOST"),
  user=os.getenv("DB_USER"),
  password=os.getenv("DB_PASSWORD"),
  database=os.getenv("DB_NAME")
)

# print(conn.is_connected())

# 이제부터는 연결된 다리를 기준으로 실제 업무 실행 객체
cursor = conn.cursor(dictionary=True)

cursor.execute(
  """
  SELECT
    product_id,
    brand_name,
    product_name,
    price
  FROM api_products;
  """
)

rows = cursor.fetchall()

print(rows)