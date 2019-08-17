# -*- coding: utf-8 -*-
"""
Created on Sun Aug 11 17:33:53 2019

@author: alber
"""
import statistics
from telegram import Telegram
from stats import Stats

class Analyzer():
    
    def __init__(self):
        self.win = []
        self.totalsMean = []
        self.telegram = Telegram()
        self.stats = Stats()
    
    def isTimeToBetting(self, threshold, match):
        winner = self.winner[1][0] > threshold
#        totalsMean = len(self.totalsMean) != 0
        
        if winner:
            print(match.names['home'], " - " , match.names['away'], " -> ", self.win)
            return self.win
#            self.telegram.sendMessage(sport, msg)
#        if totalsMean:
#            print(match.names['home'], " - " , match.names['away'], " -> ", self.totalsMean)
#            self.telegram.sendMessage(sport, msg)
    
    def isTimeToBettingHistorical(self, threshold, sport, league, year, results):
        if self.winner[1][0] > threshold:
            print("IS TIME TO BETTING")
            cond_home = self.winner[0] == "home" and results["home"] > results["away"]
            cond_away = self.winner[0] == "away" and results["home"] < results["away"]
            
            if cond_home or cond_away:
                print("MONEY IS IN THE BANK")
                self.stats.byMatch(threshold, sport, league, year, self.winner[0], self.winner[1][0], 1)
            else :
                print("MONEY IS RUNNING OUT")
                self.stats.byMatch(threshold, sport, league, year, self.winner[0], self.winner[1][0], 0)
        else:
            print("NO BET")
        
    def winner(self, prob):
        winnerH = [prob.clasification["win"]['home'], prob.clasification["win"]['home'], 
                   prob.h2hOverall["win"]['home'], prob.h2hOverall["win"]['mutual']['home'], 
                   prob.h2hHome["win"]['home'], prob.h2hHome["win"]['mutual']['home']]
        winnerA = [prob.clasification["win"]['away'], prob.clasification["win"]['away'], 
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
        
        total = [prob.clasification["totals_mean"]['home'], prob.clasification["totals_mean"]['home'], 
                 prob.h2hOverall["totals_mean"]['home'], prob.h2hOverall["totals_mean"]['mutual']['home'], 
                 prob.h2hHome["totals_mean"]['home'], prob.h2hHome["totals_mean"]['mutual']['home'], 
                 prob.clasification["totals_mean"]['away'], prob.clasification["totals_mean"]['away'], 
                 prob.h2hOverall["totals_mean"]['away'],prob.h2hOverall["totals_mean"]['mutual']['away'], 
                 prob.h2hAway["totals_mean"]['away'], prob.h2hHome["totals_mean"]['mutual']['away']]
        
        totalsMean = statistics.mean(total)
        
        if float(keys[0]) < totalsMean:
            self.totalsMean = [keys[0], "OVER", totalsMean]
        elif float(keys[len(keys)-1]) > totalsMean:
            self.totalsMean = [keys[len(keys)-1], "UNDER", totalsMean]
                
        return self.totalsMean
                    