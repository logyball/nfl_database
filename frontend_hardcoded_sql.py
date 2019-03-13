getTeams = """
    SELECT DISTINCT Name, TeamAbbr
    FROM {0}.team;
"""

getDivs = """
    SELECT DISTINCT Division
    FROM {0}.team;
"""

getConf = """
    SELECT DISTINCT Conference
    FROM {0}.team;
"""

getYears = """
    SELECT DISTINCT Year
    FROM {0}.TeamSeasonStats
    ORDER BY Year;
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

whichTeamsForPlayer = """
    SELECT T.Name as TeamName, TPR.StartYear as Year
    FROM nflDb.TeamPlayerRel as TPR
    NATURAL JOIN nflDb.Player as P
    INNER JOIN nflDb.Team as T on TPR.TeamAbbr = T.TeamAbbr
    WHERE P.Name = %s;
"""

playerCareerStats = """
    SELECT *
    FROM nflDb.playerCareerStats as PCS
    INNER JOIN nflDb.Player as P ON P.playerid = PCS.playerid
    WHERE P.Name = %s;
"""

playerLastYearStats = """
    SELECT PSS.playerid, PSS.PassAttempts, PSS.PassCompletions, PSS.PassYds, PSS.Interceptions, PSS.PassTds, PSS.Fumbles, PSS.RushAttempts, PSS.RushYds, PSS.RushTds, PSS.Receptions, PSS.RecTds, PSS.RecYds, PSS.FgAttempts, PSS.FgMade  
    FROM nflDb.playerSeasonStats as PSS
    INNER JOIN nflDb.Player as P ON P.playerid = PSS.playerid
    WHERE P.Name = %s AND PSS.year = 2017;
"""

playerBestTeamByRec = """
    SELECT DISTINCT T.Name, TSS.Year, TSS.Wins, TSS.Losses
    FROM nflDb.TeamPlayerRel as TPR
    NATURAL JOIN nflDb.Player AS P
    INNER JOIN nfldb.teamSeasonStats as TSS ON TSS.teamAbbr = TPR.TeamAbbr
    INNER JOIN nfldb.team as T ON TSS.teamAbbr = T.TeamAbbr
    WHERE P.name = %s and TSS.Wins =

    (SELECT MAX(TSS.wins)
    FROM nflDb.TeamPlayerRel as TPR
    NATURAL JOIN nflDb.Player AS P
    INNER JOIN nfldb.teamSeasonStats as TSS ON TSS.teamAbbr = TPR.TeamAbbr
    WHERE P.name = %s);
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
