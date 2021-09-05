import pytest
from live import live_data

@pytest.mark.parametrize("website_path",
                         [("file:///C:/Users/Cesar/Documents/Apuestas/ml_corners_predictor/DataEnginnering/DataCollection/test/websites_examples/mismarcadores_live.mhtml")])
def test_get_today_matches(website_path: str):
    live_data.collect_current_day_matches(url_football_matches=website_path)