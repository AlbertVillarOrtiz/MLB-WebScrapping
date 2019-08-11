# -*- coding: utf-8 -*-
"""
Created on Sun Aug 11 17:33:53 2019

@author: alber
"""
import statistics

class Analyzer():
    
    def __init__(self):
        self.win = []
    
    def isTimeToBetting(self, threshold):
        winner = self.winner[1][0] > threshold
        
        return winner
    
    def winner(self, prob):
        winnerH = [prob.clasiOverall['home'], prob.clasiHome['home'], 
                   prob.h2hOverall['home'], prob.h2hOverall['mutual']['home'], 
                   prob.h2hHome['home'], prob.h2hHome['mutual']['home']]
        winnerA = [prob.clasiOverall['away'], prob.clasiAway['away'], 
                   prob.h2hOverall['away'],prob.h2hOverall['mutual']['away'], 
                   prob.h2hAway['away'], prob.h2hHome['mutual']['away']]
        
        resultH = [statistics.mean(winnerH), prob.win['home']]
        resultA = [statistics.mean(winnerA), prob.win['away']]
        
        if resultH[0] > resultA[0]:
            self.win = ['home', resultH]
        else:
            self.win = ['away', resultA]