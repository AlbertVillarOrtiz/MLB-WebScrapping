# -*- coding: utf-8 -*-
"""
Created on Thu Aug 15 19:52:49 2019

@author: alber
"""
"""
En esta clase queremos guardar las stats de cada deporte liga. 
- Año
- Deporte
- Liga
- Partido
    - ID
    - Prediccion
    - Resultado

Se visualizara por:
    - Partido
    - Mensual
    - Anual
    - Liga
    - Deporte
"""
import pandas as pd

class Stats():
    
    def __init__(self):
        pass
    
    def byMatch(self, threshold, sport, league, year, prediction, probability, result):
        headers = ['Sport', 'League', "Threshold", 'Year', "Prediction", "Probability", "Result"]
        data = pd.read_csv("stats.csv") 
        df = pd.DataFrame(data, columns= headers)
        
        df = df.append([sport, league, threshold, year, prediction, probability, result])
        df.to_csv ('stats.csv', index = None, header=True)
    
    def byMonth(self, sport, league):
        pass
    
    def byYear(self, threshold, sport, league, year, result):
        headers = ['Sport', 'League', "Threshold", 'Year', "Result"]
        pass
    
    def byLeague(self, threshold, sport, league, result):
        headers = ['Sport', 'League', "Threshold", "Result"]
        pass
    
    def bySport(self, threshold, sport, result):
        headers = ['Sport', "Threshold", "Result"]
        pass
    
    