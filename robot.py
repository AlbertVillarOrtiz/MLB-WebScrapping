# -*- coding: utf-8 -*-
"""
Created on Sun Jul 21 18:41:55 2019

@author: AlbertVillarOrtiz
"""
from match import Match
from probabilities import Probabilities
from analyzer import Analyzer
from scrapper import Scrapper
from historical import Historical

class Robot():
    
    def __init__(self):
        self.threshold = 0.6
        self.max_games = 20
        self.count_games = 0
    
    def _updateCountGames(self):
        self.count_games = self.count_games + 1
    
    def _initCountGames(self):
        self.count_games = 0
        
    def getMatch(self, scrapper, id_match, league):
        match = Match()
        id_teams = scrapper.getIdTeams(id_match)
        match.setInfoMatch(id_teams, id_match)
        
        match = scrapper.getH2h(match)
        match = scrapper.getClasification(match, league)
        match = scrapper.getOdds(match)
        
        return match

    def getProbabilities(self, match):
        probabilities = Probabilities()
        probabilities.calculateProbabilitiesClasi(match)
        probabilities.calculateProbabilitiesH2h(match)
        probabilities.calculateProbabilitiesOdd(match)
        
        return probabilities
    
    def getAnalysis(self, probabilities):
        analyzer = Analyzer()
        analyzer.winner(probabilities)
#        analyzer.totalsMean(probabilities)
        
        return analyzer
    
    def run(self):
        scrapper = Scrapper()
        sports = scrapper.getSport()
        for sport in sports:
            
            leagues = scrapper.getLeague(sport)
            for league in leagues:
                
                id_matchs = scrapper.getIdsMatch(sport["name"], league["name"])
                self._initCountGames()
                while self.count_games < self.max_games and self.count_games < len(id_matchs):
                    
                    print(sport["name"], league['name'], self.count_games)
                    match = self.getMatch(scrapper, id_matchs[self.count_games], league)
                    probabilities = self.getProbabilities(match)
                    if probabilities.isAllCorrect():
                        
                        analyzer = self.getAnalysis(probabilities)
                        analyzer.isTimeToBetting(self.threshold, match)
                    self._updateCountGames()
    
    def runHistorical(self):
        historical = Historical()
        scrapper = Scrapper()
        index_sports = historical.historical
        for sport in index_sports.keys():                
            id_matchs_by_year = index_sports[sport]["mlb"]["matchs"]
            league =  {'name': 'usa/mlb/', 'id1': 'Uanezsbs', 'id2': 'GMHpTqQb'}
            
            for year in ["2017"]:
                i = 0
                iterator = list(id_matchs_by_year[year].keys())
                for id_match in iterator:
                    
                    print(sport, "mlb", year, id_match, i, len(id_matchs_by_year[year].keys()))
                    match = self.getMatch(scrapper, id_match, league)
                    probabilities = self.getProbabilities(match)
                    if probabilities.isAllCorrect():
                        
                        analyzer = self.getAnalysis(probabilities)
                        analyzer.isTimeToBettingHistorical(sport, league["name"], year, id_match, id_matchs_by_year[year][id_match])
                    
                    i = i + 1


