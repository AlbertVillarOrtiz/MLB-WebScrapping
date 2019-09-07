# -*- coding: utf-8 -*-
"""
Created on Sun Aug 11 17:33:53 2019

@author: alber
"""
import statistics
import pandas as pd
from telegram import Telegram
from stats import Stats

class Analyzer():
    
    def __init__(self):
        self.win = []
        self.totalsMean = []
        self.telegram = Telegram()
        self.stats = Stats()
        self.threshold_perc = 70
        self.threshold_odd = 1.6
        self.diff_prob = 0.05
        self.diff_odd = 0.9
    
    def isTimeToBetting(self, threshold, match):
        threshold_perc_okey = self.win[1][0] >= self.threshold_perc
        odd1 = 1/self.win[1][1] if self.win[1][1] != 0 else 0
        odd2 = 1/self.win[1][3] if self.win[1][3] != 0 else 0
        threshold_odd_okey = odd1 >= self.threshold_odd
        diff_prob_okey = (self.win[1][0] - self.win[1][2]) >= self.diff_prob
        diff_odd_okey = (odd1 - odd2) >= self.diff_odd
        
        print(match.names['home'], " - " , match.names['away'])
        print(self.win[1][0],"/",self.threshold_perc, threshold_perc_okey)
        print(odd1,"/",self.threshold_odd, threshold_odd_okey)
        print((self.win[1][0] - self.win[1][2]),"/",self.diff_prob, diff_prob_okey)
        print((odd1 - odd2),"/",self.diff_odd, diff_odd_okey)
        
        if threshold_perc_okey and threshold_odd_okey and diff_prob_okey and diff_odd_okey:
            #print(match.names['home'], " - " , match.names['away'], " -> ", self.win)
            return self.win

    def isTimeToBettingHistorical(self, sport, league, year, id_match, results):
        headers = ['Sport', 'League', 'Year', "Prediction", "Probability", 
                   "Odd", "Opponent_probability", "Opponent_odd", "Id_Match", "Result"]
        name = "_".join((sport, "mlb", year))
        data = pd.read_csv(name + ".csv") 
        df = pd.DataFrame(data, columns = headers)
        
        cond_home = self.win[0] == "home" and results["home"] > results["away"]
        cond_away = self.win[0] == "away" and results["home"] < results["away"]
            
        result = 1 if cond_home or cond_away else 0
        odd1 = 1/self.win[1][1] if self.win[1][1] != 0 else 0
        odd2 = 1/self.win[1][3] if self.win[1][3] != 0 else 0
        
        df = df.append({
            "Sport": sport, 
            "League": league, 
            "Year": year,
            "Prediction": self.win[0],
            "Probability": self.win[1][0],
            "Odd": odd1,
            "Opponent_probability": self.win[1][2],
            "Opponent_odd": odd2,
            "Id_Match": id_match, 
            "Result": result
            }, ignore_index=True)
        df.to_csv (name + '.csv', header=True)
        print("Match stored")
        
        
    def winner(self, prob):
        winnerH = [prob.clasification["win"]['overall']['home'], prob.clasification["win"]['home']['home'], 
                   prob.h2hOverall["win"]['home'], prob.h2hOverall["win"]['mutual']['home'], 
                   prob.h2hHome["win"]['home'], prob.h2hHome["win"]['mutual']['home']]
        winnerA = [prob.clasification["win"]['overall']['away'], prob.clasification["win"]['away']['away'], 
                   prob.h2hOverall["win"]['away'],prob.h2hOverall["win"]['mutual']['away'], 
                   prob.h2hAway["win"]['away'], prob.h2hHome["win"]['mutual']['away']]
        
        resultH = [statistics.mean(winnerH), prob.win['home'], statistics.mean(winnerA), prob.win['away']]
        resultA = [statistics.mean(winnerA), prob.win['away'], statistics.mean(winnerH), prob.win['home']]
        
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
                    