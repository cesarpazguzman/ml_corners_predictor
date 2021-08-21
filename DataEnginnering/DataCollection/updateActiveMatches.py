import time
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from core import utils, mysql_management

path_exec_chrome = "C:/Users/Cesar/Documents/Apuestas/chromedriver.exe"
url_football_matches = "https://www.flashscore.es/?rd=mismarcadores.com"
mysql_con = mysql_management.MySQLManager()

def updateActiveMatches():
    driver = webdriver.Chrome(path_exec_chrome, options=utils.options)

    driver.get(url_football_matches)
    time.sleep(2)

    stmt = "INSERT INTO cornersSecond.active_matches (id, url) VALUES (%s, %s)"
    urls = []

    c = driver.page_source
    soup = BeautifulSoup(c, "html.parser")
    live_matches = soup.find_all("div", {"class": "event__match--live"})

    mysql_con.deleteAllRecords("cornersSecond.active_matches")

    for match in live_matches:
        minute = match.find_all("div", {"class": "event__stage--block"})
        minute = minute and minute[0] and minute[0].get_text() or False

        if minute and (minute == 'Descanso' or utils.getNumber(minute) <= 75):
            print(minute)
            urls.append((len(urls), "https://www.flashscore.es/partido/{0}/#estadisticas-del-partido;0".format(
                match.get("id").replace("g_1_", ""))))

    print(len(urls), urls)

    mysql_con.executeMany(stmt, urls)

    driver.close()