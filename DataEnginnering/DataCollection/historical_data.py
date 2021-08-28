import time
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from core import utils, mysql_management
from pandas import DataFrame
import concurrent.futures
from core.driver_manager import DriverManager
from selenium.webdriver.support import expected_conditions as EC

path_exec_chrome = "C:/Users/Cesar/Documents/Apuestas/chromedriver.exe"
mysql_con = mysql_management.MySQLManager()
stmt_urls = "INSERT INTO football_data.finished_matches (id, url) VALUES (%s, %s)"

def get_all_matches_url():

    season_leagues_url = mysql_con.select_table("season_leagues_url")[["URL","LEAGUE"]]
    leagues = list(set(season_leagues_url["LEAGUE"].tolist()))
    num_workers = len(leagues)

    url_finished_present = mysql_con.select_table("finished_matches")["URL"].tolist()

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = []
        for league in leagues:
            urls = season_leagues_url[season_leagues_url["LEAGUE"] == league]["URL"].tolist()
            futures.append(executor.submit(_get_all_matches_url, urls, url_finished_present))

def _get_all_matches_url(urls_league, url_finished_present):
    driverManager = DriverManager(adult_accept=False)
    urls_to_insert = []
    for url in urls_league:
        driverManager.get(url)
        driverManager.click_button_by_id("onetrust-accept-btn-handler")
        driverManager.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.5)
        while True:
            if not driverManager.check_exists_by_xpath(driverManager.driver, './/*[@id="live-table"]/div[1]/div/div/a'):
                break
            if not driverManager.click_path(driverManager.driver, './/*[@id="live-table"]/div[1]/div/div/a'):
                break
            driverManager.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(0.5)

        count=0
        for match in driverManager.driver.find_elements_by_xpath(
                './/div[starts-with(@class,"event__match event__match--static")]'):

            # Si ocurrio un evento en el partido, suspendido o por perdido, pasamos de el
            if driverManager.check_exists_by_xpath(match, './/div[starts-with(@class,"event__stage")]'): continue

            id_match = match.get_attribute('id').replace("g_1_", "")
            count += 1

            if id_match not in url_finished_present:
                print(count, id_match)
                urls_to_insert.append((count, id_match))

    mysql_con.execute_many(stmt_urls, urls_to_insert)

    driverManager.quit()

