import DataCollection.historical.historical_data as historical
import DataCollection.live.live_data as live
import DataCollection.core.scrapper_weather as sw
from DataCollection.core import scrapper_matches
import logging

#1 Load historical data
#2 Load urls about today matches for proccesing them during the day.

logger = logging.getLogger("logs").getChild(__name__)

def execute_process(process):
    if process == 1:
        logger.info("Executing process: Historical")
        #historical.get_all_matches_url()
        historical.get_stats_matches()
        #sm = scrapper_matches.Scrapper()
        #data = sm.get_stats_match("CEnQwkhs")
        #sm.insert_data_match(data, True)
        #sw.ScrapperWeather().get_weather_data_historical("","")
    elif process == 2:
        live.collect_current_day_matches()