import psycopg2 as pgre
import hardcoded_sql as static_sql
import sql_helpers
from sportsreference.nfl.roster import Player as pl

DB = 'postgres'     # env var
USER = 'postgres'   # env var
PASS = 'admin'      # env var
HOST = 'localhost'  # env var
PORT = '5432'       # env var

# the first time this is run on a local computer, we'll
# need to run some setup
#   Requires a connection to the db (passed as param)
def init_setup(conn):
    sql_helpers.transaction(conn, static_sql.createSchema)
    sql_helpers.transaction(conn, static_sql.playerTableCreate)
    sql_helpers.transaction(conn, static_sql.teamTableCreate)
    sql_helpers.transaction(conn, static_sql.teamPlayerRelTableCreate)
    sql_helpers.transaction(conn, static_sql.teamSeasonStatsCreate)
    sql_helpers.transaction(conn, static_sql.gameTableCreate)
    sql_helpers.transaction(conn, static_sql.scheduleTableCreate)
    sql_helpers.transaction(conn, static_sql.playerGameStatsTableCreate)
    sql_helpers.transaction(conn, static_sql.playerSeasonStatsTableCreate)
    sql_helpers.transaction(conn, static_sql.playerCareerStatsTableCreate)


c = pgre.connect(host=HOST, database=DB, user=USER, password=PASS, port=PORT)
init_setup(c)
c.close()
