# -*- coding: utf-8 -*-
"""
Created on Sun Aug 11 17:33:53 2019

@author: alber
"""
import statistics

class Analyzer():
    
    def __init__(self):
        self.winner = []
    
    def isTimeToBetting(self, threshold):
        winner = self.winner[1][0] > threshold
        
        return winner
    
    def winner(self, prob):
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
            self.winner = ['home', resultH]
        else:
            self.winner = ['away', resultA]