import pytest
from core import scrapper_matches

@pytest.mark.parametrize("website_path",
                         [(["file:///C:/Users/Cesar/Documents/Apuestas/ml_corners_predictor/DataEnginnering/DataCollection/test/websites_examples/finished_match1º.mhtml"])])
def test_get_stats_matches(website_path: str):
    scrapper = scrapper_matches.Scrapper()
    scrapper.get_stats_match()