from sportsreference.nfl.roster import Player as rosterPl
from sportsreference.nfl.boxscore import Boxscore as box
from sportsreference.nfl.boxscore import BoxscorePlayer as boxPl
from sportsreference.nfl.schedule import Schedule as sch
from sportsreference.nfl.teams import Teams, Team
from sportsreference.nfl.roster import Roster
from insert_players_sql import addTeamData, SCHEMANAME
import sql_helpers as sqhelp

PROCPLRS = {}
PROCGAMES = {}

def playerPerGameHelper(conn, player):
    if player._player_id not in PROCPLRS.keys():
        print("new player %s" % player._player_id)
        sqhelp.addPlayerDataPerPosition(conn, rosterPl(player._player_id))
        PROCPLRS[player._player_id] = ''
        
def getPlayerPerGameInfo(conn, boxsc):
    for player in boxsc._away_players:
        playerPerGameHelper(conn, player)
    for player in boxsc._home_players:
        playerPerGameHelper(conn, player)
        
def getGameInfo(conn, gm, year):
    print("new Game %s" % gm)
    boxsc = box(gm.boxscore_index)
    getPlayerPerGameInfo(conn, boxsc)
    sqhelp.addGameStats(conn, boxsc, gm)
    sqhelp.addGameToSched(conn, boxsc, gm.week, year, gm.boxscore_index)

def addAllData(conn, teamDict, startYear, endYear):
    for tm in teamDict:
        print("New team: %s" % tm)
        for yr in range(startYear, endYear):
            print("new year %d" % yr)
            try:
                sched = sch(abbreviation=tm, year=yr)
                for game in sched:
                    if game.boxscore_index in PROCGAMES.keys():
                        continue
                    getGameInfo(conn, game, yr)
                    PROCGAMES[game.boxscore_index] = ''
            except Exception as e:
                print(e)
                continue

def addTeams(conn, startYear, endYear):
    teamz = {}
    for year in range(startYear, endYear):
        seasons = Teams(year=year)
        for team in seasons:
            if team.abbreviation not in teamz.keys():
                sql = addTeamData.format(
                    SCHEMANAME,
                    team.abbreviation,
                    team.name
                )
                sqhelp.transaction(conn, sql)
                teamz[team.abbreviation] = ""
            sqhelp.addTeamSeasonStats(conn, team, year)
    return teamz