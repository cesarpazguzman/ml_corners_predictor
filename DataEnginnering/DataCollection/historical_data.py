from core import mysql_management
import concurrent.futures
from core import scrapper_matches as sm

mysql_con = mysql_management.MySQLManager()

def get_all_matches_url():

    season_leagues_url = mysql_con.select_table("season_leagues_url")[["URL","LEAGUE"]]
    leagues = list(set(season_leagues_url["LEAGUE"].tolist()))
    num_workers = len(leagues)

    url_finished_present = mysql_con.select_table("finished_matches")["URL"].tolist()

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = []
        for league in leagues:
            urls = season_leagues_url[season_leagues_url["LEAGUE"] == league]["URL"].tolist()
            futures.append(executor.submit(sm.Scrapper().get_all_matches_url, urls, url_finished_present))



def get_stats_matches():
    id_matches = mysql_con.select_table("finished_matches")["URL"].tolist()
    num_workers = 10
    splitted_matches = list(split(id_matches, num_workers))

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = []
        for url_matches in splitted_matches:
            futures.append(executor.submit(sm.Scrapper().get_stats_match, url_matches))

def split(a, n):
    k, m = divmod(len(a), n)
    return (a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n))
