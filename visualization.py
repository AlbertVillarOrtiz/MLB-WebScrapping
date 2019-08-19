# -*- coding: utf-8 -*-
"""
Created on Sun Aug 18 14:54:21 2019

@author: alber
"""
import pandas as pd
import statistics

def visualizeThreshold(df, inversion, difference_prob = 0, difference_odd = 0, threshold_odd = 0, threshold_max = 100):
    for threshold in range(50, 85, 5):
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
            print("Threshold: ", str(threshold))
            print("Pronosticos realizados: ", nBets)
            print("Pronosticos acertados: ", nGreen)
            print("Porcentaje de acierto: ", perc*100)
            if len(mean_odd) > 0:
                print("Cuota media: ", statistics.mean(mean_odd))
            print("Beneficio con inversion de " + str(inversion) + ": ", beneficio, " euros")
            print("Máximas pérdidas seguidas: ", -max_downhill*100, "euros (", max_downhill, "pronosticos )")
            print("Máximas ganancias seguidas: ", max_streak*100, "euros (", max_streak, "pronosticos )\n")

def visualizeTotal(df, inversion, results, difference_prob = 0, difference_odd = 0, threshold_odd = 0):
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
    print("Beneficio con inversion de " + str(inversion) + " euros: ", beneficio, " euros")
    print("Máximas pérdidas seguidas: ", -max_downhill*100, " euros (", max_downhill, "pronosticos )")
    print("Máximas ganancias seguidas: ", max_streak*100, "euros (", max_streak, "pronosticos )\n")

def visualizeHistorical():
    headers = ['Sport', 'League', 'Year', "Prediction", "Probability", 
                       "Odd", "Opponent_probability", "Opponent_odd", "Id_Match", "Result"]
    name = "_".join(("beisbol", "mlb", "2018"))
    data = pd.read_csv(name + ".csv") 
    inversion = 100
    df = pd.DataFrame(data, columns= headers)
    results = df[df["Result"] == 1]
    
    visualizeTotal(df, inversion, results,
                   threshold_odd = 1.8)
    visualizeThreshold(df, inversion,
                       threshold_odd = 1.8)

visualizeHistorical()