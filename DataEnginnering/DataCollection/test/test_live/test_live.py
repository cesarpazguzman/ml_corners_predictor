import pytest
from live import live_data
import json

@pytest.mark.parametrize("website_path",
                         [("file:///C:/Users/Cesar/Documents/Apuestas/ml_corners_predictor/DataEnginnering/DataCollection/test/test_live/test_data/website_live.mhtml")])
def test_get_today_matches(website_path: str):
    matches_today = live_data.get_records_today_filtered(url_football_matches=website_path)

    with open('test/test_live/test_data/get_today_matches_result.json', 'w') as outfile:
        json.dump(matches_today, outfile)