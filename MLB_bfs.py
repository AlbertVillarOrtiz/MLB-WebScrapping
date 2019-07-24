# -*- coding: utf-8 -*-
"""
Created on Sun Jul 21 18:41:55 2019

@author: AlbertVillarOrtiz
"""

from bs4 import BeautifulSoup
import requests
import re
from match import Match

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

def normalizeClasificationData(data):
    for i in range(len(data)+1):
        result = data[i].split(":")
        if len(result) > 0:
            del data[i]
            for j in range(len(result)):
                data.insert(i, result[j])
        data[i] = float(data[i])

    return data

def getClasification(match):
    print("1. INICIO EJECUCION RANKING MISMARCADORES\n")
    SITUATIONS = ['overall', 'home', 'away']
    names = []
    clasification = []
    
    for situation in SITUATIONS:
        url = "https://d.mismarcadores.com/x/feed/ss_1_Uanezsbs_GMHpTqQb_table_{}?e={}&hp1={}&hp2={}".format(situation, match.id, match.ids['local'], match.ids['away'])
        website_url = requests.get(url, headers={'X-Fsign': 'SW9D1eZo'}).text
        soup = BeautifulSoup(website_url,"html.parser")

        trClasi = soup.find_all("tr", {"class": "highlight"})
        for i in range(2):
            clasi = trClasi[i].get_text(separator="/").split("/")[0:7]
            del clasi[1]
            clasification.append(normalizeClasificationData(clasi))
            names.append(clasification[i][1])
    
    match.setNamesMatch(names) 
    match.setClasification(clasification[0:2], clasification[2:4], clasification[4:6])
    
    return match

def getH2h(match):
    print("2. INICIO EJECUCION H2H MISMARCADORES\n")
    url = "https://d.mismarcadores.com/x/feed/d_hh_{}_es_1".format(match.id)
    website_url = requests.get(url, headers={'X-Fsign': 'SW9D1eZo'}).text
    soup = BeautifulSoup(website_url,"html.parser")
    h2h = []
    
    tableHome = soup.find_all("table", {"class": "h2h_home"})
    for table in tableHome:
        mHome = []
        matchsHome = table.find_all("tr", {"class": "highlight"})
        for i in range(10):
            mHome.append(matchsHome[i].get_text(separator="/").split("/")[-4])
        print("------------------")
    
    tableAway = soup.find_all("table", {"class": "h2h_away"})
    for table in tableAway:
        mAway = []
        matchsAway = table.find_all("tr", {"class": "highlight"})
        for i in range(10):
            mAway.append(matchsAway[i].get_text(separator="/").split("/")[-4])
        print("------------------")
    
    tableMutual = soup.find_all("table", {"class": "h2h_mutual"})
    for table in tableMutual:
        mMutual = []
        matchsMutual = table.find_all("tr", {"class": "highlight"})
        for i in range(10):
            mMutual.append(matchsMutual[i].get_text(separator="/").split("/")[-4])
        print("------------------")
    
    match.setH2hOverall()
    match.setH2hLocal()
    match.setH2hAway()

def getOdds(match):
    print("2. INICIO EJECUCION ODDS MISMARCADORES\n")
    url = "https://d.mismarcadores.com/x/feed/d_od_{}_es_1_eu".format(match.id)
    website_url = requests.get(url, headers={'X-Fsign': 'SW9D1eZo'}).text
    soup = BeautifulSoup(website_url,"html.parser")
    
    tableMoneyLine = soup.find("table", {"id": "odds_ml"})
    trML = tableMoneyLine.find_all("tr", {"class": "odd"})
    
    for i in range(len(trML)):
        print(trML[i].get_text(separator="/").split("/"))
    print("------------------")
    
    tableOverUnder = soup.find_all("table", id=lambda x: x and x.startswith('odds_ou'))
    for table in tableOverUnder:
        trML = table.find_all("tr", {"class": "odd"})
    
        for i in range(len(trML)):
            print(trML[i].get_text(separator="/").split("/"))
    print("------------------")
            
    tableHandicap = soup.find("table", id=lambda x: x and x.startswith('odds_ah'))
    trML = tableHandicap.find_all("tr", {"class": "odd"})
    
    for i in range(len(trML)):
        print(trML[i].get_text(separator="/").split("/"))
    print("------------------")
    
    

def main():
    ids = getIdMatchs()
    ids = ["WURpHIWA"]
    
    for idMatch in ids:
        match = Match(getIdTeams(idMatch), idMatch)
        #match = getClasification(match)
        match = getH2h(match)
        #getOdds(match)