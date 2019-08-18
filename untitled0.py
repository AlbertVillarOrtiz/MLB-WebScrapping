# -*- coding: utf-8 -*-
"""
Created on Sun Aug 18 14:54:21 2019

@author: alber
"""
import pandas as pd

headers = ['Sport', 'League', 'Year', "Prediction", "Probability", "Id_Match", "Result"]
name = "_".join(("beisbol", "mlb", "2018"))
data = pd.read_csv(name + ".csv") 
print(data)
df = pd.DataFrame(data, columns= headers)

df = df.append({
        "Sport": "a", 
        "League": "b", 
        "Year": "c",
        "Prediction": "a",
        "Probability": "c",
        "Id_Match": "b", 
        "Result": 1}, ignore_index=True)

print("Writting...")
df.to_csv (name + '.csv', header=True)
print("Match stored!!")