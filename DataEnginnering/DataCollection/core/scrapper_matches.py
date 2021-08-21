from core.driver_manager import DriverManager


class Scrapper:
    driverManager = None

    def __init__(self):
        self.driverManager = DriverManager()

    def get_stats_match(self, url_matches):
        for url in url_matches:
            self.driverManager.get(url, 1)

            if "Remates" not in self.driverManager.c or "Posesión de balón" not in self.driverManager.c \
                    or "Córneres" not in self.driverManager.c:
                print("El partido no cumple con los requisitos")
                continue

            idPartido = url.replace("https://www.flashscore.es/partido/", "")\
                .replace("/#resumen-del-partido/estadisticas-del-partido/0", "")
            resultado = self.driverManager.soup.find_all("div", {"class":"wrapper___3rU3Jah"})[0]
            golesL = resultado.find_all("span")[0].get_text()
            golesV = resultado.find_all("span")[2].get_text()
            time = self.driverManager.soup.find_all("div",{"class":"startTime___2oy0czV"})[0].get_text().split(" ")[0]
            jornada = self.driverManager.soup.find_all("span",{"class":"country___24Qe-aj"})[0].get_text().split("Jornada ")[1]
            teamH = ((
                self.driverManager.soup.find_all("div", {"class": "participantName___3lRDM1i overflow___cyQxKBr"})))[0]\
                .find("a").get_text()
            teamA = ((
                self.driverManager.soup.find_all("div", {"class": "participantName___3lRDM1i overflow___cyQxKBr"})))[1]\
                .find("a").get_text()

            cuotaL, cuotaV, cuota1X, cuotaX2 = self.get_cuotas()

            stats_total = self.get_stats()
            stats_first_time = self.get_stats_time(
                "https://www.flashscore.es/partido/{0}/#resumen-del-partido/estadisticas-del-partido/1".format(idPartido))
            stats_second_time = self.get_stats_time(
                "https://www.flashscore.es/partido/{0}/#resumen-del-partido/estadisticas-del-partido/2".format(
                    idPartido))

            print(idPartido, time, jornada, teamH,'-', teamA, golesL, golesV, cuotaL, cuotaV, cuota1X, cuotaX2, stats_total,
                  stats_first_time, stats_second_time)

            comments = self.get_comments(idPartido, teamH, teamA)

            print(comments)

        self.driverManager.quit()

    def get_cuotas(self):
        try:
            cuotaL = self.driverManager.soup.find_all("div", {"class":"cellWrapper___2KG4ULl"})[0]\
                .find_all("span")[0].find_all("span")[1].get_text()
            cuotaV = self.driverManager.soup.find_all("div", {"class":"cellWrapper___2KG4ULl"})[2]\
                .find_all("span")[0].find_all("span")[1].get_text()
        except:
            cuotaL = -1
            cuotaV = -1
        try:
            cuotaX2 = round(1.0 / (1 - (1.0 / float(cuotaL) - 0.05)), 2)
        except:
            cuotaX2= -1

        try:
            cuota1X = round(1.0 / (1 - (1.0 / float(cuotaV) - 0.05)), 2)
        except:
            cuota1X= -1

        return cuotaL, cuotaV, cuota1X, cuotaX2

    def get_stats_time(self, url):
        self.driverManager.get(url, 1)
        return self.get_stats()

    def get_stats(self):
        stats_match = self.driverManager.soup.find_all("div", {"class": "statRow___3x8JuS9"})
        i = 0
        stats = {}
        while True:
            try:
                val1 = stats_match[i].find_all("div", {"class": "homeValue___Al8xBea"})[0].get_text()
                title = stats_match[i].find_all("div", {"class": "categoryName___3Keq6yi"})[0].get_text()
                val2 = stats_match[i].find_all("div", {"class": "awayValue___SXUUfSH"})[0].get_text()

                stats[title] = {"Local": val1, "Vis": val2}
                i += 1
            except:
                break

        return stats

    def get_comments(self, idPartido, teamH, teamA):
        self.driverManager.get(
            "https://www.flashscore.es/partido/{0}/#resumen-del-partido/comentarios-en-directo/0".format(idPartido), 1)
        list_comments = {teamH: {"gol":[], "corners":[]},
                         teamA: {"gol":[], "corners":[]}}

        comments = self.driverManager.soup.find_all("div", {"class":"row___2o4yBki"})
        for comment in comments:
            type_comment = "corners" if comment.find_all("svg",{"class":"corner___qyvhu5w"}) else False
            if type_comment:
                comment_text = comment.find_all("div", {"class":"comment___1wPYbke"})[0].get_text()
                comment_time = comment.find_all("div", {"class":"time___13X5bGP"})[0].get_text().replace("'", "")
                comment_team = teamH.split(" ")[0] in comment_text and teamH or \
                               teamA.split(" ")[0] in comment_text and teamA or False

                if comment_team: list_comments[comment_team][type_comment].append(comment_time)

        self.driverManager.get(
            "https://www.flashscore.es/partido/{0}/#resumen-del-partido/resumen-del-partido".format(idPartido), 1)

        events_home = self.driverManager.soup.find_all("div", {"class":"summaryVerticalScore___3x0kuLg homeParticipant___1RqKe4V"})
        for event in events_home:
            if event.find_all("svg", {"class":"footballGoal___a0A1PzP"}):
                gol_time = event.find_all("div", {"class":"timeBox___16CXu5a"})[0].get_text().replace("'", "")
                list_comments[teamH]["gol"].append(gol_time)

        events_away = self.driverManager.soup.find_all("div", {
            "class": "summaryVerticalScore___3x0kuLg awayParticipant___o6T_Xev"})
        for event in events_away:
            if event.find_all("svg", {"class": "footballGoal___a0A1PzP"}):
                gol_time = event.find_all("div", {"class": "timeBox___16CXu5a"})[0].get_text().replace("'", "")
                list_comments[teamA]["gol"].append(gol_time)

        return list_comments



