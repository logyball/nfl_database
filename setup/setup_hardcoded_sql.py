from os import environ

SCHEMANAME = environ['NFLSUBDB']

createSchema = """
    CREATE SCHEMA IF NOT EXISTS {0};
""".format(SCHEMANAME)

playerTableCreate = """
    CREATE TABLE IF NOT EXISTS {0}.Player(
        PlayerId        varchar     PRIMARY KEY,
        Name            varchar,
        Position        varchar,
        BirthDate       date,
        Height          varchar
    );
""".format(SCHEMANAME)

teamTableCreate = """
    CREATE TABLE IF NOT EXISTS {0}.Team(
        TeamAbbr        varchar     PRIMARY KEY,
        Name            varchar,
        Division        varchar,
        Conference      varchar
    );
""".format(SCHEMANAME)

teamPlayerRelTableCreate = """
    CREATE TABLE IF NOT EXISTS {0}.TeamPlayerRel(
        PlayerId        varchar     NOT NULL REFERENCES {0}.Player(PlayerId), 
        TeamAbbr        varchar     NOT NULL REFERENCES {0}.Team(TeamAbbr), 
        StartYear       integer,
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
        PRIMARY KEY(TeamAbbr, Year)
    );
""".format(SCHEMANAME)

gameTableCreate = """
    CREATE TABLE IF NOT EXISTS {0}.Game(
        GameKey         varchar     PRIMARY KEY,
        Week            integer,
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

addExtraTeams = """
    INSERT INTO {0}.team (teamabbr, name)
    VALUES
    ('OAK', 'Oakland Raiders'),
    ('STL', 'St Louis Rams'),
    ('TEN', 'Tennesse Titans'),
    ('IND', 'Indianapolis Colts'),
    ('BAL', 'Baltimore Ravens'),
    ('HOU', 'Houston Texans'),
    ('ARI', 'Arizona Cardinals'),
    ('LAR', 'Los Angeles Rams'),
    ('LAC', 'Los Angeles Chargers'),
    ('2TM', 'Two Teams'),
    ('3TM', 'Three Teams'),
    ('IDK', 'ERROR TEAM')
""".format(SCHEMANAME)

# have to add this manually because sportsreference sucks
addExtraTeamData = """
    UPDATE {0}.team set
        Division = info.Division,
        Conference = info.Conference
    FROM (VALUES
        ('BAL', 'AFC North', 'AFC'),
        ('RAV', 'AFC North', 'AFC'),
        ('CIN', 'AFC North', 'AFC'),
        ('CLE', 'AFC North', 'AFC'),
        ('PIT', 'AFC North', 'AFC'),
        ('BUF', 'AFC East', 'AFC'),
        ('MIA', 'AFC East', 'AFC'),
        ('NWE', 'AFC East', 'AFC'),
        ('NYJ', 'AFC East', 'AFC'),
        ('HOU', 'AFC South', 'AFC'),
        ('HTX', 'AFC South', 'AFC'),
        ('IND', 'AFC South', 'AFC'),
        ('CLT', 'AFC South', 'AFC'),
        ('JAX', 'AFC South', 'AFC'),
        ('OTI', 'AFC South', 'AFC'),
        ('TEN', 'AFC South', 'AFC'),
        ('DEN', 'AFC West', 'AFC'),
        ('KAN', 'AFC West', 'AFC'),
        ('OAK', 'AFC West', 'AFC'),
        ('RAI', 'AFC West', 'AFC'),
        ('LAC', 'AFC West', 'AFC'),
        ('SDG', 'AFC West', 'AFC'),
        ('CHI', 'NFC North', 'NFC'),
        ('DET', 'NFC North', 'NFC'),
        ('GNB', 'NFC North', 'NFC'),
        ('MIN', 'NFC North', 'NFC'),
        ('DAL', 'NFC East', 'NFC'),
        ('NYG', 'NFC East', 'NFC'),
        ('PHI', 'NFC East', 'NFC'),
        ('WAS', 'NFC East', 'NFC'),
        ('ATL', 'NFC South', 'NFC'),
        ('CAR', 'NFC South', 'NFC'),
        ('NOR', 'NFC South', 'NFC'),
        ('TAM', 'NFC South', 'NFC'),
        ('ARI', 'NFC West', 'NFC'),
        ('CRD', 'NFC West', 'NFC'),
        ('STL', 'NFC West', 'NFC'),
        ('LAR', 'NFC West', 'NFC'),
        ('RAM', 'NFC West', 'NFC'),
        ('SFO', 'NFC West', 'NFC'),
        ('SEA', 'NFC West', 'NFC')
        ) AS info(TeamAbbr, Division, Conference)
    WHERE team.TeamAbbr = info.TeamAbbr;
""".format(SCHEMANAME)

teamSeasonWithMetadataViewCreate = """
    CREATE VIEW {0}.TeamSeasonWithMetadata AS (
        SELECT *
        FROM {0}.Team
        NATURAL JOIN {0}.TeamSeasonStats
    );
""".format(SCHEMANAME)

fullScheduleDataCreate = """
    CREATE VIEW {0}.FullScheduleData AS (
        SELECT *
        FROM {0}.Game
        NATURAL JOIN {0}.Schedule
    );
""".format(SCHEMANAME)