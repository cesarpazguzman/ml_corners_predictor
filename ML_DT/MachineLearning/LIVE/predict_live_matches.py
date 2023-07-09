from DataCollection.core import scrapper_matches as sm
from datetime import datetime
from DataCollection.core import utils
from DataCollection.properties import properties
import concurrent.futures
from sqlalchemy import create_engine

import pandas as pd




def get_urls_live_matches(conn, now=datetime.now()):
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S").split(" ")[1]
    time_now = utils.time_to_double(dt_string.split(":")[0]+":"+dt_string.split(":")[1].split(":")[0])

    print(time_now)

    query = 'SELECT * FROM active_matches WHERE {0} - time_match between {1} and {2}'\
            .format(time_now, properties.threshold_time, properties.max_threshold_time)

    active_matches = pd.read_sql(query, con=conn)[["URL", "TIME_MATCH"]]

    id_matches = list(set(active_matches["URL"].tolist()))

    print(id_matches)
    
    return id_matches


#This method will be executed each minute in order to collect the stats
def process_live_matches():

    num_workers = properties.num_workers_life

    conn = create_engine(properties.pymsqyl_url)

    tablon_m70_less3 = ""#get_tablon(70, False, 3, conn)
    tablon_m63_less4 = ""#get_tablon(63, False, 4, conn)
    tablon_m57_less5 = ""#get_tablon(57, False, 5, conn)

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = []
        #while True:
        id_matches_live = get_urls_live_matches(conn)
        splitted_matches = list(utils.split(id_matches_live, num_workers))
        print(splitted_matches)
        n_worker = 1
        for url_matches in splitted_matches:
            if url_matches!=[]:
                futures.append(executor.submit(predict_live_matches, url_matches,
                tablon_m70_less3, tablon_m63_less4, tablon_m57_less5, n_worker))
                n_worker += 1


def predict_live_matches(url_matches: list, tablon_m70_less3, tablon_m63_less4, tablon_m57_less5, n_worker):
    for id_match in url_matches:
        data = sm.Scrapper(n_worker).get_stats_live_match(id_match)

        if data!={} :
            data_example = """
            {'id_match': 'voC9JWBG', 'goals_h': '1', 'goals_a': '0', 'teamH': 'Cadiz', 'teamA': 'Granada', 'odds_h': '1.20', 
            'odds_a': '41.00', 'odds_hx': 0.98, 'odds_ax': 4.62, 
            'stats_first_time': {'Posesion de balon': {'Home': '34%', 'Away': '66%'}, 'Remates': {'Home': '8', 'Away': '7'}, 
                'Remates a puerta': {'Home': '3', 'Away': '2'}, 'Remates fuera': {'Home': '2', 'Away': '4'}, 
                'Remates rechazados': {'Home': '3', 'Away': '1'}, 'Tiros libres': {'Home': '7', 'Away': '5'}, 
                'Corneres': {'Home': '6', 'Away': '0'}, 'Fueras de juego': {'Home': '2', 'Away': '0'}, 
                'Saques de banda': {'Home': '12', 'Away': '15'}, 'Paradas': {'Home': '2', 'Away': '2'}, 
                'Faltas': {'Home': '3', 'Away': '7'}, 'Tarjetas amarillas': {'Home': '1', 'Away': '1'}, 
                'Pases totales': {'Home': '116', 'Away': '233'}, 'Pases completados': {'Home': '69', 'Away': '182'}, 
                'Tackles': {'Home': '10', 'Away': '6'}, 'Ataques': {'Home': '33', 'Away': '60'}, 
                'Ataques peligrosos': {'Home': '18', 'Away': '31'}}, 
            'comments': {'Cadiz': {'gol': ["32'"], 'corners': []}, 'Granada': {'gol': [], 'corners': []}}}
            """
            print(data)


def get_table_sql(minute, is_upper, quantity, conn):
    
    tablon = pd.read_sql("""
        SELECT m.ID, DATE_MATCH, TEAM_HOME, TEAM_AWAY, CORNERS_MIN_HOME, CORNERS_MIN_AWAY,
        GOALS_MIN_HOME, GOALS_MIN_AWAY
        FROM matches m
        ORDER BY DATE_MATCH asc
        LIMIT 2000""", conn)

    tablon["GOALS_H"] = tablon["GOALS_MIN_HOME"].apply(
        lambda x: len([val for val in list(x.split(";")) if val.isnumeric() and int(val)<minute-3]))
    tablon["GOALS_A"] = tablon["GOALS_MIN_AWAY"].apply(
        lambda x: len([val for val in list(x.split(";")) if val.isnumeric() and int(val)<minute-3]))

    tablon["CORNERS_H"] = tablon["CORNERS_MIN_HOME"].apply(
        lambda x: len([val for val in list(x.split(";")) if val.isnumeric() and int(val)<minute-3]))
    tablon["CORNERS_A"] = tablon["CORNERS_MIN_AWAY"].apply(
        lambda x: len([val for val in list(x.split(";")) if val.isnumeric() and int(val)<minute-3]))

    tablon["TOTAL_CORNERS"] = tablon[["CORNERS_H", "CORNERS_A"]].apply(lambda x: x[0] + x[1], axis=1)

    tablon["CORNERS_H2>60"] = tablon["CORNERS_MIN_HOME"].apply(
            lambda x: len([val for val in list(x.split(";")) if val.isnumeric() and int(val)>minute and int(val)<93]))
    tablon["CORNERS_A2>60"] = tablon["CORNERS_MIN_AWAY"].apply(
        lambda x: len([val for val in list(x.split(";")) if val.isnumeric() and int(val)>minute and int(val)<93]))
    tablon["TOTAL_CORNERS>60"] = tablon[["CORNERS_H2>60", "CORNERS_A2>60"]].apply(lambda x: x[0] + x[1], axis=1)
    
    if is_upper:
        tablon["output"] = tablon[["CORNERS_H2>60", "CORNERS_A2>60"]].apply(lambda x: 1 if x[0]+x[1]> quantity else 0, axis=1)
    else:
        tablon["output"] = tablon[["CORNERS_H2>60", "CORNERS_A2>60"]].apply(lambda x: 1 if x[0]+x[1] < quantity else 0, axis=1)

    return tablon



def get_tablon_windows(tablon):


    tablon["AVG_CORNERSHOMED2_L3"] = tablon.sort_values(by=['DATE_MATCH'], ascending=True)\
                            .groupby(['TEAM_HOME'])['CORNERS_H2>60'].rolling(3, min_periods = 1).mean()\
                            .reset_index(drop=True, level=0)
    tablon["AVG_CORNERSHOMER2_L3"] = tablon.sort_values(by=['DATE_MATCH'], ascending=True)\
                            .groupby(['TEAM_HOME'])['CORNERS_A2>60'].rolling(3, min_periods = 1).mean()\
                            .reset_index(drop=True, level=0)

    tablon["AVG_CORNERSAWAYD2_L3"] = tablon.sort_values(by=['DATE_MATCH'], ascending=True)\
                            .groupby(['TEAM_AWAY'])['CORNERS_A2>60'].rolling(3, min_periods = 1).mean()\
                            .reset_index(drop=True, level=0)
    tablon["AVG_CORNERSAWAYR2_L3"] = tablon.sort_values(by=['DATE_MATCH'], ascending=True)\
                            .groupby(['TEAM_AWAY'])['CORNERS_H2>60'].rolling(3, min_periods = 1).mean()\
                            .reset_index(drop=True, level=0)

    tablon["AVG_CORNERSHOMED2_L5"] = tablon.sort_values(by=['DATE_MATCH'], ascending=True)\
                            .groupby(['TEAM_HOME'])['CORNERS_H2>60'].rolling(5, min_periods = 1).mean()\
                            .reset_index(drop=True, level=0)

    tablon["AVG_CORNERSAWAY2_L5"] = tablon.sort_values(by=['DATE_MATCH'], ascending=True)\
                            .groupby(['TEAM_AWAY'])['TOTAL_CORNERS>60'].rolling(5, min_periods = 1).mean()\
                            .reset_index(drop=True, level=0)
    tablon["AVG_CORNERSAWAYD2_L5"] = tablon.sort_values(by=['DATE_MATCH'], ascending=True)\
                            .groupby(['TEAM_AWAY'])['CORNERS_A2>60'].rolling(5, min_periods = 1).mean()\
                            .reset_index(drop=True, level=0)

    tablon["AVG_CORNERSHOMED1_L3"] = tablon.sort_values(by=['DATE_MATCH'], ascending=True)\
                            .groupby(['TEAM_HOME'])['CORNERS_H'].rolling(3, min_periods = 1).mean()\
                            .reset_index(drop=True, level=0)
    tablon["AVG_CORNERSHOMER1_L3"] = tablon.sort_values(by=['DATE_MATCH'], ascending=True)\
                            .groupby(['TEAM_HOME'])['CORNERS_A'].rolling(3, min_periods = 1).mean()\
                            .reset_index(drop=True, level=0)

    tablon["AVG_CORNERSAWAY1_L3"] = tablon.sort_values(by=['DATE_MATCH'], ascending=True)\
                            .groupby(['TEAM_AWAY'])['TOTAL_CORNERS'].rolling(3, min_periods = 1).mean()\
                            .reset_index(drop=True, level=0)
    tablon["AVG_CORNERSAWAYD1_L3"] = tablon.sort_values(by=['DATE_MATCH'], ascending=True)\
                            .groupby(['TEAM_AWAY'])['CORNERS_A'].rolling(3, min_periods = 1).mean()\
                            .reset_index(drop=True, level=0)

    tablon["AVG_CORNERSHOME1_L5"] = tablon.sort_values(by=['DATE_MATCH'], ascending=True)\
                            .groupby(['TEAM_HOME'])['TOTAL_CORNERS'].rolling(5, min_periods = 1).mean()\
                            .reset_index(drop=True, level=0)
    tablon["AVG_CORNERSHOMED1_L5"] = tablon.sort_values(by=['DATE_MATCH'], ascending=True)\
                            .groupby(['TEAM_HOME'])['CORNERS_H'].rolling(5, min_periods = 1).mean()\
                            .reset_index(drop=True, level=0)
    tablon["AVG_CORNERSHOMER1_L5"] = tablon.sort_values(by=['DATE_MATCH'], ascending=True)\
                            .groupby(['TEAM_HOME'])['CORNERS_A'].rolling(5, min_periods = 1).mean()\
                            .reset_index(drop=True, level=0)

    tablon["AVG_CORNERSAWAY1_L5"] = tablon.sort_values(by=['DATE_MATCH'], ascending=True)\
                            .groupby(['TEAM_AWAY'])['TOTAL_CORNERS'].rolling(5, min_periods = 1).mean()\
                            .reset_index(drop=True, level=0)
    tablon["AVG_CORNERSAWAYD1_L5"] = tablon.sort_values(by=['DATE_MATCH'], ascending=True)\
                            .groupby(['TEAM_AWAY'])['CORNERS_A'].rolling(5, min_periods = 1).mean()\
                            .reset_index(drop=True, level=0)
    tablon["AVG_CORNERSAWAYR1_L5"] = tablon.sort_values(by=['DATE_MATCH'], ascending=True)\
                            .groupby(['TEAM_AWAY'])['CORNERS_H'].rolling(5, min_periods = 1).mean()\
                            .reset_index(drop=True, level=0)

    tablon["DIF_AVGCORNERSL5_HD_CURRENT"] = tablon[["CORNERS_H", "AVG_CORNERSHOMED1_L5"]].apply(lambda x:
                                                                                              x[0] - x[1], axis=1)
    tablon["DIF_AVGCORNERSL5_AD_CURRENT"] = tablon[["CORNERS_A", "AVG_CORNERSAWAYD1_L5"]].apply(lambda x:
                                                                                              x[0] - x[1], axis=1)
    tablon["DIF_AVGCORNERSL5_HR_CURRENT"] = tablon[["CORNERS_A", "AVG_CORNERSHOMER1_L5"]].apply(lambda x:
                                                                                              x[0] - x[1], axis=1)
    tablon["DIF_AVGCORNERSL5_AR_CURRENT"] = tablon[["CORNERS_H", "AVG_CORNERSAWAYR1_L5"]].apply(lambda x:
                                                                                              x[0] - x[1], axis=1)

    tablon["NUM_MATCHESHOME_POSITIVE_L5"] = tablon.sort_values(by=['DATE_MATCH'], ascending=True)\
                            .groupby(['TEAM_HOME'])['output'].rolling(5, min_periods = 1).sum()\
                            .reset_index(drop=True, level=0)
    tablon["NUM_MATCHESAWAY_POSITIVE_L5"] = tablon.sort_values(by=['DATE_MATCH'], ascending=True)\
                        .groupby(['TEAM_AWAY'])['output'].rolling(5, min_periods = 1).sum()\
                        .reset_index(drop=True, level=0)
    
    tablon["AVG_CORNERS_LOSE_HOME"] = tablon[tablon.GOALS_H<tablon.GOALS_A].sort_values(by=['DATE_MATCH'], ascending=True)\
                            .groupby(['TEAM_HOME'])['CORNERS_H2>60'].rolling(5, min_periods = 1).mean()\
                            .reset_index(drop=True, level=0)
    tablon["AVG_CORNERS_WIN_HOME"] = tablon[tablon.GOALS_H>tablon.GOALS_A].sort_values(by=['DATE_MATCH'], ascending=True)\
                            .groupby(['TEAM_HOME'])['CORNERS_H2>60'].rolling(5, min_periods = 1).mean()\
                            .reset_index(drop=True, level=0)
    tablon["AVG_CORNERS_WIN_AWAY"] = tablon[tablon.GOALS_A>tablon.GOALS_H].sort_values(by=['DATE_MATCH'], ascending=True)\
                            .groupby(['TEAM_AWAY'])['CORNERS_A2>60'].rolling(5, min_periods = 1).mean()\
                            .reset_index(drop=True, level=0)
    tablon["AVG_CORNERS_DRAW_HOME"] = tablon[tablon.GOALS_H==tablon.GOALS_A].sort_values(by=['DATE_MATCH'], ascending=True)\
                            .groupby(['TEAM_HOME'])['CORNERS_H2>60'].rolling(5, min_periods = 1).mean()\
                            .reset_index(drop=True, level=0)
    tablon["AVG_CORNERS_DRAW_AWAY"] = tablon[tablon.GOALS_A==tablon.GOALS_H].sort_values(by=['DATE_MATCH'], ascending=True)\
                            .groupby(['TEAM_AWAY'])['CORNERS_A2>60'].rolling(5, min_periods = 1).mean()\
                            .reset_index(drop=True, level=0)

    

    return tablon



def get_tablon_window_agg(tablon):

    df_corners_lose_home=tablon[tablon.GOALS_H<tablon.GOALS_A].sort_values(by=['DATE_MATCH'], ascending=True)\
        .groupby(['TEAM_HOME'])['CORNERS_H2>60'].rolling(3, min_periods = 1).mean()\
        .reset_index( level=0)
    df_corners_lose_away=tablon[tablon.GOALS_H>tablon.GOALS_A].sort_values(by=['DATE_MATCH'], ascending=True)\
        .groupby(['TEAM_AWAY'])['CORNERS_A2>60'].rolling(3, min_periods = 1).mean()\
        .reset_index( level=0)

    df_corners_win_home=tablon[tablon.GOALS_H>tablon.GOALS_A].sort_values(by=['DATE_MATCH'], ascending=True)\
        .groupby(['TEAM_HOME'])['CORNERS_H2>60'].rolling(3, min_periods = 1).mean()\
        .reset_index( level=0)
    df_corners_win_away=tablon[tablon.GOALS_H<tablon.GOALS_A].sort_values(by=['DATE_MATCH'], ascending=True)\
        .groupby(['TEAM_AWAY'])['CORNERS_A2>60'].rolling(3, min_periods = 1).mean()\
        .reset_index( level=0)

    df_corners_draw_home=tablon[tablon.GOALS_H==tablon.GOALS_A].sort_values(by=['DATE_MATCH'], ascending=True)\
        .groupby(['TEAM_HOME'])['CORNERS_H2>60'].rolling(3, min_periods = 1).mean()\
        .reset_index( level=0)
    df_corners_draw_away=tablon[tablon.GOALS_H==tablon.GOALS_A].sort_values(by=['DATE_MATCH'], ascending=True)\
        .groupby(['TEAM_AWAY'])['CORNERS_A2>60'].rolling(3, min_periods = 1).mean()\
        .reset_index( level=0)
    
    for team_home in tablon["TEAM_HOME"].unique().tolist():
        for index, row in tablon[tablon.TEAM_HOME==team_home].iterrows():
            df_corners_lose_home_aux = df_corners_lose_home[df_corners_lose_home.TEAM_HOME==team_home][:-1]
            lst = df_corners_lose_home_aux[df_corners_lose_home_aux.index<=index]["CORNERS_H2>60"].tolist()
            tablon.at[index,"AVG_CORNERS_LOSE_HOME"] = float(lst[-1]) if lst else -1

            df_corners_win_home_aux = df_corners_win_home[df_corners_win_home.TEAM_HOME==team_home][:-1]
            lst = df_corners_win_home_aux[df_corners_win_home_aux.index<=index]["CORNERS_H2>60"].tolist()
            tablon.at[index,"AVG_CORNERS_WIN_HOME"] = float(lst[-1]) if lst else -1

            df_corners_draw_home_aux = df_corners_draw_home[df_corners_draw_home.TEAM_HOME==team_home][:-1]
            lst = df_corners_draw_home_aux[df_corners_draw_home_aux.index<=index]["CORNERS_H2>60"].tolist()
            tablon.at[index,"AVG_CORNERS_DRAW_HOME"] = float(lst[-1]) if lst else -1

    for team_away in tablon["TEAM_AWAY"].unique().tolist():
        for index, row in tablon[tablon.TEAM_AWAY==team_away].iterrows():
            df_corners_lose_away_aux = df_corners_lose_away[df_corners_lose_away.TEAM_AWAY==team_away][:-1]
            lst = df_corners_lose_away_aux[df_corners_lose_away_aux.index<=index]["CORNERS_A2>60"].tolist()
            tablon.at[index,"AVG_CORNERS_LOSE_AWAY"] = float(lst[-1]) if lst else -1

            df_corners_win_away_aux = df_corners_win_away[df_corners_win_away.TEAM_AWAY==team_away][:-1]
            lst = df_corners_win_away_aux[df_corners_win_away_aux.index<=index]["CORNERS_A2>60"].tolist()
            tablon.at[index,"AVG_CORNERS_WIN_AWAY"] = float(lst[-1]) if lst else -1

            df_corners_draw_away_aux = df_corners_draw_away[df_corners_draw_away.TEAM_AWAY==team_away][:-1]
            lst = df_corners_draw_away_aux[df_corners_draw_away_aux.index<=index]["CORNERS_A2>60"].tolist()
            tablon.at[index,"AVG_CORNERS_DRAW_AWAY"] = float(lst[-1]) if lst else -1
            
    return tablon

def get_tablon(minute, is_upper, quantity, conn):
    tablon = get_table_sql(minute, is_upper, quantity, conn)
    tablon = get_tablon_windows(tablon)
    tablon = get_tablon_window_agg(tablon)
    
    columns_drop=["ID", "TEAM_HOME", "TEAM_AWAY",
             
              "CORNERS_A",
              
             "AVG_CORNERS_LOSE_AWAY",
            'CORNERS_H2>60','CORNERS_A2>60', 'TOTAL_CORNERS>60',
             "GOALS_A",
            "NUM_MATCHESAWAY_POSITIVE_L5", "TOTAL_CORNERS", "output"]
    
    tablon = tablon.sort_values(by=["ID"], ascending=True).drop(columns=columns_drop, axis=1)

    return tablon