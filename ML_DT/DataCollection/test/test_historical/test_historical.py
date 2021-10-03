import pytest
from DataCollection.core import scrapper_matches
from DataCollection.historical import historical_data
import json

@pytest.mark.parametrize("id_match", [("YN3p7dNn")])
def test_get_stats_match(id_match: str):
    scrapper = scrapper_matches.Scrapper()
    data = scrapper.get_stats_match(id_match)

    with open('DataCollection/test/test_historical/test_data/get_stats_match_result.json', 'w') as outfile:
        json.dump(data, outfile)


def test_get_historical_data():
    historical_data.get_all_matches_url(current_season=True)
    historical_data.get_stats_matches()
