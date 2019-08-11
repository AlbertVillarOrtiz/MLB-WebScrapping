# -*- coding: utf-8 -*-
"""
Created on Sat Aug 10 21:12:43 2019

@author: AlbertVillarOrtiz
"""

class Scrapper(self):
    self.__url_leagues = "https://d.mismarcadores.com/x/feed/f_{}_0_2_es_1"
    self.__url_id_match = "https://www.mismarcadores.com/{}/{}partidos/"
    self.__url_id_teams = "https://www.mismarcadores.com/partido/{}/#h2h;overall"
    self.__url_clasification = "https://d.mismarcadores.com/x/feed/ss_1_Uanezsbs_GMHpTqQb_table_{}?e={}&hp1={}&hp2={}"
    self.__url_h2h = "https://d.mismarcadores.com/x/feed/d_hh_{}_es_1"
    self.__url_odd = "https://d.mismarcadores.com/x/feed/d_od_{}_es_1_eu"

    def __init__(self):
        