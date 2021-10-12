import DataCollection.historical.historical_data as historical
import DataCollection.live.live_data as live

#1 Load historical data
#2 Load urls about today matches for proccesing them during the day.

def execute_process(process):
    if process == 1:
        #historical.get_all_matches_url()
        historical.get_stats_matches()
    elif process == 2:
        live.collect_current_day_matches()