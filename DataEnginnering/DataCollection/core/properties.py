stmt_match: str = """INSERT INTO football_data.matches (id, league, round, team_home, team_away, date_match, goals_h, goals_a,
        odds_home, odds_home_x, odds_away, odds_away_x, stats_home_total_match, stats_home_firsttime_match,
        stats_home_secondtime_match, stats_away_total_match, stats_away_firsttime_match, stats_away_secondtime_match,
        corners_min_home, corners_min_away, goals_min_home, goals_min_away) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""";

stmt_stats: str = """
    INSERT INTO football_data.stats_matches (id, ball_possession, goal_attempts, shots_on_goal, shots_off_goal, 
    blocked_shots, free_kicks, corners, offsides, throw_in, goalkeeper_saves, fouls, yellow_cards, red_cards,
    completed_passes, tackles, attacks, dangerous_attacks) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s, %s)
""";

stmt_finished_matches: str = "INSERT INTO football_data.finished_matches (id, url) VALUES (%s, %s)";

stmt_active_matches: str = "INSERT INTO football_data.active_matches (id, url) VALUES (%s, %s)"

num_workers: int = 10

path_exec_chrome: str = "C:/Users/Cesar/Documents/Apuestas/chromedriver.exe"

mysql_host: str = "localhost"
mysql_user: str = "root"
mysql_password: str = "secret"
mysql_database: str = "football_data"

pymsqyl_url: str = 'mysql+pymysql://root:secret@localhost/football_data'

batch_size_inserts: int = 50

minute_max_live: int = 75
