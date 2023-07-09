from Database import mysql_management
import concurrent.futures
from DataCollection.core import scrapper_matches as sm
from DataCollection.core import utils
from DataCollection.properties import properties
import logging

mysql_con = mysql_management.MySQLManager()

logger = logging.getLogger("logs").getChild(__name__)

def get_all_matches_url(current_season=False):
    logger.info("GET URLS HISTORICAL MATCHES")
    season_leagues_url = mysql_con.select_table("season_leagues_url", sort="ID")[["ID", "URL","LEAGUE"]]

    leagues = list(set(season_leagues_url["LEAGUE"].tolist()))
    num_workers = len(leagues)

    logger.info(f"Leagues: {leagues}. N workers: {num_workers}")

    url_finished_present = mysql_con.select_table("finished_matches")["URL"].tolist()

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = []
        n_worker = 1
        for league in leagues:
            urls = season_leagues_url[season_leagues_url["LEAGUE"] == league]["URL"].tolist()
            futures.append(executor.submit(sm.Scrapper(n_worker).get_all_matches_url, urls, url_finished_present,
                                           current_season))
            n_worker+=1


def get_stats_matches():
    logger.info("STATS MATCHES")
    id_matches = mysql_con.select_table("finished_matches", 
        where="URL NOT IN (SELECT ID FROM football_data.matches) AND INVALID IS FALSE")["URL"].tolist()
    num_workers = (properties.num_workers if len(id_matches)>100 else 2) if len(id_matches)>10 else 1
    splitted_matches = list(utils.split(id_matches, num_workers))

    logger.info("N workers: " + str(num_workers))
    logger.info("N matches: " + str(len(id_matches)))
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = []
        n_worker = 1
        for url_matches in splitted_matches:
            futures.append(executor.submit(sm.Scrapper(n_worker).get_stats_matches, url_matches))
            n_worker+=1
