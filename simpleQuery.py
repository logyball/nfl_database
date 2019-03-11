import psycopg2 as pgre

DB = 'postgres'
USER = 'postgres'
PASS = 'admin'
HOST = 'localhost'
PORT = '5432'

posStr = """
Enter which position you'd like to see player stats on:
    1. QB
    2. WR
    3. RB
    4. TE
    5. K
"""

nameStr = """
Enter a player's name: 
"""

statStr = """
Which stat would you like?
    1. Height
    2. Weight
"""

pos = input(posStr)
name = input(nameStr)
stat = input(statStr)

c = pgre.connect(host=HOST, database=DB, user=USER, password=PASS, port=PORT)

cur = c.cursor()
cur.execute("SELECT Weight FROM nfldb.player WHERE name='Drew Brees'")
a = cur.fetchall()
for n in a:
    print(n)
cur.close()
c.close()