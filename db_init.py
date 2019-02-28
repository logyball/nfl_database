import psycopg2 as pgre

DB = 'postgres'
USER = 'postgres'
PASS = 'admin'
HOST = 'localhost'

c = pgre.connect(host=HOST, database=DB, user=USER, password=PASS)