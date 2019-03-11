SCHEMANAME = "nflDb"

createSchema = """
    CREATE SCHEMA IF NOT EXISTS {0};
""".format(SCHEMANAME)

playerTableCreate = """
    CREATE TABLE IF NOT EXISTS {0}.Player(
        PlayerId        varchar     PRIMARY KEY,
        Name            varchar,
        Position        varchar,
        BirthDate       date,
        Height          varchar,
        Weight          integer
    );
""".format(SCHEMANAME)

teamTableCreate = """
    CREATE TABLE IF NOT EXISTS {0}.Team(
        TeamAbbr        varchar     PRIMARY KEY,
        Name            varchar,
        City            varchar,
        Division        varchar,
        Conference      varchar
    );
""".format(SCHEMANAME)

teamPlayerRelTableCreate = """
    CREATE TABLE IF NOT EXISTS {0}.TeamPlayerRel(
        PlayerId        varchar     NOT NULL REFERENCES {0}.Player(PlayerId), 
        TeamAbbr        varchar     NOT NULL REFERENCES {0}.Team(TeamAbbr), 
        StartYear       integer, 
        EndYear         integer,
        PRIMARY KEY(PlayerId, TeamAbbr, StartYear)
    );
""".format(SCHEMANAME)

teamSeasonStatsCreate = """
    CREATE TABLE IF NOT EXISTS {0}.TeamSeasonStats( 
        TeamAbbr        varchar     NOT NULL REFERENCES {0}.Team(TeamAbbr), 
        Year            integer     NOT NULL, 
        Wins            integer,
        Losses          integer,
        PointsFor       integer,
        PointsAgainst   integer,
        YardsFor        integer,
        YardsAgainst    integer,
        MadePlayoffs    boolean,
        PRIMARY KEY(TeamAbbr, Year)
    );
""".format(SCHEMANAME)

gameTableCreate = """
    CREATE TABLE IF NOT EXISTS {0}.Game(
        GameKey         varchar     PRIMARY KEY, 
        HomeTeam        varchar     NOT NULL REFERENCES {0}.Team(TeamAbbr), 
        AwayTeam        varchar     NOT NULL REFERENCES {0}.Team(TeamAbbr),
        HomeScore       integer,
        AwayScore       integer,
        Winner          varchar     NOT NULL REFERENCES {0}.Team(TeamAbbr), 
        Loser           varchar     NOT NULL REFERENCES {0}.Team(TeamAbbr)      
    )
""".format(SCHEMANAME)

scheduleTableCreate = """
    CREATE TABLE IF NOT EXISTS {0}.Schedule(
        TeamAbbr        varchar     NOT NULL REFERENCES {0}.Team(TeamAbbr), 
        Year            integer     NOT NULL,
        Week            integer     NOT NULL,
        GameKey         varchar     NOT NULL REFERENCES {0}.Game(GameKey),
        PRIMARY KEY(TeamAbbr, Year, Week) 
    )
""".format(SCHEMANAME)

playerGameStatsTableCreate = """
    CREATE TABLE IF NOT EXISTS {0}.PlayerGameStats(
        PlayerId        varchar     NOT NULL REFERENCES {0}.Player(PlayerId), 
        GameKey         varchar     NOT NULL REFERENCES {0}.Game(GameKey),
        PassAttempts    integer,
        PassCompletions integer,
        PassYds         integer,
        Interceptions   integer,
        PassTDs         integer,
        Fumbles         integer,
        RushAttempts    integer,
        RushYds         integer,
        RushTDs         integer,
        Receptions      integer,
        RecTDs          integer,
        RecYds          integer,
        FGAttempts      integer,
        FGMade          integer,
        PRIMARY KEY(PlayerId, GameKey)
    )
""".format(SCHEMANAME)

playerSeasonStatsTableCreate = """
    CREATE TABLE IF NOT EXISTS {0}.PlayerSeasonStats(
        PlayerId        varchar     NOT NULL REFERENCES {0}.Player(PlayerId), 
        Year            integer     NOT NULL,
        PassAttempts    integer,
        PassCompletions integer,
        PassYds         integer,
        Interceptions   integer,
        PassTDs         integer,
        Fumbles         integer,
        RushAttempts    integer,
        RushYds         integer,
        RushTDs         integer,
        Receptions      integer,
        RecTDs          integer,
        RecYds          integer,
        FGAttempts      integer,
        FGMade          integer,
        PRIMARY KEY(PlayerId, Year)
    )
""".format(SCHEMANAME)

playerCareerStatsTableCreate = """
    CREATE TABLE IF NOT EXISTS {0}.PlayerCareerStats(
        PlayerId        varchar     NOT NULL PRIMARY KEY REFERENCES {0}.Player(PlayerId),
        PassAttempts    integer,
        PassCompletions integer,
        PassYds         integer,
        Interceptions   integer,
        PassTDs         integer,
        Fumbles         integer,
        RushAttempts    integer,
        RushYds         integer,
        RushTDs         integer,
        Receptions      integer,
        RecTDs          integer,
        RecYds          integer,
        FGAttempts      integer,
        FGMade          integer
    )
""".format(SCHEMANAME)