from core import mysql_management, driver_manager, scrapper_matches, utils
from datetime import datetime
from properties import properties, queries
import concurrent.futures

mysql_con = mysql_management.MySQLManager()
scrapper = scrapper_matches.Scrapper()


def get_records_today(url_football_matches="https://www.flashscore.es/?rd=mismarcadores.com"):
    driver_m = driver_manager.DriverManager(adult_accept=False, headless=False)
    driver_m.get(url_football_matches)
    id_matches: list = []

    mysql_con.delete_all_records("football_data.active_matches")

    possibles_matches = driver_m.driver.find_elements_by_xpath(
        './/div[starts-with(@class,"event__match event__match--scheduled")]')

    for possible_match in possibles_matches:
        id_matches.append(possible_match.get_attribute('id').replace("g_1_", ""))

    driver_m.quit()

    return id_matches

#This method will be executed each morning at 08:00 in order to collect matches of this day for Spain, Italy,
#England, Deutsch and France.
def collect_current_day_matches():
    id_matches = get_records_today()
    records_to_insert = scrapper.get_filtered_active_matches(id_matches)
    mysql_con.execute_many(queries.stmt_active_matches, records_to_insert)

#This method will be executed each minute in order to collect the stats
def process_live_matches():
    id_matches_live = get_urls_live_matches()

    num_workers = properties.num_workers_life
    splitted_matches = list(utils.split(id_matches_live, num_workers))

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = []
        for url_matches in splitted_matches:
            futures.append(executor.submit(scrapper_matches.Scrapper().get_stats_matches, url_matches))


def get_urls_live_matches(now=datetime.now()):
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S").split(" ")[1]
    time_now = utils.time_to_double(dt_string.split(":")[0]+":"+dt_string.split(":")[1].split(":")[0])

    active_matches = mysql_con.select_table("active_matches",
                                            "{0} - time_match between >"
                                            " {1}".format(time_now, properties.threshold_time)
                                            )[["URL", "TIME_MATCH"]]

    id_matches = list(set(active_matches["URL"].tolist()))

    return id_matches
