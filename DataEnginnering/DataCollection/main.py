from live import live_data
from core.scrapper_matches import Scrapper
from historical import historical_data

if __name__ == '__main__':

    historical = True

    #historical_data.get_all_matches_url()


    if historical:
        urls_matches = ['lMpp7vVh', 'zwkkBYgh']
    #    historical_data.get_stats_matches()
        scrapper = Scrapper()
        scrapper.get_stats_matches(urls_matches)
    else:
        live_data.collect_current_day_matches()
        #live_data.get_stats_live_matches()