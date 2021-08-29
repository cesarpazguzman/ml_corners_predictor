import updateActiveMatches
from core.scrapper_matches import Scrapper
import historical_data

if __name__ == '__main__':

    historical = True

    #historical_data.get_all_matches_url()

    historical_data.get_stats_matches()
    #if historical_data:
    #    urls_matches = ['lMpp7vVh', 'zwkkBYgh']

    #    scrapper = Scrapper()
    #    scrapper.get_stats_match(urls_matches)
    #else:
    #    updateActiveMatches.updateActiveMatches()