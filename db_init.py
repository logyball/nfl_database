import psycopg2 as pgre
import setup_hardcoded_sql as setup_sql
import sql_helpers

DB = 'postgres'     # env var
USER = 'postgres'   # env var
PASS = 'admin'      # env var
HOST = 'localhost'  # env var
PORT = '5432'       # env var

# the first time this is run on a local computer, we'll
# need to run some setup
#   Requires a connection to the db (passed as param)
def init_table_setup(conn):
    sql_helpers.transaction(conn, setup_sql.createSchema)
    sql_helpers.transaction(conn, setup_sql.playerTableCreate)
    sql_helpers.transaction(conn, setup_sql.teamTableCreate)
    sql_helpers.transaction(conn, setup_sql.teamPlayerRelTableCreate)
    sql_helpers.transaction(conn, setup_sql.teamSeasonStatsCreate)
    sql_helpers.transaction(conn, setup_sql.gameTableCreate)
    sql_helpers.transaction(conn, setup_sql.scheduleTableCreate)
    sql_helpers.transaction(conn, setup_sql.playerGameStatsTableCreate)
    sql_helpers.transaction(conn, setup_sql.playerSeasonStatsTableCreate)
    sql_helpers.transaction(conn, setup_sql.playerCareerStatsTableCreate)


c = pgre.connect(host=HOST, database=DB, user=USER, password=PASS, port=PORT)
init_table_setup(c)
c.close()
