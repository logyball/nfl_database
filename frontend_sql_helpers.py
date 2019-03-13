import psycopg2 as pgre
import frontend_hardcoded_sql as fhs
from os import environ

SCHEMANAME  = environ['NFLSUBDB']
DB          = environ['PGDB']
USER        = environ['PGUSERNAME']
PASS        = environ['PGPASSWORD']
HOST        = environ['PGHOST']
PORT        = environ['PGPORT']
STARTYEAR   = environ['NFLDBSTARTYEAR']
ENDYEAR     = environ['NFLDBENDYEAR']

MAXROWSTOFETCH = 5000

# ensure acidity
def addTransaction(conn, sql_string):
    try:
        cursor = conn.cursor()
        cursor.execute(sql_string)
        cursor.close()
        conn.commit()
    except pgre.DatabaseError as error:
        conn.rollback()
        print(error)
        print(sql_string)

# ensure acidity
def fetchTransaction(conn, sql_string):
    results = []
    try:
        cursor = conn.cursor()
        cursor.execute(sql_string)
        while True:
            rows = cursor.fetchmany(MAXROWSTOFETCH)
            if not rows:
                break
            results += rows
        cursor.close()
    except pgre.DatabaseError as error:
        print(error)
        print(sql_string)
        return []
    return results

def getConn():
    return pgre.connect(host=HOST, database=DB, user=USER, password=PASS, port=PORT)

def getTeams():
    c = getConn()
    sql = fhs.getTeams.format(SCHEMANAME)
    res = fetchTransaction(c, sql)
    c.close()
    return res

def getTeamsBeatUs(conn, team):
    sql = fhs.teamsWhoBeatUs.format(
        SCHEMANAME,
        team
    )
    return fetchTransaction(conn, sql)

def getBestConferenceTeam(conn, team):
    sql = fhs.teamWithBestRecordInConference.format(
        SCHEMANAME,
        team
    )
    return fetchTransaction(conn, sql)

def getBestDivisionTeam(conn, team):
    sql = fhs.teamWithBestRecordInDivision.format(
        SCHEMANAME,
        team
    )
    return fetchTransaction(conn, sql)

def get5YearBeatUs(conn, team):
    sql = fhs.fiveYearBeatUs.format(
        SCHEMANAME,
        team
    )
    return fetchTransaction(conn, sql)

def get5YearWeBeat(conn, team):
    sql = fhs.fiveYearWeBeat.format(
        SCHEMANAME,
        team
    )
    return fetchTransaction(conn, sql)

def answerCoachQuestions(qs):
    c = getConn()
    answers = {}
    team = qs['selectTeam']
    if 'beatUs' in qs.keys():
        answers['beatUs'] = getTeamsBeatUs(c, team)
    if 'bestRecInConf' in qs.keys():
        answers['bestConf'] = getBestConferenceTeam(c, team)
    if 'bestRecInDiv' in qs.keys():
        answers['bestDiv'] = getBestDivisionTeam(c, team)
    if '5YearBeatUs' in qs.keys():
        answers['fiveYrBU'] = get5YearBeatUs(c, team)
    if '5YearWeBeat' in qs.keys():
        answers['fiveYrWB'] = get5YearWeBeat(c, team)
    print(answers)
    c.close()
    return answers

def answerFanTeamQuestions(qs):
    c = getConn()
    answers = {}
    team = qs['selectTeam']
    if 'beatUs' in qs.keys():
        answers['beatUs'] = getTeamsBeatUs(c, team)
    if 'bestRecInConf' in qs.keys():
        answers['bestConf'] = getBestConferenceTeam(c, team)
    if 'bestRecInDiv' in qs.keys():
        answers['bestDiv'] = getBestDivisionTeam(c, team)
    if '5YearBeatUs' in qs.keys():
        answers['fiveYrBU'] = get5YearBeatUs(c, team)
    if '5YearWeBeat' in qs.keys():
        answers['fiveYrWB'] = get5YearWeBeat(c, team)
    print(answers)
    c.close()
    return answers
