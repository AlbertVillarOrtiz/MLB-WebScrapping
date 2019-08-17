# -*- coding: utf-8 -*-
"""
Created on Wed Aug 14 23:21:39 2019

@author: AlbertVillarOrtiz
"""
import json
from scrapper import Scrapper

class Historical():
    
    def __init__(self):
        self.historical = self.readHistorical()
        self._index_sports = self._readIndexSports()
    
    def readHistorical(self):
        data = json.load(open('historical.json'))
            
        return data
    
    def _readIndexSports(self):
        data = json.load(open('index_sports.json'))
            
        return data
    
    def _writeHistorical(self):
        json.dump(self.historical, open('historical.json', 'w'), sort_keys=True, indent=4)
    
    def _writeIndexSports(self):
        json.dump(self._index_sports, open('index_sports.json', 'w'), sort_keys=True, indent=4)
        
    def _defineHistorical(self, league_historical):
        self.historical = league_historical
    
    def _defineIndexSports(self, leagues):
        self._index_sports = leagues
    
# -----------------------------------------------------------------------------
    def runIndexSports(self):
        scrapper = Scrapper()
        sports = scrapper.getSport()
        for sport in sports:
            leagues_by_sport = scrapper.getAllLeaguesByCountry(sport)
            self._defineIndexSports(leagues_by_sport)
        
        self._writeIndexSports()
        
    def runHistorical(self, year):
        scrapper = Scrapper()
        
        for sport in self.historical.keys():
            league = "mlb"
#            for league in index_sports[sport].keys():
            self.historical[sport][league]["matchs"][year] = scrapper.getHistorical(self.historical[sport][league], year)
            self._defineHistorical(self.historical)
            
            self._writeHistorical()
            