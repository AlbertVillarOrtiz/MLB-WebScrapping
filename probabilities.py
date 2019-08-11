# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 11:05:44 2019

@author: AlbertVillarOrtiz
"""

class Probabilities:
    
    def __init__(self, probW, probOU, probAH):
        self.probWin = probW
        self.probOU = probOU
        self.probAH = probAH
        self.probClasiOverall = {}
        self.probClasiHome = {}
        self.probClasiAway = {}
        self.probH2hOverall = {}
        self.probH2hHome = {}
        self.probH2hAway = {}
    
    def setClasiProbabilities(self, overall, home, away):
        self.probClasiOverall = overall
        self.probClasiHome = home
        self.probClasiAway = away
    
    def setH2hProbabilities(self, overall, home, away):
        self.probH2hOverall = overall
        self.probH2hHome = home
        self.probH2hAway = away