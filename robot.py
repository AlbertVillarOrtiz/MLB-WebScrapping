# -*- coding: utf-8 -*-
"""
Created on Sun Jul 21 18:41:55 2019

@author: AlbertVillarOrtiz
"""
from match import Match
from probabilities import Probabilities
from analyzer import Analyzer
from scrapper import Scrapper

class Robot():
    
    def __init__(self):
        self.threshold = 0.6
        self.max_failed = 10
        self.max_games = 25
        self.count_failed = 0
        self.count_games = 0
    
    def updateMatchFailed(self):
        self.count_failed = self.count_failed + 1
    
    def updateGameByLeague(self):
        self.count_games = self.count_games + 1
    
    def initCounters(self):
        self.count_failed = 0
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
        
        return analyzer
    
    def run(self):
        scrapper = Scrapper()
        sports = scrapper.getSport()
        for sport in sports:
            
            leagues = scrapper.getLeague(sport)
            for league in leagues:
                
                id_matchs = scrapper.getIdsMatch(sport["name"], league["name"])

                self.initCounters()
                while self.count_failed < self.max_failed and self.count_games < self.max_games and self.count_games < len(id_matchs):
                    print(sport["name"], league['name'], self.count_games)
                    match = self.getMatch(scrapper, id_matchs[self.count_games], league)
                    probabilities = self.getProbabilities(match)
                    if probabilities.isAllCorrect():
                        
                        analyzer = self.getAnalysis(probabilities)
#                        if analyzer.isTimeToBetting(self.threshold):
                        print(match.names['home'], " - " , match.names['away'], " -> ", analyzer.win)
                    else:
                        self.updateMatchFailed()
                    
                    self.updateGameByLeague()
            


