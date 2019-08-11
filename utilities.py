# -*- coding: utf-8 -*-
"""
Created on Sat Aug 10 21:11:32 2019

@author: AlbertVillarOrtiz
"""

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