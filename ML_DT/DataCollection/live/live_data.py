from DataCollection.core import driver_manager, scrapper_matches
from Database import mysql_management
from DataCollection.properties import queries


mysql_con = mysql_management.MySQLManager()
scrapper = scrapper_matches.Scrapper(1)


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
