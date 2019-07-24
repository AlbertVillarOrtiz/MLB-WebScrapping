# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 12:26:44 2019

@author: AlbertVillarOrtiz
"""

class Match:
    league = "MLB"
    
    def __init__(self, idsTeams, idMatch):
        self.idsTeams = {
                "local": idsTeams[0],
                "away": idsTeams[1]
                }
        self.id = idMatch
        
    def setNamesMatch(self, names):
        self.names = {
                "local": names[0],
                "away": names[1]
                }
    
    def setH2hOverall(self, localO, awayO, mutualO):
        self.h2hLocalO = localO
        self.h2hAwayO = awayO
        self.h2hMutualO = mutualO
    
    def setH2hLocal(self, localL, mutualL):
        self.h2hLocalL = localL
        self.h2hMutualL = mutualL
    
    def setH2hAway(self, awayA):
        self.h2hAwayA = awayA
        
    def setClasification(self, mutualO, localL, awayA):
        self.clasMutualO = {
                "local": {
                        "POS": mutualO[0][0],
                        "GP": mutualO[0][1],
                        "GW": mutualO[0][2],
                        "GL": mutualO[0][3],
                        "PF": mutualO[0][4],
                        "PA": mutualO[0][5],
                        "PCT": mutualO[0][6]
                        },
                "away": {
                        "POS": mutualO[1][0],
                        "GP": mutualO[1][1],
                        "GW": mutualO[1][2],
                        "GL": mutualO[1][3],
                        "PF": mutualO[1][4],
                        "PA": mutualO[1][5],
                        "PCT": mutualO[1][6]
                        }
        }
        self.clasLocalL = {
                "local": {
                        "POS": localL[0][0],
                        "GP": localL[0][1],
                        "GW": localL[0][2],
                        "GL": localL[0][3],
                        "PF": localL[0][4],
                        "PA": localL[0][5],
                        "PCT": localL[0][6]
                        },
                "away": {
                        "POS": localL[1][0],
                        "GP": localL[1][1],
                        "GW": localL[1][2],
                        "GL": localL[1][3],
                        "PF": localL[1][4],
                        "PA": localL[1][5],
                        "PCT": localL[1][6]
                        }
        }
        self.clasAwayA = {
                "local": {
                        "POS": awayA[0][0],
                        "GP": awayA[0][1],
                        "GW": awayA[0][2],
                        "GL": awayA[0][3],
                        "PF": awayA[0][4],
                        "PA": awayA[0][5],
                        "PCT": awayA[0][6]
                        },
                "away": {
                        "POS": awayA[1][0],
                        "GP": awayA[1][1],
                        "GW": awayA[1][2],
                        "GL": awayA[1][3],
                        "PF": awayA[1][4],
                        "PA": awayA[1][5],
                        "PCT": awayA[1][6]
                        }
        }