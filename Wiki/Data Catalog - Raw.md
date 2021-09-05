# Data Catalog - Raw

There're usually matches every weekend (Friday - Saturday- Sunday - Monday). Occasionally, there're also Tuesday - Wednesday - Thursday.

**Leagues collected**: Spain, Italy, England, France and Germany.  
**Seasons**: 2014/2015 to 2020/2021
**Number of rounds**: 1-38 rounds by season. 
**Number of matches collected**: About 11.500

## 1- Match

**Frecuency:** Incremental - At 08:00 every Tuesday (After weekend). 

| NAME | TYPE | NULL | DESCRIPTION
|--|--|--|--|
| ID | VARCHAR (10) | N | ID |
| LEAGUE | VARCHAR (20) | N | SPAIN, ITALY, ENGLAND, FRANCE, GERMANY |
| ROUND | INTEGER | N | ROUND OF THE SEASON (1-38) |
| TEAM_HOME | VARCHAR (50) | N | NAME OF HOME TEAM |
| TEAM_AWAY | VARCHAR (50) | N | NAME OF AWAY TEAM |
| DATE_MATCH | DATE | N | DATE OF THE MATCH (2020-05-05) |
| GOALS_H | INTEGER | N | GOALS DONE BY HOME TEAM |
| GOALS_A | INTEGER | N | GOALS DONE BY AWAY TEAM |
| TEAM_HOME | VARCHAR (50) | N | NAME OF HOME TEAM |
| ODDS_HOME | DOUBLE | N | ODDS 1 - 1.83 |
| ODDS_HOME_X | DOUBLE | N | ODDS 1X - 1.15 |
| ODDS_AWAY | DOUBLE | N | ODDS 2 - 1.83 |
| ODDS_AWAY_X | DOUBLE | N | ODDS X2 - 1.15 |
| STATS_HOME_TOTAL_MATCH | VARCHAR(10) | N | ID STATS TOTAL OF HOME TEAM |
| STATS_HOME_FIRSTTIME_MATCH | VARCHAR(10) | N | ID STATS FOR THE FIRST TIME OF HOME TEAM |
| STATS_HOME_TOTAL_MATCH | VARCHAR(10) | N | ID STATS FOR THE SECOND TIME OF HOME TEAM |
| STATS_AWAY_TOTAL_MATCH | VARCHAR(10) | N | ID STATS TOTAL OF AWAY TEAM |
| STATS_AWAY_FIRSTTIME_MATCH | VARCHAR(10) | N | ID STATS FOR THE FIRST TIME OF AWAY TEAM |
| STATS_AWAY_TOTAL_MATCH | VARCHAR(10) | N | ID STATS FOR THE SECOND TIME OF AWAY TEAM |
| CORNERS_MIN_HOME | VARCHAR(255) | N | MINUTE WHEN CORNERS HAPPENED FOR HOME TEAM - 25;45;78;90 |
| CORNERS_MIN_AWAY | VARCHAR(255) | N | MINUTE WHEN CORNERS HAPPENED FOR AWAY TEAM - 25;45;78;90 |
| GOALS_MIN_HOME | VARCHAR(255) | N | MINUTE WHEN GOALS HAPPENED FOR HOME TEAM - 5;66 |
| GOALS_MIN_AWAY | VARCHAR(255) | N | MINUTE WHEN GOALS HAPPENED FOR AWAY TEAM - 86 |

##
## 2- STATS MATCHES

**Frecuency:** Incremental - At 08:00 every Tuesday (After weekend). 6 records by match (**Home team:** All match, first time and second time. **Away team:** All match, first time and second time)

| NAME | TYPE | NULL | DESCRIPTION
|--|--|--|--|
| ID | VARCHAR (10) | N | ID |
| BALL_POSSESSION | INTEGER | N | Ex: 50
| GOAL_ATTEMPTS | INTEGER | N | TOTAL SHOTS - 15 |
| SHOTS_ON_GOAL | INTEGER | N | SHOTS WHICH CAN BE GOAL - 4 |
| TEAM_AWAY | INTEGER | N | SHOTS OFF GOAL - 11|
| BLOCKED_SHOTS | INTEGER | N | SHOTS WHICH ARE BLOCKED BEFORE ARRIVING TO GOAL |
| FREE_KICKS | INTEGER | N | FREE KICKS |
| CORNERS | INTEGER | N | HOW MANY CORNERS? |
| OFFSIDES | INTEGER | N | OFFSIDES |
| THROW_IN | INTEGER | N |  |
| GOALKEEPER_SAVES | INTEGER | N |  SHOTS WHICH ARE BLOCKED BY THE GOALKEEPER  |
| FOULS | INTEGER | N | FOULS |
| YELLOW_CARDS | INTEGER | N | YELLOW CARDS |
| RED_CARDS | INTEGER | N | RED CARDS |
| COMPLETED_PASSES | INTEGER | N | HOW MANY PASSES? |
| TACKLES | INTEGER | N | TACKLES |
| ATTACKS | INTEGER | N | HOW MANY ATTACKS? |
| DANGEROUS_ATTACKS | INTEGER | N | HOW MANY DANGEROUS ATTACKS? |

##
## 3- FINISHED MATCHES URL

**Frecuency:** Incremental - At 08:00 every Tuesday (After weekend). This tables is queried for getting the urls asociated with finished matches. The aim is to save this urls for their future use. 

| NAME | TYPE | NULL | DESCRIPTION
|--|--|--|--|
| ID | VARCHAR (10) | N | ID |
| URL | VARCHAR (10) | N | URL: Example https://www.flashscore.es/partido/YN3p7dNn/#resumen-del-partido/estadisticas-del-partido/0 |

##
## 3- ACTIVE MATCHES URL

**Frecuency:** Incremental - At 08:00 every day for getting url of today matches and proccesing them for the day. 

This table is used for querying live matches in the middletime. If time of the match minus the current time is between 45 min - 75 min, the url is proccessed. 

| NAME | TYPE | NULL | DESCRIPTION
|--|--|--|--|
| ID | VARCHAR (10) | N | ID |
| URL | VARCHAR (10) | N | URL: Example https://www.flashscore.es/partido/YN3p7dNn/#resumen-del-partido/estadisticas-del-partido/0 |
| TIME | DOUBLE | N | TIME OF THE MATCH CASTED TO DOUBLE - 15:30 -> 15.5 |
