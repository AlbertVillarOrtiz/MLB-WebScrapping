# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 11:05:44 2019

@author: AlbertVillarOrtiz
"""
from utilities import countWins, formObjectToProbabilities

class Probabilities:
    
    def __init__(self):
        self.win = {"home": 0, "away": 0}
        self.ou = {}
        self.ah = {}
        self.clasiOverall = {}
        self.clasiHome = {}
        self.clasiAway = {}
        self.h2hOverall = {}
        self.h2hHome = {}
        self.h2hAway = {}
    
    def _setOddProbabilities(self, win, ou, ah):
        self.win = win
        self.ou = ou
        self.ah = ah
    
    def _setClasiProbabilities(self, overall, home, away):
        self.clasiOverall = overall
        self.clasiHome = home
        self.clasiAway = away
    
    def _setH2hProbabilities(self, overall, home, away):
        self.h2hOverall = overall
        self.h2hHome = home
        self.h2hAway = away
    
    def calculateProbabilitiesH2h(self, match):
        if len(match.h2hOverall) != 0:
            overall = countWins(match.h2hOverall, match.names)
            home = countWins(match.h2hHome, match.names)
            away = countWins(match.h2hAway, match.names)
            
            self._setH2hProbabilities(overall, home, away)
    
    def calculateProbabilitiesClasi(self, match):
        if len(match.clasOverall) != 0:
            overall = {"home": match.clasOverall['home']['PCT'], "away": match.clasOverall['away']['PCT']}
            home = {"home": match.clasHome['home']['PCT']}
            away = {"away": match.clasAway['away']['PCT']}
            
            self._setClasiProbabilities(overall, home, away)
    
    def calculateProbabilitiesOdd(self, match):
        if len(match.oddsW) != 0:
            win = formObjectToProbabilities(match.oddsW)
            ou = formObjectToProbabilities(match.oddsOU)
            ah = formObjectToProbabilities(match.oddsAH)
            
            self._setOddProbabilities(win, ou, ah)
    
    def isAllCorrect(self):
        clasiO = len(self.clasiOverall) != 0
        h2hO = len(self.h2hOverall) != 0
        
        return clasiO and h2hO