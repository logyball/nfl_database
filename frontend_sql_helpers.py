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

def fetchTransactionSafely(conn, sql_string, user_input):
    results = []
    try:
        cursor = conn.cursor()
        cursor.execute(sql_string, user_input)
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

def getDivs():
    c = getConn()
    sql = fhs.getDivs.format(SCHEMANAME)
    res = fetchTransaction(c, sql)
    c.close()
    return res

def getConf():
    c = getConn()
    sql = fhs.getConf.format(SCHEMANAME)
    res = fetchTransaction(c, sql)
    c.close()
    return res

def getYears():
    c = getConn()
    sql = fhs.getYears.format(SCHEMANAME)
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

def getTeamsPlayedOn(conn, pl):
    user_input = (pl,)
    return fetchTransactionSafely(conn, fhs.whichTeamsForPlayer, user_input)

def getPlayerCareerStats(conn, pl):
    user_input = (pl,)
    return fetchTransactionSafely(conn, fhs.playerCareerStats, user_input)

def getPlayerSeasonStats(conn, pl):
    user_input = (pl,)
    return fetchTransactionSafely(conn, fhs.playerLastYearStats, user_input)

def getBestTeamRecord(conn, pl):
    user_input = (pl,pl)
    return fetchTransactionSafely(conn, fhs.playerBestTeamByRec, user_input)

def getCoachImproving(conn, team, year):
    row = []
    try:
        cursor = conn.cursor()
        cursor.callproc('nflDb.GetCoachImprovment', (team, year))
        row = cursor.fetchall()
        cursor.close()
        conn.commit()
    except pgre.DatabaseError as error:
        print(error)
    return row

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
    if 'isCoachImproving' in qs.keys():
        answers['isCoachImproving'] = getCoachImproving(c, team, qs['coachStartYear'])
        answers['coachStartYear'] = qs['coachStartYear']
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

def makeStatsIntelligable(statDict):
    d = {}
    try:
        if statDict[0][1]:
            d['passAt'] = statDict[0][1]
        if statDict[0][2]:
            d['passCom'] = statDict[0][2]
        if statDict[0][3]:
            d['passYds'] = statDict[0][3]
        if statDict[0][4]:
            d['int'] = statDict[0][4]
        if statDict[0][5]:
            d['passtd'] = statDict[0][5]
        if statDict[0][6]:
            d['fumbles'] = statDict[0][6]
        if statDict[0][7]:
            d['rushAt'] = statDict[0][7]
        if statDict[0][8]:
            d['rushyd'] = statDict[0][8]
        if statDict[0][9]:
            d['rushtd'] = statDict[0][9]
        if statDict[0][10]:
            d['rec'] = statDict[0][10]
        if statDict[0][11]:
            d['rectds'] = statDict[0][11]
        if statDict[0][12]:
            d['recyds'] = statDict[0][12]
        if statDict[0][13]:
            d['fga'] = statDict[0][13]
        if statDict[0][14]:
            d['fgm'] = statDict[0][14]
    except IndexError as e:
        print(e)
    return d

def makeCustomTeam(conn, name, abbr, div, conf):
    try:
        cursor = conn.cursor()
        cursor.callproc('nflDb.addNewTeam', (abbr, name, div, conf))
        cursor.close()
        conn.commit()
    except pgre.DatabaseError as error:
        print(error)

def makeCustomPlayer(conn, pid, pname, pos):
    try:
        cursor = conn.cursor()
        cursor.callproc('nflDb.addNewPlayer', (pid, pname, pos, '1-1-90', '5-10'))
        cursor.close()
        conn.commit()
    except pgre.DatabaseError as error:
        print(error)


def answerFanPlayerQuestions(qs):
    c = getConn()
    answers = {}
    pl = qs['favPlayer']
    if 'teamsPlayedOn' in qs.keys():
        answers['teamsPlayedOn'] = getTeamsPlayedOn(c, pl)
    if 'careerStats' in qs.keys():
        answers['careerStats'] = makeStatsIntelligable(getPlayerCareerStats(c, pl))
    if 'seasonStats' in qs.keys():
        answers['seasonStats'] = makeStatsIntelligable(getPlayerSeasonStats(c, pl))
    if 'bestTeamRecord' in qs.keys():
        answers['bestTeamRecord'] = getBestTeamRecord(c, pl)
    if 'custTeam' in qs.keys():
        makeCustomTeam(c, qs['custTeam'], qs['custTeamAbbr'], qs['custTeamDivs'], qs['custTeamConfs'])
    if 'custPlayer' in qs.keys():
        makeCustomPlayer(c, qs['custPlayer'], qs['custPlayerName'], qs['custPlayerPos'])
    answers['favPlayer'] = pl
    print(answers)
    c.close()
    return answers