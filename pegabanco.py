import psycopg2
from configparser import ConfigParser


#conn = psycopg2.connect("dbname=suppliers user=postgres password=postgres")
conn = psycopg2.connect(
    host="localhost",
    port= 5434,
    database="banco001",
    user="postgres",
    password="1",
    options="-c search_path=public")

cur = conn.cursor()
cur.execute("""SELECT 
  item.codigo_barra
FROM 
  item;""")

tables = cur.fetchall()
print(tables)

print (conn.closed) # 0
