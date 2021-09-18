from DataCollection.core import scrapper_matches as sm, mysql_management
from datetime import datetime
from DataCollection.core import utils
from DataCollection.properties import properties
import concurrent.futures

mysql_con = mysql_management.MySQLManager()


def get_urls_live_matches(now=datetime.now()):
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S").split(" ")[1]
    time_now = utils.time_to_double(dt_string.split(":")[0]+":"+dt_string.split(":")[1].split(":")[0])

    active_matches = mysql_con.select_table("active_matches",
                                            "{0} - time_match between {1} and {2}"
                                            .format(time_now, properties.threshold_time, properties.max_threshold_time)
                                            )[["URL", "TIME_MATCH"]]

    id_matches = list(set(active_matches["URL"].tolist()))

    return id_matches


#This method will be executed each minute in order to collect the stats
def process_live_matches():
    id_matches_live = get_urls_live_matches()

    num_workers = properties.num_workers_life
    splitted_matches = list(utils.split(id_matches_live, num_workers))

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = []
        for url_matches in splitted_matches:
            futures.append(executor.submit(predict_live_matches, url_matches))


def predict_live_matches(url_matches: list):
    data_matches = sm.Scrapper().get_stats_matches(url_matches)

    for data_match in data_matches:
        print(data_match)

        #TO DO - PREDICT TARGET CORNER FOR THIS MATCH