import updateActiveMatches
from core.scrapper_matches import Scrapper
import historical_data

if __name__ == '__main__':

    historical = True

    historical_data.get_all_matches_url()

    #if historical_data:
    #    urls_matches = ['https://www.flashscore.es/partido/0W2sDvzL/#resumen-del-partido/estadisticas-del-partido/0',
    #                    'https://www.flashscore.es/partido/YqNKQc4K/#resumen-del-partido/estadisticas-del-partido/0',
    #                    'https://www.flashscore.es/partido/WKxM5dSf/#resumen-del-partido/estadisticas-del-partido/0']

    #    scrapper = Scrapper()
    #    scrapper.get_stats_match(urls_matches)
    #else:
    #    updateActiveMatches.updateActiveMatches()