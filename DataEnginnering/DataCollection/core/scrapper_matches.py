import time

from core.driver_manager import DriverManager
from core import mysql_management
from core import properties

class Scrapper:

    def __init__(self):
        self.driverManager = DriverManager()
        self.mysql_con = mysql_management.MySQLManager()
        self.stats_to_insert = []
        self.matches_to_insert = []
        self.current_batch_insert = 0

    def get_stats_match(self, id_matches):
        last = id_matches[-1]
        for id_match in id_matches:
            url = "https://www.flashscore.es/partido/{0}/#resumen-del-partido/estadisticas-del-partido/0".format(id_match)
            self.driverManager.get(url, 1)
            soup = self.driverManager.soup

            data = {"id_match": id_match}

            if "Remates" not in self.driverManager.c or "Posesión de balón" not in self.driverManager.c \
                    or "Córneres" not in self.driverManager.c:
                print("The match {0} doesn't have the minimum requirements".format(id_match))
                continue

            try:
                outcome = self.driverManager.find_elem(soup, "div", "wrapper___3rU3Jah", "outcome", 0)
                data["goals_h"] = outcome.find_all("span")[0].get_text()
                data["goals_a"] = outcome.find_all("span")[2].get_text()
                data["time"] = self.driverManager.find_elem(soup,"div", "startTime___2oy0czV", "time", 0).get_text().split(" ")[0]
                data["round"] = self.driverManager.find_elem(soup,"span", "country___24Qe-aj", "round", 0).get_text().split("Jornada ")[1]
                data["league"] = self.driverManager.find_elem(soup, "span", "country___24Qe-aj", "round", 0).get_text().split(" - ")[0]\
                    .split(":")[0]

                data["teamH"] = self.driverManager.find_elem(soup, "div", "participantName___3lRDM1i overflow___cyQxKBr", "teamH", 0)\
                    .find("a").get_text()
                data["teamA"] = self.driverManager.find_elem(soup, "div", "participantName___3lRDM1i overflow___cyQxKBr", "teamA", 1)\
                    .find("a").get_text()

                data["odds_h"], data["odds_a"], data["odds_hx"], data["odds_ax"] = self.get_cuotas()

                data["stats_total"] = self.get_stats()
                data["stats_first_time"] = self.get_stats_time(
                    "https://www.flashscore.es/partido/{0}/#resumen-del-partido/estadisticas-del-partido/1".format(id_match))
                data["stats_second_time"] = self.get_stats_time(
                    "https://www.flashscore.es/partido/{0}/#resumen-del-partido/estadisticas-del-partido/2".format(
                        id_match))

                data["comments"] = self.get_comments(id_match, data["teamH"], data["teamA"])

                print(self.current_batch_insert, data)
                self.insert_data_match(data, last == id_match)

            except:
                print("Error unknown scrapping {0}".format(id_match))

        self.driverManager.quit()

    def get_cuotas(self):
        soup = self.driverManager.soup
        try:

            odd_h = self.driverManager.find_elem(soup, "div", "cellWrapper___2KG4ULl", "odd_h", 0)\
                .find_all("span")[0].find_all("span")[1].get_text()
            odd_a = self.driverManager.find_elem(soup, "div", "cellWrapper___2KG4ULl", "odd_h", 2)\
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

    def get_stats_time(self, url):
        self.driverManager.get(url, 1)
        return self.get_stats()

    def get_stats(self):
        stats_match = self.driverManager.find_elem(self.driverManager.soup, "div", "statRow___3x8JuS9", "stats")
        i = 0
        stats = {}
        while True:
            try:
                val1 = self.driverManager.find_elem(stats_match[i], "div", "homeValue___Al8xBea", "val1", 0).get_text()
                title = self.driverManager.find_elem(stats_match[i], "div", "categoryName___3Keq6yi", val1, 0).get_text()
                val2 = self.driverManager.find_elem(stats_match[i], "div", "awayValue___SXUUfSH", val1, 0).get_text()

                stats[title] = {"Home": val1, "Away": val2}
                i += 1
            except: break

        return stats

    def get_comments(self, idPartido, teamH, teamA):
        self.driverManager.get(
            "https://www.flashscore.es/partido/{0}/#resumen-del-partido/comentarios-en-directo/0".format(idPartido), 1)
        list_comments = {teamH: {"gol":[], "corners":[]},
                         teamA: {"gol":[], "corners":[]}}

        comments = self.driverManager.find_elem(self.driverManager.soup, "div", "row___2o4yBki", "comments")

        for comment in comments:
            type_comment = "corners" if comment.find_all("svg",{"class":"corner___qyvhu5w"}) else False
            if type_comment:
                comment_text = self.driverManager.find_elem(comment, "div", "comment___1wPYbke", "comment_text", 0).get_text()
                comment_time = self.driverManager.find_elem(comment, "div", "time___13X5bGP", "comment_text", 0).get_text().replace("'", "")
                comment_team = teamH.split(" ")[0] in comment_text and teamH or \
                               teamA.split(" ")[0] in comment_text and teamA or False

                if comment_team: list_comments[comment_team][type_comment].append(comment_time)

        self.driverManager.get(
            "https://www.flashscore.es/partido/{0}/#resumen-del-partido/resumen-del-partido".format(idPartido), 1)

        events_home = self.driverManager.find_elem(self.driverManager.soup, "div",
                                                   "summaryVerticalScore___3x0kuLg homeParticipant___1RqKe4V", "events_home")

        for event in events_home:
            if event.find_all("svg", {"class":"footballGoal___a0A1PzP"}):
                gol_time = self.driverManager.find_elem(event, "div", "timeBox___16CXu5a", "gol_time_h", 0).get_text()
                list_comments[teamH]["gol"].append(gol_time)

        events_away = self.driverManager.find_elem(self.driverManager.soup, "div",
                                                   "summaryVerticalScore___3x0kuLg awayParticipant___o6T_Xev",
                                                   "events_away")
        for event in events_away:
            if event.find_all("svg", {"class": "footballGoal___a0A1PzP"}):
                gol_time = self.driverManager.find_elem(event, "div", "timeBox___16CXu5a", "gol_time_a", 0).get_text()
                list_comments[teamA]["gol"].append(gol_time)

        return list_comments

    def insert_data_match(self, data, force_insert=False):
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

        corners_min_h = ";".join([min.replace("'", "").replace("90+", "9")[:2] for min in data["comments"][data["teamH"]]["corners"]])
        corners_min_a = ";".join([min.replace("'", "").replace("90+", "9")[:2] for min in data["comments"][data["teamA"]]["corners"]])
        goals_min_h = ";".join([min.replace("'", "").replace("90+", "9")[:2] for min in data["comments"][data["teamH"]]["gol"]])
        goals_min_a = ";".join([min.replace("'", "").replace("90+", "9")[:2] for min in data["comments"][data["teamA"]]["gol"]])
        self.matches_to_insert.append((id_match, data["league"], data["round"], data["teamH"], data["teamA"], data["time"],
                                       data["goals_h"], data["goals_a"], data["odds_h"], data["odds_hx"], data["odds_a"], data["odds_ax"],
                                       id_match+"HT", id_match+"H1", id_match+"H2", id_match+"AT", id_match+"A1",
                                       id_match+"A2", corners_min_h, corners_min_a, goals_min_h, goals_min_a))
        self.current_batch_insert += 1

        if self.current_batch_insert == properties.batch_size_inserts or force_insert:
            self.mysql_con.execute_many(properties.stmt_stats, self.stats_to_insert)
            time.sleep(2)
            self.mysql_con.execute_many(properties.stmt_match, self.matches_to_insert)
            self.current_batch_insert = 0
            self.stats_to_insert = []
            self.matches_to_insert = []

    def insert_stats(self, id_match, stats, h_a):
        ball_possession = stats["Posesión de balón"][h_a].replace('%', '')
        goal_attempts = stats["Remates"][h_a]
        corners = stats["Córneres"][h_a]
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

    def get_all_matches_url(self, urls_league, url_finished_present):
        driverManager = DriverManager(adult_accept=False, headless=False)

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

        self.mysql_con.execute_many(properties.stmt_finished_matches, urls_to_insert)

        driverManager.quit()
