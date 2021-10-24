import time

from DataCollection.core.driver_manager import DriverManager
from DataCollection.core import utils
from Database import mysql_management
from DataCollection.properties import properties, queries
from DataCollection.core import scrapper_weather

import unidecode


class Scrapper:

    def __init__(self):
        self.driverManager = DriverManager()
        self.scrapper_weather = scrapper_weather.ScrapperWeather()
        self.mysql_con = mysql_management.MySQLManager()
        self.stats_to_insert: list = []
        self.matches_to_insert: list = []
        self.current_batch_insert: int = 0

    def get_stats_match(self, id_match: str) -> dict:
        url = "https://www.flashscore.es/partido/{0}/#resumen-del-partido/estadisticas-del-partido/0".format(id_match)
        self.driverManager.get(url, 1)
        soup = self.driverManager.soup

        data = {"id_match": id_match}

        print(url)
        if "Remates" not in self.driverManager.c or "Posesión de balón" not in self.driverManager.c \
                or "Córneres" not in self.driverManager.c:
            print("The match {0} doesn't have the minimum requirements".format(id_match))
            return {}

        try:
            outcome = self.driverManager.find_elem(soup, "div", "detailScore__wrapper", "outcome", 0)
            data["goals_h"] = outcome.find_all("span")[0].get_text()
            data["goals_a"] = outcome.find_all("span")[2].get_text()

            data["date"] = \
            self.driverManager.find_elem(soup, "div", "duelParticipant__startTime", "date", 0).get_text().split(" ")[0]

            data["time"] = \
            self.driverManager.find_elem(soup, "div", "duelParticipant__startTime", "time", 0).get_text().split(" ")[1]

            data["date"] = data["time"].split(".")[2] + '-' + data["time"].split(".")[1] + '-' + \
                           data["time"].split(".")[0]

            if "Descenso" in self.driverManager.find_elem(soup, "span",
                                                          "tournamentHeader__country", "round", 0).get_text():
                return {}

            data["round"] = \
            self.driverManager.find_elem(soup, "span", "tournamentHeader__country", "round", 0).get_text().split("Jornada ")[1]

            data["league"] = \
            unidecode.unidecode(self.driverManager
                                .find_elem(soup, "span", "tournamentHeader__country", "round", 0).get_text().split(" - ")[0]
                                .split(":")[0])

            data["teamH"] = unidecode.unidecode(self.driverManager.find_elem(
                soup, "div", "participant__participantName participant__overflow", "teamH", 0)
                                                     .find("a").get_text())
            data["teamA"] = unidecode.unidecode(self.driverManager.find_elem(
                soup, "div", "participant__participantName participant__overflow", "teamA", 1)
                                                     .find("a").get_text())

            data["odds_h"], data["odds_a"], data["odds_hx"], data["odds_ax"] = self.get_cuotas()

            data["comments"] = self.get_comments(id_match, data["teamH"], data["teamA"])

            data["stats_total"] = self.get_stats()
            data["stats_first_time"] = self.get_stats_time(
                "https://www.flashscore.es/partido/{0}/#resumen-del-partido/estadisticas-del-partido/1".format(
                    id_match))
            data["stats_second_time"]= self.get_stats_time(
                "https://www.flashscore.es/partido/{0}/#resumen-del-partido/estadisticas-del-partido/2".format(
                    id_match))

            place_weather = self.mysql_con.select_table("stadiums", where=f"TEAM={data['teamH']}")[["PLACE_WEATHER"]]
            data["weather_info"], data["temperature"], data["wind"], data["rain"], data["humidity"], data["cloudy"] = self.scrapper_weather\
                    .get_weather_data_historical(list(set(place_weather["PLACE_WEATHER"].tolist()))[0], data["date"], data["time"])

            return data
        except Exception as ex:
            print("Error unknown scrapping {0}".format(id_match), ex)
            return {}

    def get_stats_matches(self, id_matches: list):
        last = id_matches[-1]
        for id_match in id_matches:
            data = self.get_stats_match(id_match)
            #self.insert_data_match(data, last == id_match)

        self.driverManager.quit()

    def get_stats_live_matches(self, id_matches: list):
        last = id_matches[-1]
        for id_match in id_matches:
            data = self.get_stats_match(id_match)

        self.driverManager.quit()

    def get_cuotas(self):
        soup = self.driverManager.soup
        try:

            odd_h: str = self.driverManager.find_elem(soup, "div", "cellWrapper", "odd_h", 0)\
                .find_all("span")[0].find_all("span")[1].get_text()
            odd_a: str = self.driverManager.find_elem(soup, "div", "cellWrapper", "odd_h", 2)\
                .find_all("span")[0].find_all("span")[1].get_text()
        except:
            odd_h = -1
            odd_a = -1
        try:
            odd_ax = round(1.0 / (1 - (1.0 / float(odd_h) - 0.05)), 2)
        except:
            odd_ax= -1

        try:
            odd_hx = round(1.0 / (1 - (1.0 / float(odd_a) - 0.05)), 2)
        except:
            odd_hx= -1

        return odd_h, odd_a, odd_hx, odd_ax

    def get_stats_time(self, url: str) -> dict:
        self.driverManager.get(url, 1)
        return self.get_stats()

    def get_stats(self) -> dict:
        stats_match = self.driverManager.find_elem(self.driverManager.soup, "div", "statRow", "stats")
        i = 0
        stats = {}
        while True:
            try:
                val1: str = self.driverManager.find_elem(stats_match[i], "div", "statHomeValue", "val1", 0)\
                    .get_text()
                title: str = self.driverManager.find_elem(stats_match[i], "div", "statCategoryName", val1, 0)\
                    .get_text()
                val2: str = self.driverManager.find_elem(stats_match[i], "div", "statAwayValue", val1, 0)\
                    .get_text()

                stats[unidecode.unidecode(title)] = {"Home": val1, "Away": val2}
                i += 1

            except: break

        return stats

    def get_comments(self, id_match: str, team_h: str, team_a: str) -> dict:
        self.driverManager.get(
            "https://www.flashscore.es/partido/{0}/#resumen-del-partido/comentarios-en-directo/0".format(id_match), 1)
        list_comments = {team_h: {"gol":[], "corners":[]},
                         team_a: {"gol":[], "corners":[]}}

        comments = self.driverManager.find_elem(self.driverManager.soup, "div", "soccer__row", "comments")

        for comment in comments:
            comment_text = self.driverManager.find_elem(comment, "div", "soccer__comment", "comment_text", 0) \
                .get_text()
            
            if "lluvia" in comment_text or "llovi" in comment_text or "llover" in comment_text \
                    or "ojado" in comment_text or "temperatura" in comment_text or "calor" in comment_text \
                        or "frío" in comment_text or "frio" in comment_text or "caluroso" in comment_text:
                print(id_match, comment_text)
            
            type_comment = "corners" if comment.find_all("svg",{"class":"corner-ico"}) else False
            if type_comment:
                comment_text = self.driverManager.find_elem(comment, "div", "soccer__comment", "comment_text", 0)\
                    .get_text()
                comment_time = self.driverManager.find_elem(comment, "div", "soccer__time", "comment_text", 0)\
                    .get_text().replace("'", "")
                comment_team = team_h.split(" ")[0] in comment_text and team_h or \
                               team_a.split(" ")[0] in comment_text and team_a or False

                if comment_team: list_comments[comment_team][type_comment].append(comment_time)

        self.driverManager.get(
            "https://www.flashscore.es/partido/{0}/#resumen-del-partido/resumen-del-partido".format(id_match), 1)

        events_home = self.driverManager.find_elem(self.driverManager.soup, "div",
                                                   "smv__participantRow smv__homeParticipant",
                                                   "events_home")

        for event in events_home:
            if event.find_all("svg", {"class":"footballGoal-ico"}):
                gol_time = self.driverManager.find_elem(event, "div", "smv__timeBox", "gol_time_h", 0).get_text()
                list_comments[team_h]["gol"].append(gol_time)

        events_away = self.driverManager.find_elem(self.driverManager.soup, "div",
                                                   "smv__participantRow smv__awayParticipant",
                                                   "events_away")
        for event in events_away:
            if event.find_all("svg", {"class": "footballGoal-ico"}):
                gol_time = self.driverManager.find_elem(event, "div", "smv__timeBox", "gol_time_a", 0).get_text()
                list_comments[team_a]["gol"].append(gol_time)

        return list_comments

    def insert_data_match(self, data: dict, force_insert=False):

        if data !={}:
            id_match = data["id_match"]
            ht = self.insert_stats(id_match + "HT", data["stats_total"], "Home")
            h1 = self.insert_stats(id_match + "H1", data["stats_first_time"], "Home")
            h2 = self.insert_stats(id_match + "H2", data["stats_second_time"], "Home")
            at = self.insert_stats(id_match + "AT", data["stats_total"], "Away")
            a1 = self.insert_stats(id_match + "A1", data["stats_first_time"], "Away")
            a2 = self.insert_stats(id_match + "A2", data["stats_second_time"], "Away")
            self.stats_to_insert.append(ht)
            self.stats_to_insert.append(h1)
            self.stats_to_insert.append(h2)
            self.stats_to_insert.append(at)
            self.stats_to_insert.append(a1)
            self.stats_to_insert.append(a2)

            corners_min_h = ";".join(
                [min.replace("'", "").replace("90+", "9")[:2] for min in data["comments"][data["teamH"]]["corners"]])

            corners_min_a = ";".join(
                [min.replace("'", "").replace("90+", "9")[:2] for min in data["comments"][data["teamA"]]["corners"]])

            goals_min_h = ";".join(
                [min.replace("'", "").replace("90+", "9")[:2] for min in data["comments"][data["teamH"]]["gol"]])

            goals_min_a = ";".join(
                [min.replace("'", "").replace("90+", "9")[:2] for min in data["comments"][data["teamA"]]["gol"]])

            self.matches_to_insert.append((id_match, data["league"], data["round"], data["teamH"], data["teamA"],
                                        data["date"], data["time"], data["goals_h"], data["goals_a"], data["odds_h"], data["odds_hx"],
                                        data["odds_a"], data["odds_ax"], id_match+"HT", id_match+"H1", id_match+"H2",
                                        id_match+"AT", id_match+"A1", id_match+"A2", corners_min_h, corners_min_a,
                                        goals_min_h, goals_min_a, data["weather_info"], data["temperature"], data["rain"],
                                        data["humidity"], data["cloudy"], data["wind"]))

            self.current_batch_insert += 1

        if self.current_batch_insert == properties.batch_size_inserts or force_insert:
            self.mysql_con.execute_many(queries.stmt_stats, self.stats_to_insert)
            time.sleep(2)
            self.mysql_con.execute_many(queries.stmt_match, self.matches_to_insert)
            self.current_batch_insert = 0
            self.stats_to_insert = []
            self.matches_to_insert = []

    def insert_stats(self, id_match: str, stats: dict, h_a: str) -> tuple:
        ball_possession = stats["Posesion de balon"][h_a].replace('%', '')
        goal_attempts = stats["Remates"][h_a]
        corners = stats["Corneres"][h_a]
        shots_on_goal = 0 if "Remates a puerta" not in stats else stats["Remates a puerta"][h_a]
        shots_off_goal = 0 if "Remates fuera" not in stats else stats["Remates fuera"][h_a]
        blocked_shots = 0 if "Remates rechazados" not in stats else stats["Remates rechazados"][h_a]
        free_kicks = 0 if "Tiros libres" not in stats else stats["Tiros libres"][h_a]
        offsides = 0 if "Fueras de juego" not in stats else stats["Fueras de juego"][h_a]
        throw_in = 0 if "Saques de banda" not in stats else stats["Saques de banda"][h_a]
        goalkeeper_saves = 0 if "Paradas" not in stats else stats["Paradas"][h_a]
        fouls = 0 if "Faltas" not in stats else stats["Faltas"][h_a]
        yellow_cards = 0 if "Tarjetas amarillas" not in stats else stats["Tarjetas amarillas"][h_a]
        red_cards = 0 if "Tarjetas rojas" not in stats else stats["Tarjetas rojas"][h_a]
        completed_passes = 0 if "Pases totales" not in stats else stats["Pases totales"][h_a]
        tackles = 0 if "Tackles" not in stats else stats["Tackles"][h_a]
        attacks = 0 if "Ataques" not in stats else stats["Ataques"][h_a]
        dangerous_attacks = 0 if "Ataques peligrosos" not in stats else stats["Ataques peligrosos"][h_a]

        return (id_match, ball_possession, goal_attempts, corners, shots_on_goal, shots_off_goal, blocked_shots,
                free_kicks, offsides, throw_in, goalkeeper_saves, fouls, yellow_cards, red_cards, completed_passes,
                tackles, attacks, dangerous_attacks)

    def get_all_matches_url(self, urls_league: list, url_finished_present: list, current=False):
        driverManager = DriverManager(adult_accept=False, headless=False)

        # If we want to update only the last season
        if current: urls_league = [urls_league[0]]

        urls_to_insert = []
        for url in urls_league:
            driverManager.get(url)
            driverManager.click_button_by_id("onetrust-accept-btn-handler")

            while True:
                #For doing the button visible for selenium, scroll down
                driverManager.scroll_down()
                if not driverManager.check_exists_by_xpath(driverManager.driver,
                                                           './/*[@id="live-table"]/div[1]/div/div/a'): break
                if not driverManager.click_path(driverManager.driver, './/*[@id="live-table"]/div[1]/div/div/a'): break

            count = 0
            for match in driverManager.driver.find_elements_by_xpath(
                    './/div[starts-with(@class,"event__match event__match--static")]'):

                # Si ocurrio un evento en el partido, suspendido o por perdido, pasamos de el
                if driverManager.check_exists_by_xpath(match, './/div[starts-with(@class,"event__stage")]'): continue

                id_match = match.get_attribute('id').replace("g_1_", "")
                count += 1
                if id_match not in url_finished_present:
                    print(count, id_match)
                    urls_to_insert.append((count, id_match))

        self.mysql_con.execute_many(queries.stmt_finished_matches, urls_to_insert)

        driverManager.quit()

    def get_filtered_active_matches(self, id_matches: list):
        records_to_insert = []
        for id_match in id_matches:
            url_match = "https://www.flashscore.es/partido/{0}/#resumen-del-partido".format(id_match)
            print(url_match)
            self.driverManager.get(url_match, 1)
            soup = self.driverManager.soup

            time_match: str = self.driverManager.find_elem(soup,"div", "startTime___2oy0czV", "time", 0)\
                .get_text().split(" ")[1]
            league: str = self.driverManager.find_elem(soup, "span", "country___24Qe-aj", "round", 0)\
                .get_text()

            #Filtering female leagues
            if "Femenina" in league: continue

            league: str = league.split(" - ")[0]

            if league.split(":")[0] not in properties.current_mapping_leagues or \
                league.split(":")[1].strip() != properties.current_mapping_leagues[league.split(":")[0]]: continue

            time_match = utils.time_to_double(time_match)

            records_to_insert.append((len(records_to_insert), id_match, time_match))


        self.driverManager.quit()

        return records_to_insert
