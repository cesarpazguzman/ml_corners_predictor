import time
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from core import utils, mysql_management
from pandas import DataFrame
import concurrent.futures
from core.driver_manager import DriverManager

path_exec_chrome = "C:/Users/Cesar/Documents/Apuestas/chromedriver.exe"
mysql_con = mysql_management.MySQLManager()

def get_all_matches_url():

    season_leagues_url = mysql_con.select_table("season_leagues_url")[["URL","LEAGUE"]]
    leagues = list(set(season_leagues_url["LEAGUE"].tolist()))
    num_workers = len(leagues)

    url_finished_present = mysql_con.select_table("finished_matches")["URL"].tolist()
    stmt = "INSERT INTO cornersSecond.finished_matches (id, url) VALUES (%s, %s)"

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = []
        for league in leagues:
            urls = season_leagues_url[season_leagues_url["LEAGUE"] == league]["URL"].tolist()
            futures.append(executor.submit(_get_all_matches_url, urls, url_finished_present))

def _get_all_matches_url(urls_league, url_finished_present):
    driverManager = DriverManager(adult_accept=False)
    for url in urls_league:
        driverManager.get(url)
        driverManager.click_button_by_id("onetrust-accept-btn-handler")

    driverManager.quit()
