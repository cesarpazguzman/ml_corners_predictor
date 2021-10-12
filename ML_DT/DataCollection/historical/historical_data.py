from Database import mysql_management
import concurrent.futures
from DataCollection.core import scrapper_matches as sm
from DataCollection.core import utils
from DataCollection.properties import properties

mysql_con = mysql_management.MySQLManager()


def get_all_matches_url(current_season=False):
    season_leagues_url = mysql_con.select_table("season_leagues_url", sort="ID")[["ID", "URL","LEAGUE"]]

    leagues = list(set(season_leagues_url["LEAGUE"].tolist()))
    num_workers = len(leagues)

    url_finished_present = mysql_con.select_table("finished_matches")["URL"].tolist()

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = []
        for league in leagues:
            urls = season_leagues_url[season_leagues_url["LEAGUE"] == league]["URL"].tolist()
            futures.append(executor.submit(sm.Scrapper().get_all_matches_url, urls, url_finished_present,
                                           current_season))


def get_stats_matches():
    id_matches = mysql_con.select_table("finished_matches", where="URL NOT IN (SELECT ID FROM football_data.matches)")\
        ["URL"].tolist()
    num_workers = properties.num_workers
    splitted_matches = list(utils.split(id_matches, num_workers))

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = []
        for url_matches in splitted_matches:
            futures.append(executor.submit(sm.Scrapper().get_stats_matches, url_matches))
