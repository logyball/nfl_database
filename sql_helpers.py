import psycopg2 as pgre

# ensure acidity
def transaction(conn, sqlString):
    # add try/catch
    cursor = conn.cursor()
    cursor.execute(sqlString)
    cursor.close()
    conn.commit()
