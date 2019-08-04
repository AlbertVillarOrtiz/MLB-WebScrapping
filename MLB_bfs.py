# -*- coding: utf-8 -*-
"""
Created on Sun Jul 21 18:41:55 2019

@author: AlbertVillarOrtiz
"""

from bs4 import BeautifulSoup
import requests
import re
import numpy as np
import statistics
from match import Match
from probabilities import Probabilities

def getIdMatchs(sport, league):
    try: 
        url = "https://www.mismarcadores.com/{}/{}partidos/".format(sport, league)
        website_url = requests.get(url).text
        soup = BeautifulSoup(website_url,"html.parser")
        
        matchsTable = soup.find("div",{"id":"tournament-page-data-fixtures"}).string
        indexes = [m.start() for m in re.finditer('AA÷', matchsTable)]
        ids = []
        for element in indexes:
            test = matchsTable[element:element+12]
            index = test.index("¬")
            ids.append(matchsTable[element+3:element+index])
    except:
        ids = []
        
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

def normalizeData(data):
    for i in range(len(data)+1):
        result = data[i].split(":")
        if len(result) > 0:
            del data[i]
            for j in range(len(result)):
                data.insert(i, result[j])
        data[i] = float(data[i])

    return data

def normalizeH2hData(data):
    for i in range(len(data)):
        result = data[i].split(":")
        result[0] = float(result[0])
        result[1] = float(result[1])

    return result

def getSize(array, default):
    if len(array) > default:
        result = default
    else:
        result = len(array)
        
    return result      

def getClasification(match):
    SITUATIONS = ['overall', 'home', 'away']
    clasification = []
    
    try:
        for situation in SITUATIONS:
            url = "https://d.mismarcadores.com/x/feed/ss_1_Uanezsbs_GMHpTqQb_table_{}?e={}&hp1={}&hp2={}".format(situation, match.id, match.idsTeams['home'], match.idsTeams['away'])
            website_url = requests.get(url, headers={'X-Fsign': 'SW9D1eZo'}).text
            soup = BeautifulSoup(website_url,"html.parser")
    
            trClasi = soup.find_all("tr", {"class": "highlight"})
            for i in range(2):
                clasi = trClasi[i].get_text(separator="/").split("/")[0:7]
                length = len(clasification)
                if clasi[1] == match.names['home'] and i%2 != 0:
                    del clasi[1]
                    clasification.insert(length-1, normalizeData(clasi))
                else:
                    del clasi[1]
                    clasification.append(normalizeData(clasi))  
        
        match.setClasification(clasification[0:2], clasification[2:4], clasification[4:6])
    except:
        print("NO CLASIFICATION")
    
    return match

def getH2h(match):
    url = "https://d.mismarcadores.com/x/feed/d_hh_{}_es_1".format(match.id)
    website_url = requests.get(url, headers={'X-Fsign': 'SW9D1eZo'}).text
    soup = BeautifulSoup(website_url,"html.parser")
    h2h = []
    names = []
    
    tableHome = soup.find_all("table", {"class": "h2h_home"})
    for table in tableHome:
        mHome = []
        matchsHome = table.find_all("tr", {"class": "highlight"})
        for i in range(getSize(matchsHome, 10)):
            h2hValues = matchsHome[i].get_text(separator="/").split("/")[-3:]
            h2hValues.extend(normalizeH2hData([h2hValues[-1]]))
            del h2hValues[2]
            mHome.append(h2hValues)
        h2h.append(mHome)
        
    names.append(h2h[-1][-1][0])
    tableAway = soup.find_all("table", {"class": "h2h_away"})
    for table in tableAway:
        mAway = []
        matchsAway = table.find_all("tr", {"class": "highlight"})
        for i in range(getSize(matchsAway, 10)):
            h2hValues = matchsAway[i].get_text(separator="/").split("/")[-3:]
            h2hValues.extend(normalizeH2hData([h2hValues[-1]]))
            del h2hValues[2]
            mAway.append(h2hValues)
        h2h.append(mAway)
        
    names.append(h2h[-1][-1][1])
    tableMutual = soup.find_all("table", {"class": "h2h_mutual"})
    for table in tableMutual:
        mMutual = []
        matchsMutual = table.find_all("tr", {"class": "highlight"})
        for i in range(getSize(matchsMutual, 10)):
            h2hValues = matchsMutual[i].get_text(separator="/").split("/")[-3:]
            h2hValues.extend(normalizeH2hData([h2hValues[-1]]))
            del h2hValues[2]
            mMutual.append(h2hValues)
        h2h.append(mMutual)
    
    match.setH2h(h2h)
    match.setNamesMatch(names)
    
    return match

def getOdds(match):
    url = "https://d.mismarcadores.com/x/feed/d_od_{}_es_1_eu".format(match.id)
    website_url = requests.get(url, headers={'X-Fsign': 'SW9D1eZo'}).text
    soup = BeautifulSoup(website_url,"html.parser")
    
    tableMoneyLine = soup.find("table", {"id": "odds_ml"})
    trML = tableMoneyLine.find_all("tr", {"class": "odd"})
    
    oddsW = []
    oddsOU = {}
    oddsAH = {}
    odds = trML[0].get_text(separator="/").split("/")
    odds.remove('\xa0')
    oddsW = list(map(float, odds))
    
    tableOverUnder = soup.find_all("table", id=lambda x: x and x.startswith('odds_ou'))
    for table in tableOverUnder:
        trML = table.find_all("tr", {"class": "odd"})
    
        for i in range(len(trML)):
            overUnder = trML[i].get_text(separator="/").split("/")
            oddsOU[overUnder[0]] = list(map(float, overUnder[1:3]))
            
    tableHandicap = soup.find("table", id=lambda x: x and x.startswith('odds_ah'))
    trML = tableHandicap.find_all("tr", {"class": "odd"})
    
    for i in range(len(trML)):
        asianHandicap = trML[i].get_text(separator="/").split("/")
        oddsAH[asianHandicap[0]] = list(map(float, asianHandicap[1:3]))
    
    match.setOdds(oddsW, oddsOU, oddsAH)
    
    return match

def getData(idMatch):
    match = Match(getIdTeams(idMatch), idMatch)
    match = getH2h(match)
    match = getClasification(match)
    match = getOdds(match)
    
    return match

def formObjectToProbabilities(array):
    for key in array.keys():
        if isinstance(array[key], (list, tuple, np.ndarray)):
            for i in range(len(array[key])):
                array[key][i] = 1/array[key][i]
        else:
            array[key] = 1/array[key]
    
    return array
    
def setProbabilitiesOdds(match):
    probW = formObjectToProbabilities(match.oddsW)
    probOU = formObjectToProbabilities(match.oddsOU)
    probAH = formObjectToProbabilities(match.oddsAH)
    
    return Probabilities(probW, probOU, probAH)

def setProbabilitiesClasi(match, prob):
    overall = {"home": match.clasOverall['home']['PCT'], "away": match.clasOverall['away']['PCT']}
    home = {"home": match.clasHome['home']['PCT']}
    away = {"away": match.clasAway['away']['PCT']}
    
    prob.setClasiProbabilities(overall, home, away)
    
    return prob

def countWins(array, names):
    probH2h = array
    for key in array.keys():
        countHome = 0
        countAway = 0
        size = len(array[key])
        for i in range(size):
            try:
                indexHome = array[key][i].index(names['home'])
            except ValueError:
                indexHome = -1
            try:
                indexAway = array[key][i].index(names['away'])
            except ValueError:
                indexAway = -1
            
            result = array[key][i][-2] > array[key][i][-1]
            if (indexHome == 0 and result) or (indexHome == 1 and not result):
                countHome = countHome + 1
            elif (indexAway == 0 and result) or (indexAway == 1 and not result):
                countAway = countAway + 1
        
        if key == "home":
            probH2h['home'] = countHome / size
        elif key == "away":
            probH2h['away'] = countAway / size
        elif key == "mutual":
            probH2h['mutual'] = {'home': countHome / size, 'away': countAway / size}
        
    return probH2h

def setProbabilitiesH2h(match, prob):
    overall = countWins(match.h2hOverall, match.names)
    home = countWins(match.h2hHome, match.names)
    away = countWins(match.h2hAway, match.names)
    
    prob.setH2hProbabilities(overall, home, away)
    
    return prob

def getProbabilities(match):
    probabilities = setProbabilitiesOdds(match)
    probabilities = setProbabilitiesClasi(match, probabilities)
    probabilities = setProbabilitiesH2h(match, probabilities)
    
    return probabilities

def analyzeWin(prob):
    winnerH = [prob.probWin['home'], prob.probClasiOverall['home'], 
               prob.probClasiHome['home'], prob.probH2hOverall['home'],
               prob.probH2hOverall['mutual']['home'], prob.probH2hHome['home'], 
               prob.probH2hHome['mutual']['home']]
    winnerA = [prob.probWin['away'], prob.probClasiOverall['away'], 
               prob.probClasiAway['away'], prob.probH2hOverall['away'],
               prob.probH2hOverall['mutual']['away'], prob.probH2hAway['away'], 
               prob.probH2hHome['mutual']['away']]
    
    resultH = [statistics.mean(winnerH[1:]), winnerH[0]]
    resultA = [statistics.mean(winnerA[1:]), winnerA[0]]
    
    if resultH[0] > resultA[0]:
        result = ['home', resultH]
    else:
        result = ['away', resultA]
    
    return result

def getLeagues(sport):
    url = "https://d.mismarcadores.com/x/feed/f_{}_0_2_es_1".format(sport[1])
    website_url = requests.get(url, headers={'X-Fsign': 'SW9D1eZo'}).text
    soup = BeautifulSoup(website_url,"html.parser")
    leagues = []
    
    result = [m.start() for m in re.finditer(sport[0], soup.string)]
    
    for startIndex in result:
        init = startIndex+len(sport[0])+1
        path = soup.string[init:].split("¬")[0]
        leagues.append(path)
    
    return leagues

def getSports():
    return [["futbol", 1], ["baloncesto", 3], ["tenis", 2], ["beisbol",6]]

    
#def main():
threshold = 0.6
print("Threshold: ", threshold)

sportsIds = getSports()
for sport in sportsIds:
    print(sport)
    leaguesIds = getLeagues(sport)
    for league in leaguesIds:
        print(league)
        matchesIds = getIdMatchs(sport[0], league)
        for match in matchesIds:
            print(match)
            match = getData(match)
        #    probabilities = getProbabilities(match)
        #    winResult = analyzeWin(probabilities)
        #    
        #    
        #    if winResult[1][0] > threshold:
        #        print(match.names['home'], " - " , match.names['away'], " -> ", winResult)
        #    
