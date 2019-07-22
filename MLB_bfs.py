# -*- coding: utf-8 -*-
"""
Created on Sun Jul 21 18:41:55 2019

@author: AlbertVillarOrtiz
"""

from bs4 import BeautifulSoup
import requests
import re

def getIdMatchs():
    website_url = requests.get("https://www.mismarcadores.com/beisbol/usa/mlb/partidos/").text
    soup = BeautifulSoup(website_url,"html.parser")
    
    matchsTable = soup.find("div",{"id":"tournament-page-data-fixtures"}).string
    indexes = [m.start() for m in re.finditer('AA÷', matchsTable)]
    ids = []
    for element in indexes:
        test = matchsTable[element:element+12]
        index = test.index("¬")
        ids.append(matchsTable[element+3:element+index])
    
    return ids

def getIdTeams(idMatch):
    url = "https://www.mismarcadores.com/partido/{}/#h2h;overall".format(idMatch)
    website_url = requests.get(url, headers={'X-Fsign': 'SW9D1eZo'}).text
    soup = BeautifulSoup(website_url,"html.parser").text

    constant = "var participantEncodedIds = "
    indexes = [m.start() for m in re.finditer(constant, soup)]
    init = indexes[0] + len(constant)
    finish = init + 35

    test = soup[init:finish]
    index = test.index("];")
    
    return soup[init+2:init+index-1].replace('\'','').split(',')

def getClasification(idMatch):
    print("1. INICIO EJECUCION RANKING MISMARCADORES\n")
    SITUATIONS = ['overall', 'home', 'away']
    ids = getIdTeams(idMatch)
    
    for situation in SITUATIONS:
        url = "https://d.mismarcadores.com/x/feed/ss_1_Uanezsbs_GMHpTqQb_table_{}?e={}&hp1={}&hp2={}".format(situation, idMatch, ids[0], ids[1])
        website_url = requests.get(url, headers={'X-Fsign': 'SW9D1eZo'}).text
        soup = BeautifulSoup(website_url,"html.parser")

        trClasi = soup.find_all("tr", {"class": "highlight"})
        for i in range(2):
            print(trClasi[i].text)
        print("------------------")
        
        

def getH2h(idMatch):
    print("2. INICIO EJECUCION H2H MISMARCADORES\n")
    url = "https://d.mismarcadores.com/x/feed/d_hh_{}_es_1".format(idMatch)
    website_url = requests.get(url, headers={'X-Fsign': 'SW9D1eZo'}).text
    soup = BeautifulSoup(website_url,"html.parser")
    
    tableHome = soup.find_all("table", {"class": "h2h_home"})
    for table in tableHome:
        matchsHome = table.find_all("tr", {"class": "highlight"})
        for i in range(10):
            print(matchsHome[i].text)
        print("------------------")
    
    tableAway = soup.find_all("table", {"class": "h2h_away"})
    for table in tableAway:
        matchsAway = table.find_all("tr", {"class": "highlight"})
        for i in range(10):
            print(matchsAway[i].text)
        print("------------------")
    
    tableMutual = soup.find_all("table", {"class": "h2h_mutual"})
    for table in tableMutual:
        matchsMutual = table.find_all("tr", {"class": "highlight"})
        for i in range(10):
            print(matchsMutual[i].text)
        print("------------------")
    
#ids = getIdMatchs()
ids = ["WURpHIWA"]

for idMatch in ids:
    getClasification(idMatch)
    getH2h(idMatch)