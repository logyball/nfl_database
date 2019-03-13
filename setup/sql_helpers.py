import psycopg2 as pgre
import insert_players_sql as pl_sql
import insert_nonplayer_sql as npl_sql

# ensure acidity
def transaction(conn, sql_string):
    try:
        cursor = conn.cursor()
        cursor.execute(sql_string)
        cursor.close()
        conn.commit()
    except pgre.DatabaseError as error:
        conn.rollback()
        print(error)
        print(sql_string)

def addGameStats(conn, boxsc, gm):
    try:
        sql = npl_sql.addGameStat.format(
            npl_sql.SCHEMANAME,
            gm.boxscore_index,
            gm.week if gm.week else 0,
            boxsc.winning_abbr.upper() if boxsc.winning_abbr else 'IDK',
            boxsc.losing_abbr.upper() if boxsc.losing_abbr else 'IDK',
            boxsc.home_points if boxsc.home_points else 0,
            boxsc.away_points if boxsc.away_points else 0,
            boxsc.home_abbreviation.upper() if boxsc.home_abbreviation else 'IDK',
            boxsc.away_abbreviation.upper() if boxsc.away_abbreviation else 'IDK'
        )
        transaction(conn, sql)
    except TypeError as e:
        print(e)

def addTeamSeasonStats(conn, team, year):
    try:
        sql = npl_sql.addTeamSeasonStat.format(
            npl_sql.SCHEMANAME,
            team.abbreviation,
            int(year),
            team.wins if team.wins else 0,
            team.losses if team.losses else 0,
            team.points_for if team.points_for else 0,
            team.points_against if team.points_against else 0,
            team.yards if team.yards else 0
        )
        transaction(conn, sql)
    except TypeError as e:
        print(e)

def addQbStats(conn, player, index):
    # _attempted_passes, _completed_passes, _passing_yards, _passing_touchdows, _interceptions_thrown
    # _fumbles, _rush_yards, _rush_touchdowns
    try:
        season = player._season[index]
        if season == 'Career':
            sql = pl_sql.addQbCareerStat.format(
                pl_sql.SCHEMANAME,
                player._player_id,
                player._attempted_passes[index] if player._attempted_passes[index] else  0,
                player._completed_passes[index] if player._completed_passes[index] else  0,
                player._passing_yards[index] if player._passing_yards[index] else  0,
                player._interceptions_thrown[index] if player._interceptions_thrown[index] else  0,
                player._passing_touchdowns[index] if player._passing_touchdowns[index] else  0,
                player._fumbles[index] if player._fumbles[index] else  0,
                player._rush_attempts[index] if player._rush_attempts[index] else  0,
                player._rush_yards[index] if player._rush_yards[index] else  0,
                player._rush_touchdowns[index] if player._rush_touchdowns[index] else  0
            )
        else:
            sql = pl_sql.addQbSeasonStat.format(
                pl_sql.SCHEMANAME,
                player._player_id,
                season if season else 0,
                player._attempted_passes[index] if player._attempted_passes[index] else  0,
                player._completed_passes[index] if player._completed_passes[index] else  0,
                player._passing_yards[index] if player._passing_yards[index] else  0,
                player._interceptions_thrown[index] if player._interceptions_thrown[index] else  0,
                player._passing_touchdowns[index] if player._passing_touchdowns[index] else  0,
                player._fumbles[index] if player._fumbles[index] else  0,
                player._rush_attempts[index] if player._rush_attempts[index] else  0,
                player._rush_yards[index] if player._rush_yards[index] else  0,
                player._rush_touchdowns[index] if player._rush_touchdowns[index] else  0
            )
        transaction(conn, sql)
    except TypeError as e:
        print(e)

def addRbStats(conn, player, index):
    # _rush_attempts, _fumbles, _rush_yards, _rush_touchdowns, _receptions, _receiving_yards, _receiving_touchdowns
    try:
        season = player._season[index]
        if season == 'Career':
            sql = pl_sql.addRbCareerStat.format(
                pl_sql.SCHEMANAME,
                player._player_id,
                player._fumbles[index] if player._fumbles[index] else  0,
                player._rush_attempts[index] if player._rush_attempts[index] else  0,
                player._rush_yards[index] if player._rush_yards[index] else  0,
                player._rush_touchdowns[index] if player._rush_touchdowns[index] else  0,
                player._receptions[index] if player._receptions[index] else  0,
                player._receiving_yards[index] if player._receiving_yards[index] else  0,
                player._receiving_touchdowns[index] if player._receiving_touchdowns[index] else  0
            )
        else:
            sql = pl_sql.addRbSeasonStat.format(
                pl_sql.SCHEMANAME,
                player._player_id,
                season if season else 0,
                player._fumbles[index] if player._fumbles[index] else  0,
                player._rush_attempts[index] if player._rush_attempts[index] else  0,
                player._rush_yards[index] if player._rush_yards[index] else  0,
                player._rush_touchdowns[index] if player._rush_touchdowns[index] else  0,
                player._receptions[index] if player._receptions[index] else  0,
                player._receiving_yards[index] if player._receiving_yards[index] else  0,
                player._receiving_touchdowns[index] if player._receiving_touchdowns[index] else  0
            )
        transaction(conn, sql)
    except TypeError as e:
        print(e)

def addWrTeStats(conn, player, index):
    # _fumbles, _receptions, _receiving_yards, _receiving_touchdowns
    try:
        season = player._season[index]
        if season == 'Career':
            sql = pl_sql.addWrCareerStat.format(
                pl_sql.SCHEMANAME,
                player._player_id,
                player._fumbles[index] if player._fumbles[index] else  0,
                player._receptions[index] if player._receptions[index] else  0,
                player._receiving_yards[index] if player._receiving_yards[index] else  0,
                player._receiving_touchdowns[index] if player._receiving_touchdowns[index] else  0
            )
        else:
            sql = pl_sql.addWrSeasonStat.format(
                pl_sql.SCHEMANAME,
                player._player_id,
                season if season else 0,
                player._fumbles[index] if player._fumbles[index] else 0,
                player._receptions[index] if player._receptions[index] else 0,
                player._receiving_yards[index] if player._receiving_yards[index] else 0,
                player._receiving_touchdowns[index] if player._receiving_touchdowns[index] else 0
            )
        transaction(conn, sql)
    except TypeError as e:
        print(e)

def addKickStats(conn, player, index):
    # _field_goals_attempted, _field_goals_made
    try:
        season = player._season[index]
        if season == 'Career':
            sql = pl_sql.addKCareerStat.format(
                pl_sql.SCHEMANAME,
                player._player_id,
                player._field_goals_attempted[index] if player._field_goals_attempted[index] else 0,
                player._field_goals_made[index] if player._field_goals_made[index] else 0
            )
        else:
            sql = pl_sql.addKSeasonStat.format(
                pl_sql.SCHEMANAME,
                player._player_id,
                season if season else 0,
                player._field_goals_attempted[index] if player._field_goals_attempted[index] else 0,
                player._field_goals_made[index] if player._field_goals_made[index] else 0
            )
        transaction(conn, sql)
    except TypeError as e:
        print(e)
    except IndexError as ie:
        print(ie)

def addGameToSched(conn, boxscore, week, year, gamekey):
    team1 = boxscore.away_abbreviation.upper() if boxscore.away_abbreviation else 'IDK'
    team2 = boxscore.home_abbreviation.upper() if boxscore.home_abbreviation else 'IDK'
    try:
        sql = npl_sql.addScheduleGame.format(
            npl_sql.SCHEMANAME,
            team1,
            year,
            week,
            gamekey
        )
        transaction(conn, sql)
        sql = npl_sql.addScheduleGame.format(
            npl_sql.SCHEMANAME,
            team2,
            year,
            week,
            gamekey
        )
        transaction(conn, sql)
    except TypeError as e:
        print(e)

def addTeamYears(conn, player, index):
    try:
        sql = pl_sql.addPlayerTeamYear.format(
            pl_sql.SCHEMANAME,
            player._player_id,
            player._team_abbreviation[index] if player._team_abbreviation[index] else 'IDK',
            player._season[index] if player._season[index] else 0
        )
        transaction(conn, sql)
    except TypeError as e:
        print(e)

def addMetadata(conn, player, pos):
    try:
        name = player._name.replace("'", "") if player._name else "Unknown"
        sql = pl_sql.addPlayerMetadata.format(
            pl_sql.SCHEMANAME, 
            player._player_id, 
            name, 
            pos if pos else "NA", 
            player._birth_date if player._birth_date else '01-01-1900', 
            player._height if player._height else '6-0'
        )
        transaction(conn, sql)
    except TypeError as e:
        print(e)

def getPlayerPos(player):
    # awful, but assume player is same position
    # their whole career...
    for p in player._position[::-1]:
        if p != '':
            return p.upper()
    return ''

def addPlayerDataPerPosition(conn, player):
    try:
        pos = getPlayerPos(player)
    except TypeError as e:
        print(e)
        return
    addMetadata(conn, player, pos)
    if player._season:
        for index in range(0, len(player._season)):
            if player._season[index] != 'Career':
                addTeamYears(conn, player, index)
            if pos == 'QB':
                addQbStats(conn, player, index)
            elif pos == 'RB':
                addRbStats(conn, player, index)
            elif pos == 'WR' or pos == 'TE':
                addWrTeStats(conn, player, index)
            elif pos == 'K':
                addKickStats(conn, player, index)
