from core import mysql_management, driver_manager, scrapper_matches, utils
from datetime import datetime
from properties import properties, queries

mysql_con = mysql_management.MySQLManager()
scrapper = scrapper_matches.Scrapper()

#This method will be executed each morning at 08:00 in order to collect matches of this day for Spain, Italy,
#England, Deutsch and France.
def collect_current_day_matches(url_football_matches="https://www.flashscore.es/?rd=mismarcadores.com"):
    driver_m = driver_manager.DriverManager(adult_accept=False, headless=False)
    driver_m.get(url_football_matches)
    urls: list = []

    mysql_con.delete_all_records("football_data.active_matches")

    possibles_matches = driver_m.driver.find_elements_by_xpath(
        './/div[starts-with(@class,"event__match event__match--scheduled")]')

    for possible_match in possibles_matches:
        urls.append("https://www.flashscore.es/partido/{0}/#resumen-del-partido".format(
            possible_match.get_attribute('id').replace("g_1_", "")))

    records_to_insert = scrapper.get_filtered_active_matches(urls)
    print(records_to_insert)

    #INSERT URLS
    mysql_con.execute_many(queries.stmt_active_matches, records_to_insert)

    driver_m.quit()


def get_stats_live_matches():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S").split(" ")[1]
    time_now = utils.time_to_double(dt_string.split(":")[0]+":"+dt_string.split(":")[1].split(":")[0])

    active_matches = mysql_con.select_table("active_matches",
                                            "{0} - time_match between >ç"
                                            " {1}".format(time_now, properties.threshold_time)
                                            )[["URL", "TIME_MATCH"]]

    urls = list(set(active_matches["URL"].tolist()))

    print(urls)
