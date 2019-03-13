from os import environ

SCHEMANAME = environ['NFLSUBDB']

addQbSeasonStat = """
    INSERT INTO {0}.playerseasonstats(
        PlayerId,
        Year,
        PassAttempts,
        PassCompletions,
        PassYds,
        Interceptions,
        PassTDs,
        Fumbles,
        RushAttempts,
        RushYds,
        RushTDs
    )
    VALUES ('{1}', {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}, {11});
"""

addQbCareerStat = """
    INSERT INTO {0}.playercareerstats(
        PlayerId,
        PassAttempts,
        PassCompletions,
        PassYds,
        Interceptions,
        PassTDs,
        Fumbles,
        RushAttempts,
        RushYds,
        RushTDs
    )
    VALUES ('{1}', {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10});
"""

addQbGameStat = """
    INSERT INTO {0}.playergamestats(
        PlayerId,
        GameKey,
        PassAttempts,
        PassCompletions,
        PassYds,
        Interceptions,
        PassTDs,
        Fumbles,
        RushAttempts,
        RushYds,
        RushTDs
    )
    VALUES ('{1}', '{2}', {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}, {11});
"""

addRbSeasonStat = """
    INSERT INTO {0}.playerseasonstats(
        PlayerId,
        Year,
        Fumbles,
        RushAttempts,
        RushYds,
        RushTDs,
        Receptions,
        RecYds,
        RecTDs
    )
    VALUES ('{1}', {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9});
"""

addRbCareerStat = """
    INSERT INTO {0}.playercareerstats(
        PlayerId,
        Fumbles,
        RushAttempts,
        RushYds,
        RushTDs,
        Receptions,
        RecYds,
        RecTDs
    )
    VALUES ('{1}', {2}, {3}, {4}, {5}, {6}, {7}, {8});
"""

addRbGameStat = """
    INSERT INTO {0}.playergamestats(
        PlayerId,
        GameKey,
        Fumbles,
        RushAttempts,
        RushYds,
        RushTDs,
        Receptions,
        RecYds,
        RecTDs
    )
    VALUES ('{1}', '{2}', {3}, {4}, {5}, {6}, {7}, {8}, {9});
"""

addWrSeasonStat = """
    INSERT INTO {0}.playerseasonstats(
        PlayerId,
        Year,
        Fumbles,
        Receptions,
        RecYds,
        RecTDs
    )
    VALUES ('{1}', {2}, {3}, {4}, {5}, {6});
"""

addWrCareerStat = """
    INSERT INTO {0}.playercareerstats(
        PlayerId,
        Fumbles,
        Receptions,
        RecYds,
        RecTDs
    )
    VALUES ('{1}', {2}, {3}, {4}, {5});
"""

addWrGameStat = """
    INSERT INTO {0}.playergamestats(
        PlayerId,
        GameKey,
        Fumbles,
        Receptions,
        RecYds,
        RecTDs
    )
    VALUES ('{1}', '{2}', {3}, {4}, {5}, {6});
"""

addKSeasonStat = """
    INSERT INTO {0}.playerseasonstats(
        PlayerId,
        Year,
        FGAttempts,
        FGMade
    )
    VALUES ('{1}', {2}, {3}, {4});
"""

addKCareerStat = """
    INSERT INTO {0}.playercareerstats(
        PlayerId,
        FGAttempts,
        FGMade
    )
    VALUES ('{1}', {2}, {3});
"""

addKGameStat =  """
    INSERT INTO {0}.playergamestats(
        PlayerId,
        GameKey,
        FGAttempts,
        FGMade
    )
    VALUES ('{1}', '{2}', {3}, {4});
"""

addPlayerTeamYear = """
    INSERT INTO {0}.teamplayerrel(
        PlayerId,
        TeamAbbr,
        StartYear
    )
    VALUES ('{1}', '{2}', {3});
"""

addPlayerMetadata = """
    INSERT INTO {0}.player(
        PlayerId,
        Name,
        Position,
        BirthDate,
        Height
    )
    VALUES ('{1}', '{2}', '{3}', '{4}', '{5}');
"""

addTeamData = """
    INSERT INTO {0}.team(
        TeamAbbr,
        Name
    )
    VALUES ('{1}', '{2}');
"""