# -*- coding: utf-8 -*-
"""
Created on Sun Aug 18 14:54:21 2019

@author: alber
"""
import pandas as pd
import numpy as np
import statistics

def visualizeThreshold(df, inversion, threshold, difference_prob = 0, difference_odd = 0, threshold_odd = 0, threshold_max = 100):
    beneficio = 0
    nBets = 0
    nGreen = 0
    downhill = 0
    max_downhill = 0
    streak = 0
    max_streak = 0
    mean_odd = []
    if threshold < threshold_max: 
        matchs_prob = df[(df["Probability"] > threshold/100) & (df["Probability"] < threshold_max/100)]
        
        for index, row in matchs_prob.iterrows():
            cond_diff_prob = (row["Probability"] - row["Opponent_probability"])*100 > difference_prob
            cond_diff_odd = abs(row["Odd"] - row["Opponent_odd"]) >= difference_odd
            cond_threshold_odd = row["Odd"] > threshold_odd
            if row["Odd"] != 0:
                if cond_diff_prob and cond_diff_odd and cond_threshold_odd:
                    value = inversion*row["Odd"] - inversion if row["Result"] == 1 else - inversion
                    beneficio = beneficio + value
                    nBets = nBets + 1
                    mean_odd.append(row["Odd"])
                    if value > 0:
                        nGreen = nGreen + 1
                        streak = streak + 1
                        if downhill > max_downhill:
                            max_downhill = downhill
                            downhill = 0
                    else:
                        downhill = downhill + 1
                        if streak > max_streak:
                            max_streak = streak
                            streak = 0
                            
        perc = nGreen/nBets if nBets != 0 else 0
        
        result = {
            "num_bets": nBets,
            "perc": perc*100,
            "money": beneficio,
            "max_loss": -max_downhill*100,
            "max_win": max_streak*100,
            "mean_odd": 0,
            "money_max_loss": 0
        }
    
        if len(mean_odd) > 0:
            result["mean_odd"] = statistics.mean(mean_odd)
        
        if max_downhill*100 != 0:
            result["money_max_loss"] = beneficio/abs(max_downhill)*100

        return result

def visualizeTotal(df, inversion, difference_prob = 0, difference_odd = 0, threshold_odd = 0):
    nBets = 0
    nGreen = 0
    downhill = 0
    max_downhill = 0
    streak = 0
    max_streak = 0
    beneficio = 0
    mean_odd = []
    for index, row in df.iterrows():
        cond_diff_prob = (row["Probability"] - row["Opponent_probability"])*100 > difference_prob
        cond_diff_odd = abs(row["Odd"] - row["Opponent_odd"]) >= difference_odd
        cond_threshold_odd = row["Odd"] > threshold_odd
        if row["Odd"] != 0:
            if cond_diff_prob and cond_diff_odd and cond_threshold_odd:
                value = inversion*row["Odd"] - inversion if row["Result"] == 1 else - inversion
                beneficio = beneficio + value
                nBets = nBets + 1
                mean_odd.append(row["Odd"])
                if value > 0:
                    nGreen = nGreen + 1
                    streak = streak + 1
                    if downhill > max_downhill:
                        max_downhill = downhill
                        downhill = 0
                else:
                    downhill = downhill + 1
                    if streak > max_streak:
                        max_streak = streak
                        streak = 0
                    
    
    perc = nGreen/nBets if nBets != 0 else 0
    print("Pronosticos realizados: ", nBets)
    print("Pronosticos acertados: ", nGreen)
    print("Porcentaje de acierto: ", perc*100)
    if len(mean_odd) > 0:
        print("Cuota media: ", statistics.mean(mean_odd))
    print("Beneficio con inversion de " + str(inversion) + ": ", beneficio, " euros")
    print("Máximas pérdidas seguidas: ", -max_downhill*100, "euros (", max_downhill, "pronosticos )")
    print("Máximas ganancias seguidas: ", max_streak*100, "euros (", max_streak, "pronosticos )\n")

def saveDataMlb():
    data_total = []
    
    for year in ["2014", "2015", "2016", "2017", "2018"]:
        name = "_".join(("beisbol", "mlb", year))
        data_year = pd.read_csv(name + ".csv", index_col=None, header= 0)
        data_total.append(data_year)
        
    data_frame = pd.concat(data_total, axis=0, ignore_index=True)
    
    data_frame.to_csv ('visualization_data_mlb.csv', header=True)
    print("Match stored")
    
    return data_frame

def readDataMlb(name):
    data = pd.read_csv(name)
    data_frame = pd.DataFrame(data)
    
    return data_frame
    
def visualizeHistorical():
    inversion = 100
    data = readDataMlb("visualization_data_mlb.csv")
    data_analyzed = []
#     ["threshold", "odd", "diff_prob", "diff_odd", "num_bets", "perc", "mean_odd", "money", "max_loss", "max_wins", "money_max_loss"]
    
    for threshold in range(50, 90, 5):
        for odd in np.arange(1.0, 2.5, 0.1):
            for diff_prob in np.arange(0.05, 0.50, 0.05):
                for diff_odd in np.arange(0.1, 1, 0.1):
                    print(threshold, odd, diff_prob, diff_odd)
                    result = visualizeThreshold(data, inversion, threshold, threshold_odd=odd, difference_prob=diff_prob, difference_odd=diff_odd)
                    data_analyzed.append([
                            threshold, 
                            odd, 
                            diff_prob, 
                            diff_odd, 
                            result["num_bets"], 
                            result["perc"], 
                            result["mean_odd"], 
                            result["money"],
                            result["max_loss"],
                            result["max_win"],
                            result["money_max_loss"]
                    ])
    
    data_csv = pd.DataFrame(data_analyzed)
    data_csv.to_csv('analyzed_data_mlb.csv', header=True)

def getMaxCombination():
    data = readDataMlb("analyzed_data_mlb.csv")
    headers = list(data.columns)
    
    # get the row of max value
    max_combination_benefits = data.loc[data[headers[8]].idxmax()]
    max_combination_ben_loss = data.loc[data[headers[11]].idxmax()]
    min_combination_loss = data.loc[data[headers[9]].idxmax()]
    max_combination_win = data.loc[data[headers[10]].idxmax()]
    max_combination_perc = data.loc[data[headers[6]].idxmax()]
    
    print("Combinacion max beneficios: ", max_combination_benefits)
    print("Combinacion max beneficios min loss: ", max_combination_ben_loss)
    print("Combinacion max wins: ", max_combination_win)
    print("Combinacion min loss: ", min_combination_loss)
    print("Combinacion max perc: ", max_combination_perc)

def  visualizeResultsManual():
    data = readDataMlb("analyzed_data_mlb.csv")
    headers = list(data.columns)
    
    over65 = data.loc[data[headers[1]] == 70]
    sorted_array = over65.sort_values(by=[headers[6]], ascending = False)
    
    print(sorted_array.loc[:, [headers[5], headers[6],headers[8], headers[9], headers[10], headers[11]]][50:100])
    print(sorted_array.loc[5379])

#visualizeHistorical()
#getMaxCombination()
visualizeResultsManual()