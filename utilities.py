# -*- coding: utf-8 -*-
"""
Created on Sat Aug 10 21:11:32 2019

@author: AlbertVillarOrtiz
"""
import numpy as np

def formObjectToProbabilities(array):
    for key in array.keys():
        if isinstance(array[key], (list, tuple, np.ndarray)):
            for i in range(len(array[key])):
                array[key][i] = 1/array[key][i]
        else:
            array[key] = 1/array[key]
    
    return array

def getSize(array, default):
    if len(array) > default:
        result = default
    else:
        result = len(array)
        
    return result 

def normalizeData(data):
    for i in range(len(data)+1):
        result = data[i].split(":")
        if len(result) > 0:
            del data[i]
            for j in range(len(result)):
                data.insert(i+j, result[j])
        data[i] = float(data[i])

    return data

def normalizeH2hData(data):
    for i in range(len(data)):
        result = data[i].split(":")
        result[0] = float(result[0])
        result[1] = float(result[1])

    return result 

def countWins(array, names):
    probH2h = array
    for key in array.keys():
        countHome = 0
        countAway = 0
        size = len(array[key])
        for i in range(size):
            try:
                indexHome = array[key][i].index(names['home'])
            except ValueError:
                indexHome = -1
            try:
                indexAway = array[key][i].index(names['away'])
            except ValueError:
                indexAway = -1
            
            result = array[key][i][-2] > array[key][i][-1]
            if (indexHome == 0 and result) or (indexHome == 1 and not result):
                countHome = countHome + 1
            elif (indexAway == 0 and result) or (indexAway == 1 and not result):
                countAway = countAway + 1
        
        if key == "home":
            probH2h['home'] = countHome / size
        elif key == "away":
            probH2h['away'] = countAway / size
        elif key == "mutual":
            if size == 0:
                probH2h['mutual'] = {"home": 0 , "away": 0}
            else:
                probH2h['mutual'] = {"home": countHome / size , "away": countAway / size}
        
    return probH2h