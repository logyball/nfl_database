SCHEMANAME = "nfldb" # env var?

addGameStat = """
    INSERT INTO {0}.Game(
        GameKey,
        Week,
        HomeTeam,
        AwayTeam,
        HomeScore,
        AwayScore,
        Winner,
        Loser
    )
    VALUES ('{1}', {2}, '{3}', '{4}', {5}, {6}, '{7}', '{8}');
"""

addScheduleGame = """
    INSERT INTO {0}.Schedule(
        TeamAbbr,
        Year,
        Week,
        GameKey
    )
    VALUES ('{1}', {2}, {3}, '{4}');
"""

addTeamSeasonStat = """
    INSERT INTO {0}.TeamSeasonStats(
        TeamAbbr,
        Year,
        Wins,
        Losses,
        PointsFor,
        PointsAgainst,
        YardsFor
    )
    VALUES ('{1}', {2}, {3}, {4}, {5}, {6}, {7});
"""