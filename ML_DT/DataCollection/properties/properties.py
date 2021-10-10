
num_workers: int = 10
num_workers_life: int = 5

path_exec_chrome: str = "C:/Users/Cesar/Documents/Apuestas/chromedriver.exe"

mysql_host: str = "localhost"
mysql_user: str = "root"
mysql_password: str = "secret"
mysql_database: str = "football_data"

pymsqyl_url: str = 'mysql+pymysql://root:secret@localhost/football_data'

batch_size_inserts: int = 50

minute_max_live: int = 75

current_mapping_leagues = {"ESPAÑA": "LaLiga Santander", "ALEMANIA": "Bundesliga", "FRANCE": "Ligue 1",
                           "INGLATERRA": "Premier League", "ITALIA": "Serie A"}

#Middletime = 45 minutes = 0.75
threshold_time = 0.75 #First time
middletime = 0.25
minute_75_second_part = 0.5 #30 minutes
max_threshold_time = threshold_time + middletime + minute_75_second_part