from sportsreference.nfl.roster import Player as rosterPl
from sportsreference.nfl.boxscore import Boxscore as box
from sportsreference.nfl.schedule import Schedule as sch
from sportsreference.nfl.teams import Teams
from sportsreference.nfl.roster import Roster
from insert_players_sql import addTeamData, SCHEMANAME
from sql_helpers import transaction

STARTYEAR = 1990    # ENV VAR?
ENDYEAR = 2019      # ENV VAR?

def getTeamInfo(team):
    return {
        'name': team._name,
        'activeYears': []
    }

def getTeamsPerYear(startYear=STARTYEAR, endYear=ENDYEAR):
    teamPerYear = {}
    for yr in range(startYear, endYear):
        teams = Teams(year=yr)
        for tms in teams:
            if tms._abbreviation in teamPerYear.keys():
                teamPerYear[tms._abbreviation]['activeYears'].append(yr)
                continue
            teamPerYear[tms._abbreviation] = getTeamInfo(tms)
            teamPerYear[tms._abbreviation]['activeYears'].append(yr)
    return teamPerYear

def playerPerGameHelper(boxsc, player, procPlayers):
    if player.player_id not in procPlayers.keys():
        # add general info to overall players!
        # add season stats
        # add career stats
        # TODO - add to DB #
        procPlayers[player.player_id] = ''
    # add specific info about this game
    # TODO - add to DB #
    return procPlayers
        
def getPlayerPerGameInfo(boxsc, procPlayers):
    for player in boxsc.away_players:
        procPlayers = playerPerGameHelper(boxsc, player, procPlayers)
    for player in boxsc.away_players:
        procPlayers = playerPerGameHelper(boxsc, player, procPlayers)
        return procPlayers

def getGameInfo(gm, procPlayers):
    boxsc = box(gm.boxscore_index)
    procPlayers = getPlayerPerGameInfo(boxsc, procPlayers)
    d = {
        'uid': gm.boxscore_index,
        'week': gm.week,
        'winner': boxsc.winning_abbr.upper(),
        'loser': boxsc.losing_abbr.upper(),
        'home': boxsc.home_abbreviation.upper(),
        'away': boxsc.away_abbreviation.upper(),
        'home_pts': boxsc.home_points,
        'away_pts': boxsc.away_points
    }, 
    # TODO - ADD TO DB! #
    return procPlayers

def getSchedulePerTeamPerYear(teamDict):
    teamYearSched = {}
    processedPlayers = {}
    processedGames = {}
    for tm in teamDict:
        teamYearSched[tm] = {}
        for yr in teamDict[tm]['activeYears']:
            sched = sch(abbreviation=tm, year=yr)
            for game in sched:
                processedPlayers = getGameInfo(game, processedPlayers)
                processedGames[game.boxscore_index] = ''
                # TODO - ADD TO DB! #
    return teamYearSched

def addTeams(conn, startYear=STARTYEAR, endYear=ENDYEAR):
    tms = getTeamsPerYear(startYear, endYear)
    for tm in tms:
        sql = addTeamData.format(
            SCHEMANAME,
            tm,
            tms[tm]['name']
        )
        transaction(conn, sql)