getTeams = """
    SELECT DISTINCT Name, TeamAbbr
    FROM {0}.team;
"""

teamsWhoBeatUs = """
    SELECT Tm.Name, SUB.HomeScore, SUB.AwayScore
    FROM {0}.Team as TM
    INNER JOIN 
    (SELECT G.Winner as TmAb, G.HomeScore, G.AwayScore
    FROM {0}.Game as G
    NATURAL JOIN {0}.Schedule AS Sc
    NATURAL JOIN {0}.Team as T
    WHERE Sc.TeamAbbr = '{1}' AND Sc.Year=2017 AND G.Winner != '{1}') as SUB
    ON SUB.TmAb = TM.TeamAbbr;
"""

teamWithBestRecordInConference = """
    SELECT Name, Wins, Losses
    FROM {0}.TeamSeasonWithMetadata as TSM
    INNER JOIN
    (SELECT Conference
    FROM {0}.Team
    WHERE TeamAbbr = '{1}') as C 
    ON TSM.Conference = C.Conference
    WHERE TSM.Year = 2017
    ORDER BY TSM.Wins DESC
    LIMIT 1
"""

teamWithBestRecordInDivision = """
    SELECT Name, Wins, Losses
    FROM {0}.TeamSeasonWithMetadata as TSM
    INNER JOIN
    (SELECT Division
    FROM {0}.Team
    WHERE TeamAbbr = '{1}') as C 
    ON TSM.Division = C.Division
    WHERE TSM.Year = 2017
    ORDER BY TSM.Wins DESC
    LIMIT 1 
"""

fiveYearBeatUs = """
    SELECT Sub.WC, T.Name
    FROM 
        (SELECT COUNT(winner) as WC, Winner 
        FROM {0}.fullscheduledata
        where loser = '{1}' AND year > 2012
        GROUP BY Winner
        ORDER BY COUNT(Winner) DESC
        LIMIT 1) as Sub
    Inner Join {0}.Team as T
    ON Sub.Winner = T.TeamAbbr;
"""

fiveYearWeBeat = """
    SELECT Sub.LC, T.Name
    FROM 
        (SELECT COUNT(Loser) as LC, Loser 
        FROM {0}.fullscheduledata
        where winner = '{1}' AND year > 2012
        GROUP BY Loser
        ORDER BY COUNT(Loser) DESC
        LIMIT 1) as Sub
    Inner Join {0}.Team as T
    ON Sub.Loser = T.TeamAbbr;
"""