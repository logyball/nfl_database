import psycopg2 as pgre
import setup_hardcoded_sql as setup_sql
import sql_helpers
import data_collection as dc

DB          = 'postgres'    # env var
USER        = 'postgres'    # env var
PASS        = 'admin'       # env var
HOST        = 'localhost'   # env var
PORT        = '5432'        # env var
STARTYEAR   = 2010          # ENV VAR?
ENDYEAR     = 2019          # ENV VAR?


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
    #sql_helpers.transaction(conn, setup_sql.playerGameStatsTableCreate)
    sql_helpers.transaction(conn, setup_sql.playerSeasonStatsTableCreate)
    sql_helpers.transaction(conn, setup_sql.playerCareerStatsTableCreate)
    sql_helpers.transaction(conn, setup_sql.addExtraTeamData)

def addTeamsToDb(conn):
    teams = dc.addTeams(conn, STARTYEAR, ENDYEAR)
    sql_helpers.transaction(conn, setup_sql.addExtraTeams)
    return teams

def addAllOtherDataToDb(conn, teams):
    dc.addAllData(conn, teams, STARTYEAR, ENDYEAR)

c = pgre.connect(host=HOST, database=DB, user=USER, password=PASS, port=PORT)
init_table_setup(c)
tms = addTeamsToDb(c)
addAllOtherDataToDb(c, tms)
c.close()
