# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 11:05:44 2019

@author: AlbertVillarOrtiz
"""
from utilities import countWins, formObjectToProbabilities, countTotalsMean

class Probabilities:
    
    def __init__(self):
        self.win = {"home": 0, "away": 0}
        self.ou = {}
        self.ah = {}
        self.clasification = {}
        self.h2hOverall = {}
        self.h2hHome = {}
        self.h2hAway = {}
    
    def _setOddProbabilities(self, win, ou, ah):
        self.win = win
        self.ou = ou
        self.ah = ah
    
    def _setClasiProbabilities(self, clasification):
        self.clasification = clasification
    
    def _setH2hProbabilities(self, overall, home, away):
        self.h2hOverall = {"win": overall[0], "totals_mean": overall[1]}
        self.h2hHome = {"win": home[0], "totals_mean": home[1]}
        self.h2hAway = {"win": away[0], "totals_mean": away[1]}
    
    def calculateProbabilitiesH2h(self, match):
        if len(match.h2hOverall) != 0:
            overall_wins = countWins(match.h2hOverall, match.names)
            home_wins = countWins(match.h2hHome, match.names)
            away_wins = countWins(match.h2hAway, match.names)
            
#            overall_total = countTotalsMean(match.h2hOverall)
#            home_total = countTotalsMean(match.h2hHome)
#            away_total = countTotalsMean(match.h2hAway)
            overall_total = 0
            home_total = 0
            away_total = 0
            
            overall = [overall_wins, overall_total]
            home = [home_wins, home_total]
            away = [away_wins, away_total]
            
            self._setH2hProbabilities(overall, home, away)
    
    def calculateProbabilitiesClasi(self, match):
        if len(match.clasOverall) != 0:
            clasification = {
                    "win": {
                            "overall": {
                                "home": match.clasOverall['home']['PCT'], 
                                "away": match.clasOverall['away']['PCT']
                            },
                            "home": {
                                "home": match.clasHome['home']['PCT']
                            },
                            "away": {
                                "away": match.clasAway['away']['PCT']
                            }
                    },
                    "totals_mean": {
                            "overall": {
                                "home": (match.clasOverall['home']['PF'] + match.clasOverall['home']['PA']) / match.clasOverall['home']['GP'], 
                                "away": (match.clasOverall['away']['PF'] + match.clasOverall['away']['PA']) / match.clasOverall['away']['GP']
                            },
                            "home": {
                                "home": (match.clasHome['home']['PF'] + match.clasHome['home']['PA']) / match.clasHome['home']['GP']
                            },
                            "away": {
                                "away": (match.clasAway['away']['PF'] + match.clasAway['away']['PA']) / match.clasAway['away']['GP']
                            }
                    },
            }
            
            self._setClasiProbabilities(clasification)
    
    def calculateProbabilitiesOdd(self, match):
        if len(match.oddsW) != 0:
            win = formObjectToProbabilities(match.oddsW)
            ou = formObjectToProbabilities(match.oddsOU)
            ah = formObjectToProbabilities(match.oddsAH)
            
            self._setOddProbabilities(win, ou, ah)
    
    def isAllCorrect(self):
        clasiO = len(self.clasification) != 0
        h2hO = len(self.h2hOverall) != 0
        
        return clasiO and h2hO