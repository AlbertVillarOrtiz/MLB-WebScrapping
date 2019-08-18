# -*- coding: utf-8 -*-
"""
Created on Sun Aug 18 14:54:21 2019

@author: alber
"""
import pandas as pd
from historical import Historical

headers = ['Sport', 'League', 'Year', "Prediction", "Probability", 
                   "Odd", "Opponent_probability", "Opponent_odd", "Id_Match", "Result"]
name = "_".join(("beisbol", "mlb", "2018"))
data = pd.read_csv(name + ".csv") 
inversion = 100
beneficio = 0
df = pd.DataFrame(data, columns= headers)
results = df[df["Result"] == 1]

for index, row in df.iterrows():
    value = inversion*row["Odd"] - inversion if row["Result"] == 1 else - inversion
    beneficio = beneficio + value

print("Pronosticos realizados: ", df.shape[0])
print("Pronosticos acertados: ", results.shape[0])
print("Porcentaje de acierto: ", (results.shape[0]/df.shape[0])*100)
print("Beneficio con inversion de " + str(inversion) + " euros: ", beneficio, " euros\n")


for threshold in range(50, 85, 5):
    beneficio = 0
    matchs_prob = df[df["Probability"] > threshold/100]
    matchs_prob_winner = matchs_prob[matchs_prob["Result"] == 1]
    
    for index, row in matchs_prob.iterrows():
        value = inversion*row["Odd"] - inversion if row["Result"] == 1 else - inversion
        beneficio = beneficio + value

    porcentage = matchs_prob_winner.shape[0]/matchs_prob.shape[0] if matchs_prob.shape[0] != 0 else 0
    print("Threshold: ", str(threshold))
    print("Pronosticos realizados: ", matchs_prob.shape[0])
    print("Pronosticos acertados: ", matchs_prob_winner.shape[0])
    print("Porcentaje de acierto: ", porcentage*100)
    print("Cuota media: ", matchs_prob["Odd"].mean())
    print("Beneficio con inversion de " + str(inversion) + ": ", beneficio, " euros\n")

beneficio = 0
matchs_prob = df[df["Probability"] < 50/100]
matchs_prob_winner = matchs_prob[matchs_prob["Result"] == 1]

for index, row in matchs_prob.iterrows():
    value = inversion*row["Odd"] - inversion if row["Result"] == 1 else - inversion
    beneficio = beneficio + value

historical = Historical()

data = historical.historical

data = data["beisbol"]["mlb"]["matchs"]["2018"]
print(list(data.keys())[124])