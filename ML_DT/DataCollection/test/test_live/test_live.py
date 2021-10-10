import pytest
from DataCollection.properties import queries
from DataCollection.core import scrapper_matches
from DataCollection.live import live_data
import json
from datetime import datetime


@pytest.mark.parametrize("website_path",
                         [("file:///C:/Users/Cesar/Documents/Apuestas/ml_corners_predictor/ML_DT/DataCollection/test/test_live/test_data/website_today_matches.mhtml")])
def test_get_today_matches(website_path: str):
    scrapper = scrapper_matches.Scrapper()

    matches_today = scrapper.get_filtered_active_matches(
        live_data.get_records_today(url_football_matches=website_path))

    assert len(matches_today) > 0, "No records matches today."

    with open('DataCollection/test/test_live/test_data/get_today_matches_result.json', 'w') as outfile:
        json.dump(matches_today, outfile)

    live_data.mysql_con.execute_many(queries.stmt_active_matches, matches_today)


@pytest.mark.parametrize("website_path",
                         [("file:///C:/Users/Cesar/Documents/Apuestas/ml_corners_predictor/ML_DT/DataCollection/test/test_live/test_data/website_live_matches.mhtml")])
def test_process_live_matches(website_path: str):
    date_time_str = '18/09/21 16:00:00'

    now = datetime.strptime(date_time_str, '%d/%m/%y %H:%M:%S')

    live_data.get_urls_live_matches(now=now)
