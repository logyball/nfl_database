import psycopg2 as pgre
import insert_players_sql as pl_sql

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

def addQbStats(conn, player, index):
    # _attempted_passes, _completed_passes, _passing_yards, _passing_touchdows, _interceptions_thrown
    # _fumbles, _rush_yards, _rush_touchdowns
    season = player._season[index]
    if season == 'Career':
        sql = pl_sql.addQbCareerStat.format(
            pl_sql.SCHEMANAME,
            player._player_id,
            player._attempted_passes[index],
            player._completed_passes[index],
            player._passing_yards[index],
            player._interceptions_thrown[index],
            player._passing_touchdowns[index],
            player._fumbles[index],
            player._rush_attempts[index],
            player._rush_yards[index],
            player._rush_touchdowns[index]
        )
    else:
        sql = pl_sql.addQbSeasonStat.format(
            pl_sql.SCHEMANAME,
            player._player_id,
            season,
            player._attempted_passes[index],
            player._completed_passes[index],
            player._passing_yards[index],
            player._interceptions_thrown[index],
            player._passing_touchdowns[index],
            player._fumbles[index],
            player._rush_attempts[index],
            player._rush_yards[index],
            player._rush_touchdowns[index]
        )
    transaction(conn, sql)

def addRbStats(conn, player, index):
    # _rush_attempts, _fumbles, _rush_yards, _rush_touchdowns, _receptions, _receiving_yards, _recieving_touchdowns
    season = player._season[index]
    if season == 'Career':
        sql = pl_sql.addRbCareerStat.format(
            pl_sql.SCHEMANAME,
            player._player_id,
            player._fumbles[index],
            player._rush_attempts[index],
            player._rush_yards[index],
            player._rush_touchdowns,
            player._receptions[index],
            player._receiving_yards[index],
            player._recieving_touchdowns[index]
        )
    else:
        sql = pl_sql.addRbSeasonStat.format(
            pl_sql.SCHEMANAME,
            player._player_id,
            season,
            player._fumbles[index],
            player._rush_attempts[index],
            player._rush_yards[index],
            player._rush_touchdowns[index],
            player._receptions[index],
            player._receiving_yards[index],
            player._recieving_touchdowns[index]
        )
    transaction(conn, sql)

def addWrTeStats(conn, player, index):
    # _fumbles, _receptions, _receiving_yards, _recieving_touchdowns
    season = player._season[index]
    if season == 'Career':
        sql = pl_sql.addWrCareerStat.format(
            pl_sql.SCHEMANAME,
            player._player_id,
            player._fumbles[index],
            player._receptions[index],
            player._receiving_yards[index],
            player._recieving_touchdowns[index]
        )
    else:
        sql = pl_sql.addWrSeasonStat.format(
            pl_sql.SCHEMANAME,
            player._player_id,
            season,
            player._fumbles[index],
            player._receptions[index],
            player._receiving_yards[index],
            player._recieving_touchdowns[index]
        )
    transaction(conn, sql)

def addKickStats(conn, player, index):
    # _field_goals_attempted, _field_goals_made
    season = player._season[index]
    if season == 'Career':
        sql = pl_sql.addKCareerStat.format(
            pl_sql.SCHEMANAME,
            player._player_id,
            player._field_goals_attempted[index],
            player._field_goals_made[index]
        )
    else:
        sql = pl_sql.addKCareerStat.format(
            pl_sql.SCHEMANAME,
            season,
            player._player_id[index],
            player._field_goals_attempted[index],
            player._field_goals_made[index]
        )
    transaction(conn, sql)

def addTeamYears(conn, player, index):
    sql = pl_sql.addPlayerTeamYear.format(
        pl_sql.SCHEMANAME,
        player._player_id,
        player._team_abbreviation[index],
        player._season[index]
    )
    transaction(conn, sql)

def addMetadata(conn, player, pos):
    sql = pl_sql.addPlayerMetadata.format(
        pl_sql.SCHEMANAME, 
        player._player_id, 
        player._name, 
        pos, 
        player._birth_date, 
        player._height
    )
    transaction(conn, sql)

def addPlayerDataPerPosition(conn, player):
    # awful, but assume player is same position
    # their whole career...
    pos = player._position[len(player._position)-2]
    addMetadata(conn, player, pos)
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
