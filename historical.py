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
    
    def writeHistorical(self):
        json.dump(self._historical, open('historical.json', 'w'))
    
    def _writeIndexSports(self):
        json.dump(self._index_sports, open('index_sports.json', 'w'))
        
    def defineHistorical(self, sport, league, league_historical):
        self._historical[sport][league] = league_historical
    
    def _defineIndexSports(self, sport, leagues):
        self._index_sports[sport] = leagues
    
# -----------------------------------------------------------------------------
    def runIndexSports(self):
        scrapper = Scrapper()
        sports = scrapper.getSport()
        for sport in sports:
            leagues = scrapper.getAllLeaguesByCountry(sport)
            self._defineIndexSports(sport["name"], leagues)
        
        self._writeIndexSports()
        
    def runHistorical(self):
        index_sports = self._readIndexSports()
        scrapper = Scrapper()
        
        for sport in index_sports.keys():
            for league in index_sports[sport].keys():
                index_sports[sport][league]["matchs"] = scrapper.getHistoric(index_sports[sport][league])
                historic = Historical()
                historic.defineLeague(sport["name"], league, index_sports[sport][league])
            
            historic.writeHistorical()
                
                