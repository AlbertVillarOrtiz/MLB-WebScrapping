# -*- coding: utf-8 -*-
"""
Created on Sat Aug 10 21:12:43 2019

@author: AlbertVillarOrtiz
"""
from bs4 import BeautifulSoup
import requests
import re
import utilities as util

class Scrapper():

    def __init__(self):
        self.__url_sport = "https://www.mismarcadores.com/"
        self.__url_country_leagues = "https://www.mismarcadores.com/{}"
        self.__url_league = "https://d.mismarcadores.com/x/feed/f_{}_0_2_es_1"
        self.__url_match = "https://www.mismarcadores.com/{}/{}partidos/"
        self.__url_team = "https://www.mismarcadores.com/partido/{}/#h2h;overall"
        self.__url_clasification = "https://d.mismarcadores.com/x/feed/ss_1_{}_{}_table_{}?e={}&hp1={}&hp2={}"
        self.__url_h2h = "https://d.mismarcadores.com/x/feed/d_hh_{}_es_1"
        self.__url_odd = "https://d.mismarcadores.com/x/feed/d_od_{}_es_1_eu"
        self.__url__historic = "https://www.mismarcadores.com/{}/{}/{}-{}/resultados/"
        self.__header = {"X-Fsign": "SW9D1eZo"}
        self.__situations = ['overall', 'home', 'away']
    
    def _soupSport(self):
        website_url = requests.get(self.__url_sport, headers=self.__header).text
        soup = BeautifulSoup(website_url,"html.parser")
        
        return soup
    
    def getSport(self):
        soup = self._soupSport()
        sports = []
        
        sports_a = soup.find_all("a",{"class":"menuMinority__item"})
        for sport in sports_a:
            sport_name = sport.get('href').replace("/", "")
            sport_id = sport.get('data-sport-id')
            sports.append({"name": sport_name, "id": sport_id})
        
        sports = [{"name": "beisbol", "id": 6}]
#sports = [{'name': 'badminton', 'id': '21'}, {'name': 'baloncesto', 'id': '3'}, 
#{'name': 'balonmano', 'id': '7'}, {'name': 'bandy', 'id': '10'}, 
#{'name': 'beisbol', 'id': '6'}, {'name': 'boxeo', 'id': '16'}, 
#{'name': 'carreras-de-caballos', 'id': '35'}, {'name': 'ciclismo', 'id': '34'}, 
#{'name': 'cricket', 'id': '13'}, {'name': 'dardos', 'id': '14'}, 
#{'name': 'deportes-de-invierno', 'id': '37'}, {'name': 'esports', 'id': '36'}, 
#{'name': 'futbol', 'id': '1'}, {'name': 'futbol-americano', 'id': '5'}, 
#{'name': 'futbol-australiano', 'id': '18'}, {'name': 'futbol-playa', 'id': '26'}, 
#{'name': 'futbol-sala', 'id': '11'}, {'name': 'golf', 'id': '23'}, 
#{'name': 'hockey', 'id': '4'}, {'name': 'hockey-hierba', 'id': '24'}, 
#{'name': 'kabaddi', 'id': '42'}, {'name': 'mma', 'id': '28'}, 
#{'name': 'motor', 'id': '31'}, {'name': 'netball', 'id': '29'}, 
#{'name': 'pesapallo', 'id': '30'}, {'name': 'rugby', 'id': '8'}, 
#{'name': 'rugby-league', 'id': '19'}, {'name': 'snooker', 'id': '15'}, 
#{'name': 'tenis', 'id': '2'}, {'name': 'tenis-de-mesa', 'id': '25'}, 
#{'name': 'unihockey', 'id': '9'}, {'name': 'voleibol', 'id': '12'}, 
#{'name': 'voley-playa', 'id': '17'}, {'name': 'waterpolo', 'id': '22'}]
        
        return sports
    
    def _soupLeague(self, id_sport):
        url = self.__url_league.format(id_sport)
        website_url = requests.get(url, headers=self.__header).text
        soup = BeautifulSoup(website_url,"html.parser")
        
        return soup
    
    def getLeague(self, sport):
        soup = self._soupLeague(sport["id"])
        leagues = []
        leagues_index = [s.start() for s in re.finditer(sport["name"], soup.string)]
        leagues_index_id1 = [s.start() for s in re.finditer('ZE÷', soup.string)]
        leagues_index_id2 = [s.start() for s in re.finditer('ZC÷', soup.string)]
        
        for i in range(len(leagues_index)):
            init_path = leagues_index[i] + len(sport["name"]) + 1
            init_id1 = leagues_index_id1[i] + 3
            init_id2 = leagues_index_id2[i] + 3
            
            path = soup.string[init_path:].split("¬")[0]
            id1 = soup.string[init_id1:].split("¬")[0]
            id2 = soup.string[init_id2:].split("¬")[0]
            
            leagues.append({"name": path, "id1": id1, "id2": id2})
        
        return leagues
    
    def _soupIdsMatch(self, sport, league):
        url = self.__url_match.format(sport, league)
        website_url = requests.get(url).text
        soup = BeautifulSoup(website_url,"html.parser")
        
        return soup
    
    def getIdsMatch(self, sport, league):
        try: 
            soup = self._soupIdsMatch(sport, league)
            
            matchsTable = soup.find("div",{"id":"tournament-page-data-fixtures"}).string
            indexes = [m.start() for m in re.finditer('AA÷', matchsTable)]
            ids = []
            for element in indexes:
                test = matchsTable[element:element+12]
                index = test.index("¬")
                ids.append(matchsTable[element+3:element+index])
        except:
            ids = []
        finally:
            return ids
    
    def _soupIdsTeam(self, id_match):
        url = self.__url_team.format(id_match)
        website_url = requests.get(url, headers=self.__header).text
        soup = BeautifulSoup(website_url,"html.parser").text
        
        return soup
    
    def getIdTeams(self, id_match):
        soup = self._soupIdsTeam(id_match)
    
        constant = "var participantEncodedIds = "
        indexes = [m.start() for m in re.finditer(constant, soup)]
        init = indexes[0] + len(constant)
        finish = init + 35
    
        test = soup[init:finish]
        index = test.index("];")
        teams = soup[init+2:init+index-1]
        teams = teams.replace('\'','')
        teams = teams.split(',') 
        
        return teams
    
    def _soupClasification(self, situation, id_match, id_home, id_away, league):
        url = self.__url_clasification.format(league["id1"], league["id2"], situation, id_match, id_home, id_away)
        website_url = requests.get(url, headers=self.__header).text
        soup = BeautifulSoup(website_url,"html.parser")
        
        return soup
    
    def getClasification(self, match, league):
        clasification = []
        
        try:
            for situation in self.__situations:
                
                soup = self._soupClasification(situation, match.id, match.id_teams['home'], match.id_teams['away'], league)
                trClasi = soup.find_all("tr", {"class": "highlight"})
                for i in range(2):
                    
                    clasi = trClasi[i].get_text(separator="/").split("/")[1:8]
                    length = len(clasification)
                    if clasi[0] == match.names['home'] and i != 0:
                        del clasi[0]
                        clasification.insert(length-1, util.normalizeData(clasi))
                    else:
                        del clasi[0]
                        clasification.append(util.normalizeData(clasi))  
            
            match.setClasification(clasification[0:2], clasification[2:4], clasification[4:6])
        except:
            print("NO CLASIFICATION")
        finally:
            return match
    
    def _soupH2h(self, id_match):
        url = self.__url_h2h.format(id_match)
        website_url = requests.get(url, headers=self.__header).text
        soup = BeautifulSoup(website_url,"html.parser")
        
        return soup
    
    def getH2h(self, match):
        soup = self._soupH2h(match.id)
        h2h = []
        names = []
        
        try:
            tableHome = soup.find_all("table", {"class": "h2h_home"})
            for table in tableHome:
                mHome = []
                matchsHome = table.find_all("tr", {"class": "highlight"})
                for i in range(util.getSize(matchsHome, 10)):
                    h2hValues = matchsHome[i].get_text(separator="/").split("/")[-3:]
                    h2hValues.extend(util.normalizeH2hData([h2hValues[-1]]))
                    del h2hValues[2]
                    mHome.append(h2hValues)
                h2h.append(mHome)
                
            names.append(h2h[-1][-1][0])
            tableAway = soup.find_all("table", {"class": "h2h_away"})
            for table in tableAway:
                mAway = []
                matchsAway = table.find_all("tr", {"class": "highlight"})
                for i in range(util.getSize(matchsAway, 10)):
                    h2hValues = matchsAway[i].get_text(separator="/").split("/")[-3:]
                    h2hValues.extend(util.normalizeH2hData([h2hValues[-1]]))
                    del h2hValues[2]
                    mAway.append(h2hValues)
                h2h.append(mAway)
                
            names.append(h2h[-1][-1][1])
            tableMutual = soup.find_all("table", {"class": "h2h_mutual"})
            for table in tableMutual:
                mMutual = []
                matchsMutual = table.find_all("tr", {"class": "highlight"})
                for i in range(util.getSize(matchsMutual, 10)):
                    h2hValues = matchsMutual[i].get_text(separator="/").split("/")[-3:]
                    h2hValues.extend(util.normalizeH2hData([h2hValues[-1]]))
                    del h2hValues[2]
                    mMutual.append(h2hValues)
                h2h.append(mMutual)
            
        
            match.setH2h(h2h)
            match.setNamesMatch(names)
        except:
            print("NO H2H")
        finally:
            return match

    def _soupOdd(self, id_match):
        url = self.__url_odd.format(id_match)
        website_url = requests.get(url, headers=self.__header).text
        soup = BeautifulSoup(website_url,"html.parser")
        
        return soup
    
    def getOdds(self, match):
        soup = self._soupOdd(match.id)
        oddsW = []
        oddsOU = {}
        oddsAH = {}
        
        try:
            tableMoneyLine = soup.find("table", {"id": "odds_ml"})
            trML = tableMoneyLine.find_all("tr", {"class": "odd"})
        
            odds = trML[0].get_text(separator="/").split("/")
            if '\xa0' in odds: odds.remove('\xa0')
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
        except:
            print("NO ODDS")
        finally:
            return match
    
    def getAllLeaguesByCountry(self, sport):
        url = self.__url_country_leagues.format(sport)
        website_url = requests.get(url, headers=self.__header).text
        soup = BeautifulSoup(website_url,"html.parser")

        leagues = {}
        countries = soup.find("ul",{"class":"tournament-menu"})
        countries = countries.find_all("li")
        
        for li in countries:
            
            a = li.find("a")
            if a != None:
                
                href = a.get("href")
                if href != "#":
                
                    split = href.split("/")
                    del split[0] 
                    del split[len(split)-1]
                    if len(split) == 2:
                        leagues[split[1]] = []
                    elif len(split) == 3:
                        leagues[split[1]].append(split[2])
        
        return leagues
    
    def getHistoric(self):
        url = self.__url__historic.format("beisbol", "usa", "mlb", "2018")
        website_url = requests.get(url, headers=self.__header).text
        soup = BeautifulSoup(website_url,"html.parser")
        
        matchsTable = soup.find("div",{"class":"leagues--static"}).string
        indexes = [m.start() for m in re.finditer('AA÷', matchsTable)]
        ids = []
        for element in indexes:
            test = matchsTable[element:element+12]
            index = test.index("¬")
            ids.append(matchsTable[element+3:element+index])
        
        print(ids)
        
scrapper = Scrapper()
scrapper.getHistoric()
            
            
        
        