CREATE TABLE football_data.matches
(
    ID VARCHAR(10) NOT NULL,
    LEAGUE VARCHAR(20) NOT NULL,
    ROUND INTEGER NOT NULL,
    TEAM_HOME VARCHAR(50) NOT NULL,
    TEAM_AWAY VARCHAR(50) NOT NULL,
    DATE_MATCH DATE NOT NULL,
    GOALS_H INTEGER NOT NULL,
    GOALS_A INTEGER NOT NULL,
    ODDS_HOME DOUBLE NOT NULL,
    ODDS_HOME_X DOUBLE NOT NULL,
    ODDS_AWAY DOUBLE NOT NULL,
    ODDS_AWAY_X DOUBLE NOT NULL,
    STATS_HOME_TOTAL_MATCH VARCHAR(10) NOT NULL,
    STATS_HOME_FIRSTTIME_MATCH VARCHAR(10) NOT NULL,
    STATS_HOME_SECONDTIME_MATCH VARCHAR(10) NOT NULL,
    STATS_AWAY_TOTAL_MATCH VARCHAR(10) NOT NULL,
    STATS_AWAY_FIRSTTIME_MATCH VARCHAR(10) NOT NULL,
    STATS_AWAY_SECONDTIME_MATCH VARCHAR(10) NOT NULL,
    CORNERS_MIN_HOME VARCHAR(255) NOT NULL,
    CORNERS_MIN_AWAY VARCHAR(255) NOT NULL,
    GOALS_MIN_HOME VARCHAR(255) NOT NULL,
    GOALS_MIN_AWAY VARCHAR(255) NOT NULL
)