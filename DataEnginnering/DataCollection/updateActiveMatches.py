from core import utils, mysql_management, driver_manager, properties

url_football_matches = "https://www.flashscore.es/?rd=mismarcadores.com"
mysql_con = mysql_management.MySQLManager()


def updateActiveMatches():
    driverManager = driver_manager.DriverManager(adult_accept=False, headless=False)
    driverManager.get(url_football_matches)
    urls: list = []

    soup = driverManager.soup
    live_matches = soup.find_all("div", {"class": "event__match--live"})

    mysql_con.delete_all_records("football_data.active_matches")

    for match in live_matches:
        minute = match.find_all("div", {"class": "event__stage--block"})
        minute: str = minute and minute[0] and minute[0].get_text() or ""

        if minute != "" and (minute == 'Descanso' or utils.getNumber(minute) <= properties.minute_max_live):
            urls.append((len(urls), "https://www.flashscore.es/partido/{0}/#estadisticas-del-partido;0".format(
                match.get("id").replace("g_1_", ""))))

    print(len(urls), urls)

    mysql_con.execute_many(properties.stmt_active_matches, urls)

    driverManager.quit()