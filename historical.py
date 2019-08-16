# -*- coding: utf-8 -*-
"""
Created on Wed Aug 14 23:21:39 2019

@author: AlbertVillarOrtiz
"""
import json
from scrapper import Scrapper

class Historical():
    
    def __init__(self):
        self._historical = self._readHistorical()
        self._index_sports = self._readIndexSports()
    
    def _readHistorical(self):
        data = json.load(open('historical.json'))
            
        return data
    
    def _readIndexSports(self):
        data = json.load(open('index_sports.json'))
            
        return data
    
    def _writeHistorical(self):
        json.dump(self._historical, open('historical.json', 'w'), sort_keys=True, indent=4)
    
    def _writeIndexSports(self):
        json.dump(self._index_sports, open('index_sports.json', 'w'), sort_keys=True, indent=4)
        
    def _defineHistorical(self, league_historical):
        self._historical = league_historical
    
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
        
    def runHistorical(self):
        index_sports = self._readIndexSports()
        scrapper = Scrapper()
        
        for sport in index_sports.keys():
            league = "mlb"
#            for league in index_sports[sport].keys():
            index_sports[sport][league]["matchs"] = scrapper.getHistorical(index_sports[sport][league])
            self._defineHistorical(index_sports)
            
            self._writeHistorical()