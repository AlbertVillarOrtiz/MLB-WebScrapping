# -*- coding: utf-8 -*-
"""
Created on Sun Aug 11 17:33:53 2019

@author: alber
"""
import statistics
from telegram import Telegram

class Analyzer():
    
    def __init__(self):
        self.win = []
        self.totalsMean = []
        self.telegram = Telegram()
    
    def isTimeToBetting(self, threshold, match):
        winner = self.winner[1][0] > threshold
        totalsMean = len(self.totalsMean) != 0
        
        if winner:
            print(match.names['home'], " - " , match.names['away'], " -> ", self.win)
#            self.telegram.sendMessage(sport, msg)
            
        if totalsMean:
            print(match.names['home'], " - " , match.names['away'], " -> ", self.totalsMean)
#            self.telegram.sendMessage(sport, msg)
    
    def winner(self, prob):
        winnerH = [prob.clasiOverall["win"]['home'], prob.clasiHome["win"]['home'], 
                   prob.h2hOverall["win"]['home'], prob.h2hOverall["win"]['mutual']['home'], 
                   prob.h2hHome["win"]['home'], prob.h2hHome["win"]['mutual']['home']]
        winnerA = [prob.clasiOverall["win"]['away'], prob.clasiAway["win"]['away'], 
                   prob.h2hOverall["win"]['away'],prob.h2hOverall["win"]['mutual']['away'], 
                   prob.h2hAway["win"]['away'], prob.h2hHome["win"]['mutual']['away']]
        
        resultH = [statistics.mean(winnerH), prob.win['home']]
        resultA = [statistics.mean(winnerA), prob.win['away']]
        
        if resultH[0] > resultA[0]:
            self.win = ['home', resultH]
        else:
            self.win = ['away', resultA]
    
    def totalsMean(self, prob):
        keys = prob.ou.keys()
        
        total = [prob.clasiOverall["totals_mean"]['home'], prob.clasiHome["totals_mean"]['home'], 
                 prob.h2hOverall["totals_mean"]['home'], prob.h2hOverall["totals_mean"]['mutual']['home'], 
                 prob.h2hHome["totals_mean"]['home'], prob.h2hHome["totals_mean"]['mutual']['home'], 
                 prob.clasiOverall["totals_mean"]['away'], prob.clasiAway["totals_mean"]['away'], 
                 prob.h2hOverall["totals_mean"]['away'],prob.h2hOverall["totals_mean"]['mutual']['away'], 
                 prob.h2hAway["totals_mean"]['away'], prob.h2hHome["totals_mean"]['mutual']['away']]
        
        totalsMean = statistics.mean(total)
        
        if float(keys[0]) < totalsMean:
            self.totalsMean = [keys[0], "OVER", totalsMean]
        elif float(keys[len(keys)-1]) > totalsMean:
            self.totalsMean = [keys[len(keys)-1], "UNDER", totalsMean]
                
        return self.totalsMean
                    